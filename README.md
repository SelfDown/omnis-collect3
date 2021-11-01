# omnis-collect
omnis-collect是web接口配置工具。目的是将系统接口都统一。
简单点说，将所有的业务接口统一、让系统只有一个http接口，业务接口都是配置出来。
实现通过一些简单配置，可以提供http接口服务。


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