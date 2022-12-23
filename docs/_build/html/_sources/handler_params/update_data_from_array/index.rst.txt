7. update_data_from_array 根据数组更新数组
================================================
主要更新一个数组，数据来源也是个对象数组。

比如前端传个用户列表user_list，有用户名，没有用户ID，以及其他字段。批量更新数据库用户
数据库里面根据用户名查出用户名+用户ID的列表，需要将前台的用户user_list填充用户ID,根据用名填充

更新数组字段
     * **foreach** 循环参数中的变量
     * **item** 循环中item 名称
     * **fields** 新增、修改字段列表
     * **from_list** 来源数组
     * **from_item** 来源数组的名称
     * **ifTemplate** 2个数组中匹配的表达式
     * **foreach_key_fields** foreach 列表中匹配字段
     * **from_list_fields** from_list 列表中匹配字段


1.ifTemplate 不适合大批量数据场景，如果数据达到几千条，可能需要几分钟，因为每比较一次
实际是渲染一次模板，模板渲染多了，这比较耗时。


如果能精确匹配到字段，尽量用foreach_key_fields+from_list_fields。只能模糊匹配，
者算法匹配就只能用ifTemplate

2. foreach_key_fields+from_list_fields 表示2个数组，列出关键字段进行比较
配置示例1

    .. code-block:: yaml
     :caption: index.yaml

      - key: update_data_from_array
        params:
          foreach: local_user_list
          item: item
          fields:
            - field: tel
              template: "second_item.mobile"
            - field: wechat_userid
              template: "second_item.userid"
          from_list: remote_user_list
          from_item: second_item
          ifTemplate: "{{ item.nick == second_item.name or item.username+'@' in second_item.biz_mail }}"


foreach_key_fields+from_list_fields配置示例2

    .. code-block:: yaml
     :caption: index.yaml

      - key: update_data_from_array
        enable: "{{standard_list|length >0 and user_table_data|length >0}}"
        name: 更新同步标准
        params:
          foreach: user_table_data
          item: item
          fields:
            - field: export_way
              template: second_item.export_way
          from_list: standard_list
          from_item: second_item
          foreach_key_fields:
            - table
          from_list_fields:
            - table_name