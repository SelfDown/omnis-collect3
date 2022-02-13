# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 14:00
@Author: zzhang zzhang@cenboomh.com
@File: bulk_create.py
@desc:
"""
import json

from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class BulkUpdateService(CollectService):
    BUSConst = {
        "update_fields_name": "update_fields",
        "exclude_fields_name": "exclude_fields"
    }

    def __init__(self, op_user):
        CollectService.__init__(self, op_user)

        pass

    def get_update_fields_name(self):
        return self.BUSConst["update_fields_name"]

    def get_exclude_fields_name(self):
        return self.BUSConst["exclude_fields_name"]

    def result(self, params=None):
        result = CollectService.result(self, params)
        if self.finish or not self.is_success(result):
            return result
        params_result = self.get_params_result()
        models = get_safe_data(self.get_model_field_name(), self.template)
        models_result = get_safe_data(models, params_result)
        if not models_result:
            return self.fail("没有修改数据对象")
        model_obj_result = self.get_model_obj()
        if not self.is_success(model_obj_result):
            return model_obj_result

        model_list = []
        for param in models_result:
            model_obj_result = self.get_model_obj()
            model_obj = self.get_data(model_obj_result)
            # 更新字段
            model_obj_result = self.update_field(model_obj, param)
            if not model_obj_result:
                return model_obj_result
            model_list.append(self.get_data(model_obj_result))
        # model_class = self.get_model_class()
        # model_class.
        update_fields = get_safe_data(self.get_update_fields_name(), self.template)
        exclude_fields = get_safe_data(self.get_exclude_fields_name(), self.template)
        try:
            send_count, update_count = self.bulk_update(model_list, update_fields=update_fields,
                                                        exclude_fields=exclude_fields)

            if send_count != update_count:
                self.log("批量更新数据,发送总量【" + str(send_count) + "】和更新量【" + str(update_count) + "】不一致")
                self.log(json.dumps(params))
        except Exception as e:
            return self.fail(str(e) + "修改失败")

        return self.success(params, count=update_count)

    def bulk_update(self, objs, meta=None, update_fields=None, exclude_fields=None,
                    using='default', batch_size=None, pk_field='pk'):
        assert batch_size is None or batch_size > 0

        # force to retrieve objs from the DB at the beginning,
        # to avoid multiple subsequent queries
        objs = list(objs)
        if not objs:
            return
        batch_size = batch_size or len(objs)

        if meta:
            fields = get_fields(update_fields, exclude_fields, meta)
        else:
            meta = objs[0]._meta
            if update_fields is not None:
                fields = get_fields(update_fields, exclude_fields, meta, objs[0])
            else:
                fields = None

        if fields is not None and len(fields) == 0:
            return

        if pk_field == 'pk':
            pk_field = meta.get_field(meta.pk.name)
        else:
            pk_field = meta.get_field(pk_field)

        connection = connections[using]
        query = UpdateQuery(meta.model)
        compiler = query.get_compiler(connection=connection)

        # The case clause template; db-dependent
        # Apparently, mysql's castable types are very limited and have
        # nothing to do with the column types. Still, it handles the uncast
        # types well enough... hopefully.
        # http://dev.mysql.com/doc/refman/5.5/en/cast-functions.html#function_cast
        #
        # Sqlite also gives some trouble with cast, at least for datetime,
        # but is also permissive for uncast values
        vendor = connection.vendor
        use_cast = 'mysql' not in vendor and 'sqlite' not in vendor
        if use_cast:
            template = '"{column}" = CAST(CASE "{pk_column}" {cases}ELSE "{column}" END AS {type})'
        else:
            template = '"{column}" = (CASE "{pk_column}" {cases}ELSE "{column}" END)'

        case_template = "WHEN %s THEN {} "

        lenpks = 0
        for objs_batch in grouper(objs, batch_size):

            pks = []
            parameters = defaultdict(list)
            placeholders = defaultdict(list)

            for obj in objs_batch:

                pk_value, _ = _as_sql(obj, pk_field, query, compiler, connection)
                pks.append(pk_value)

                loaded_fields = fields or get_fields(update_fields, exclude_fields, meta, obj)

                for field in loaded_fields:
                    value, placeholder = _as_sql(obj, field, query, compiler, connection)
                    if value is None:
                        continue
                    parameters[field].extend(flatten([pk_value, value], types=tuple))
                    placeholders[field].append(placeholder)

            values = ', '.join(
                template.format(
                    column=field.column,
                    pk_column=pk_field.column,
                    cases=(case_template * len(placeholders[field])).format(*placeholders[field]),
                    type=_get_db_type(field, connection=connection),
                )
                for field in parameters.keys()
            )

            parameters = flatten(parameters.values(), types=list)
            parameters.extend(pks)

            n_pks = len(pks)
            del pks

            dbtable = '"{}"'.format(meta.db_table)

            in_clause = '"{pk_column}" in ({pks})'.format(
                pk_column=pk_field.column,
                pks=', '.join(itertools.repeat('%s', n_pks)),
            )

            sql = 'UPDATE {dbtable} SET {values} WHERE {in_clause}'.format(
                dbtable=dbtable,
                values=values,
                in_clause=in_clause,
            )
            del values

            # String escaping in ANSI SQL is done by using double quotes (").
            # Unfortunately, this escaping method is not portable to MySQL,
            # unless it is set in ANSI compatibility mode.
            if 'mysql' in vendor:
                sql = sql.replace('"', '`')

            lenpks += n_pks
            if self.can_log():
                self.log(sql)
                self.log(parameters)

            result = connection.cursor().execute(sql, parameters)

        return lenpks, result.rowcount


import itertools

from collections import defaultdict

from django.db import connections, models
from django.db.models.query import QuerySet
from django.db.models.sql import UpdateQuery


def _get_db_type(field, connection):
    if isinstance(field, (models.PositiveSmallIntegerField,
                          models.PositiveIntegerField)):
        # integer CHECK ("points" >= 0)'
        return field.db_type(connection).split(' ', 1)[0]

    return field.db_type(connection)


def _as_sql(obj, field, query, compiler, connection):
    value = getattr(obj, field.attname)

    if hasattr(value, 'resolve_expression'):
        value = value.resolve_expression(query, allow_joins=False, for_save=True)
    else:
        value = field.get_db_prep_save(value, connection=connection)

    if hasattr(value, 'as_sql'):
        placeholder, value = compiler.compile(value)
        if isinstance(value, list):
            value = tuple(value)
    else:
        placeholder = '%s'

    return value, placeholder


def flatten(l, types=(list, float)):
    """
    Flat nested list of lists into a single list.
    """
    l = [item if isinstance(item, types) else [item] for item in l]
    return [item for sublist in l for item in sublist]


def grouper(iterable, size):
    # http://stackoverflow.com/a/8991553
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            return
        yield chunk


def validate_fields(meta, fields):
    fields = frozenset(fields)
    field_names = set()

    for field in meta.fields:
        if not field.primary_key:
            field_names.add(field.name)

            if field.name != field.attname:
                field_names.add(field.attname)

    non_model_fields = fields.difference(field_names)

    if non_model_fields:
        raise TypeError(
            "These fields are not present in "
            "current meta: {}".format(', '.join(non_model_fields))
        )


def get_fields(update_fields, exclude_fields, meta, obj=None):
    deferred_fields = set()

    if update_fields is not None:
        validate_fields(meta, update_fields)
    elif obj:
        deferred_fields = obj.get_deferred_fields()

    if exclude_fields is None:
        exclude_fields = set()
    else:
        exclude_fields = set(exclude_fields)
        validate_fields(meta, exclude_fields)

    exclude_fields |= deferred_fields

    fields = [
        field
        for field in meta.concrete_fields
        if (
                not field.primary_key and
                obj and getattr(obj, field.attname) is not None and
                field.attname not in deferred_fields and
                field.attname not in exclude_fields and
                field.name not in exclude_fields and
                (
                        update_fields is None or
                        field.attname in update_fields or
                        field.name in update_fields
                )
        )
    ]

    return fields
