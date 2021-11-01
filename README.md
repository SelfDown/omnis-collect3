# omnis-collect
omnis-collect是web接口配置工具。目的是将系统接口都统一，简单点说，将所有的业务接口统一、让系统只有一个http接口，业务接口都是配置出来。
实现通过一些简单配置，可以提供http接口服务。

目前已经实现
1. 路由配置。将接口分目录管理，可以相似业务模块的功能放在一个大目录，同一页面的接口功能放在一个文件
1. 模板查询。利用jinja2模板渲染+yml的语法。通过配置sql文件，实现根据配置sql 转http接口
1. 模型数据新增、修改、删除。利用django model的orm,实现对模型数据的新增、修改、删除
1. Excel文件下载。基于配置模板查询的数据，实现数据导出
1. Excel 文件导入更新。批量更新操作，数据库一次性执行
***


***
## 目录结构
```
────────────────────────────────
├── conf
│   └── application.properties
├── sample
│   ├── app
│   └── settings.py
├── omnis_data_service
│   └── service_router.yml
────────────────────────────────
```
文档
https://omnis-collect3.readthedocs.io/en/latest/