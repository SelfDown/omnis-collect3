6. field2array,数组转列表
=========================================
将简单数组对象，转换为字典数组列表

获取调整的数据
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
规则主要在data_json 中

* from_field 数组来源字段
* to_field 数组值对应字段
* save_field  保存字段



配置示例

    .. code-block:: yaml
     :caption: 软件批量新增

         handler_params:
           - key: field2array
             name: 服务器转软件
             from_field: server_list
             to_field: server_id
             save_field: soft_list


    .. code-block:: json
     :caption: 请求示例


      {
         "service": "server.soft_save",
         "server_list": [
             "1dfe37a6-82a3-4172-a18c-640e75d62c0a",
             "793069ab-0a63-4676-9039-17080ee41f2e"
         ],
         "soft_name": "pix"
      }


    .. code-block:: json
     :caption: 返回示例

          {
              "msg": null,
              "count": 0,
              "code": "0",
              "data": [{
                  "server_id": "1dfe37a6-82a3-4172-a18c-640e75d62c0a",
                  "soft_name": "pix"
              }, {
                  "server_id": "793069ab-0a63-4676-9039-17080ee41f2e",
                  "soft_name": "test"
              }],
              "success": true
          }

1.from_field
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
来源列表，一般是简单数组对象

2.to_field 字段
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
从来源列表里面的值，转换的字段。其他字段直接复制
