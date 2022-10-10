3. check_array
=========================================
检查数组，数据是否符合要求


check_array 检查数组
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

     * item_order_index 表示数据的序号，从1开始

配置示例

    .. code-block:: yaml
     :caption: 批量更新upstream 配置


         handler_params:
           - key: check_array
             foreach: update_list
             item: item
             fields:
               - template: "{{item.name|must}}"
                 err_msg: "第【{{item_order_index}}】记录【负载均衡】名称不能为空"

