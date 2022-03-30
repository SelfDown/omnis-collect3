3. 结果转树形结构
=========================================


    * 将列表结构的数据，转树形结构数据
    * 记录中有父ID字段


模块: to_tree
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: index.yaml

       # 结果转树 实现类

      - key: to_tree
        path: collect.service_imp.result_handlers.handlers.to_tree
        class_name: ToTree
        method: handler



:::::::::::::::::::::::::::::::::::::::::::::
1. 字段解释


     * **id_field** 记录ID 字段
     * **parent_id_field** 父ID字段，默认父ID 为0 为父节点
     * **children_field** 保存到children字段，默认children


2. to_tree 是result_handler 的结果处理器



     .. code-block:: yaml
      :caption: 将用户的菜单栏转树形结构

      # 查询当前用户菜单
      - key: userMenu
        module: "sql"
        http: true
        params:
          user_id:
            template: "{% if user_id %} {{user_id}} {% else %}{{session_user_id}}{% endif %}"
        sql_file: 'userMenu.sql'
        result_handler:
          - key: to_tree
            params:
              id_field: "menu_id"
              parent_id_field: "menu_pid"
              children_field: "children"

     .. figure:: ./menu.png
        :width: 100%
        :align: center
        :alt: 菜单信息



     .. code-block:: yaml
      :caption: 项目环境

        # 项目和环境信息转树形结构
      - key: "projectTree"
        module: 'sql'# 执行mysql 查询
        http: true
        log: true
        params:
          search:
            template: "{% if search %}%{{search}}%{% endif %}"
            name: 搜索内容
        sql_file: 'projectTree.sql'
        result_handler:
          - key: to_tree
            params:
              id_field: "id"
              parent_id_field: "parent_id"
              children_field: "children"



     .. figure:: ./env.png
        :width: 100%
        :align: center
        :alt: 环境信息





