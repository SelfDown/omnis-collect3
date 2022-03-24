1. arr2obj 数组转对象
=========================================


    * 将整个结果转一个对象，如果有多个取第一个
    * 将数组中记录的某个字段（是数组）转对象，一个二级数组
    * 如果没有记录就是空对象


模块: arr2obj
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: index.yaml

      # 结果转对象
      - key: arr2obj
        path: collect.service_imp.result_handlers.handlers.array_2_obj
        class_name: Array2Obj
        method: handler



    .. code-block:: yaml
     :caption: zabbix 接口的部分配置

        result_handler:
          - key: filter_arr
            params:
              field: interfaces
              template: "{{type=='4'}}"
          - key: arr2obj
            params:
              field: interfaces

    .. note::
       filter_arr 是过滤数组处理器，这里arr2obj 是将结果记录中interfaces数组转对象



    .. code-block:: yaml
     :caption: 查询当前登录用户信息

      - key: currentUser
        module: "mysql"
        http: true
        sql_file: 'currentUser.sql'
        result_handler:
          - key: arr2obj

    .. note::
       获取用户信息，数组转对象。从数据库查询出对象列表，然后转成对象


