# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EventLog(models.Model):
    event_id = models.CharField(primary_key=True, max_length=50, blank=True, null=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    from_service = models.CharField(max_length=200)
    to_service = models.CharField(max_length=200, blank=True, null=True)
    params = models.CharField(max_length=4000, blank=True, null=True)
    create_user_id = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.CharField(max_length=50, blank=True, null=True)
    finish_time = models.CharField(max_length=50, blank=True, null=True)
    success = models.CharField(max_length=5, blank=True, null=True)
    result = models.CharField(max_length=4000, blank=True, null=True)
    msg = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_log'


class LdapGroup(models.Model):
    ldap_group_id = models.CharField(primary_key=True, max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ldap_group'


class Project(models.Model):
    project_id = models.CharField(primary_key=True, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    create_time = models.CharField(max_length=50, blank=True, null=True)
    create_user = models.CharField(max_length=50, blank=True, null=True)
    is_delete = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class Role(models.Model):
    role_id = models.CharField(primary_key=True, max_length=50, blank=True, null=True)
    role_name = models.CharField(max_length=255, blank=True, null=True)
    order_index = models.IntegerField(blank=True, null=True)
    role_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class RoleLdapGroup(models.Model):
    role_ldap_group_id = models.CharField(primary_key=True, max_length=50, blank=True, null=True)
    role_id = models.CharField(max_length=50, blank=True, null=True)
    ldap_group_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role_ldap_group'


class RoleMenu(models.Model):
    role_menu_id = models.CharField(primary_key=True, max_length=50, blank=True, null=True)
    role_id = models.CharField(max_length=50, blank=True, null=True)
    menu_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role_menu'


class SysCode(models.Model):
    sys_code_id = models.CharField(primary_key=True, blank=True, null=True)
    sys_code_type = models.CharField(blank=True, null=True)
    sys_code_type_name = models.CharField(blank=True, null=True)
    sys_code = models.CharField(blank=True, null=True)
    sys_code_text = models.CharField(blank=True, null=True)
    order_index = models.IntegerField(blank=True, null=True)
    icon = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_code'


class SysMenu(models.Model):
    menu_id = models.CharField(primary_key=True, blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    menu_type = models.CharField(blank=True, null=True)
    menu_url = models.CharField(blank=True, null=True)
    parent_id = models.CharField(blank=True, null=True)
    order_index = models.IntegerField(blank=True, null=True)
    icon = models.CharField(blank=True, null=True)
    icon2 = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_menu'


class SysProjects(models.Model):
    sys_project_id = models.CharField(primary_key=True, max_length=100, blank=True, null=True)
    project_name = models.CharField(max_length=1000, blank=True, null=True)
    project_code = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    modify_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    create_user = models.CharField(max_length=50, blank=True, null=True)
    modify_user = models.CharField(max_length=50, blank=True, null=True)
    comments = models.CharField(max_length=225, blank=True, null=True)
    is_delete = models.CharField(max_length=2, blank=True, null=True)
    order_index = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_projects'


class UserAccount(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50, blank=True, null=True)
    nick = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    user_status = models.CharField(max_length=50, blank=True, null=True)
    entry_date = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    leave_date = models.CharField(max_length=50, blank=True, null=True)
    is_delete = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.CharField(max_length=50, blank=True, null=True)
    create_user = models.CharField(max_length=50, blank=True, null=True)
    modify_user = models.CharField(max_length=50, blank=True, null=True)
    modify_time = models.CharField(max_length=50, blank=True, null=True)
    work_code = models.CharField(max_length=200, blank=True, null=True)
    create_ldap = models.CharField(max_length=50, blank=True, null=True)
    ldap_success = models.CharField(max_length=2, blank=True, null=True)
    ldap_msg = models.CharField(max_length=500, blank=True, null=True)
    svn_success = models.CharField(max_length=2, blank=True, null=True)
    svn_msg = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_account'


class UserRole(models.Model):
    user_role_id = models.CharField(primary_key=True, max_length=50, blank=True, null=True)
    role_id = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_role'