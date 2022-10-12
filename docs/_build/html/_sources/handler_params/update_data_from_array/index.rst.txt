7. update_data_from_array 根据数组更新数组
================================================
更新数组字段
     * **foreach** 循环参数中的变量
     * **item** 循环中item 名称
     * **fields** 新增、修改字段列表
     * **from_list** 来源数组
     * **from_item** 来源数组的名称
     * **ifTemplate** 2个数组中匹配的表达式



配置示例

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