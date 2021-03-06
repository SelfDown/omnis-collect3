5. http 模块。服务端发http 请求
=========================================
http 模块主要用于在服务端，发http 请求，后台有需要调用和集成第三方服务，比如我调用过zabbix、jira、confluence、grafana、企业微信
    * 基于requests 库，能调用requests,大部分api。一些文件操作还需特殊处理，普通发数据的请求没有一点问题
    * 优化BaseAuth,支持传字典
    * 优化请求头"Content-Type": "application/json",data 字段直接自动json dump
    * 支持进入公共文件,参考mybaties 引入文件模式，可以将一些公共模块，比如请求头，请求地址等引入
    * 配置化发请求。参考思路ajax 的调用方式，可以通过一段配置，发http的请求。


模块: http
>>>>>>>>>>>>>>>>>>>>>>
配置示例

**注意** 根据requests的api GET 请求传params,post请求传data

success 结果True 表示正常。False 表示错误
err_msg 结果为False 的错误异常信息



1. 发grafana 请求
::::::::::::::::::::
查询grafana 面板 



    .. code-block:: yaml
     :caption: index.yaml


      - key: query
        module: "http"
        must_login: false
        data_json: dash_query.json
        success: "{% if message %}False{% endif %}"
        err_msg: message

    grafana_server_url 是conf/application.properties的配置里面的配置
        
    .. code-block:: json
     :caption: dash_query.json


        {
          "url": "{{'grafana_server_url'|get_key}}/api/search/",
          "method": "get",
          "params": {
            "type": "dash-db"
          }
        }


2. 创建jira的issue
::::::::::::::::::::
创建jira issue,支持BaseAuth 



    .. code-block:: yaml
     :caption: index.yaml

       # http 实现类
      - key: http
        path: collect.service_imp.http.http_service
        class_name: HttpService
        method: handler

      # 这里一个创建jira 的http 请求  params 和handler_params 处理请求参数和验证一些参数，请忽略    
      - key: createIssue
        name: 创建Issue
        module: "http"
        params:
          projectKey:
            check:
              template: "{{projectKey|must}}"
              err_msg: "项目编码不能为空"
          summary:
            check:
              template: "{{summary|must}}"
              err_msg: "标题不能为空"
          description:
            check:
              template: "{{description|must}}"
              err_msg: "描述不能为空"
          label:
            default: ""
          assignee:
            default: ""
          componentName:
            check:
              template: "{{componentName|must}}"
              err_msg: "模块不能为空"
            default: ""
          fixVersion:
            default: ""
          reporter:
            check:
              template: "{{reporter|must}}"
              err_msg: "报告人不能为空"
          priority:
            check:
              template: "{{priority|must}}"
              err_msg: "优先级不能为空"
          issueType:
            check:
              template: "{{issueType|must}}"
              err_msg: "问题类型不能为空"
          hasScript:
            default: "10122"
          duedate:
            default: ""
          beans:
            default: "0"

        handler_params:
          - key: service2field # 获取项目信息
            service:
              service: 'jira.projectInfo'
              projectKey: "projectKey"
              username: username
              password: password
            save_field: 'projectInfo'
            template: "{{projectInfo.id}}"
            err_msg: "【{{projectKey}}】项目不存在"

          - key: arrayValue
            foreach: "projectInfo.issueTypes"
            ifTemplate: "{% if item.id == issueType %} True {% endif %}"
            valueTemplate: "{{item.id}}"
            save_field: hasIssueType
            template: "{% if hasIssueType %} True {% else %} False {% endif %}"
            err_msg: "【{{issueType}}】问题类型不存在"

          - key: arrayValue
            enable: "{% if componentName %} True {% else %} False {% endif %}"
            foreach: "projectInfo.components"
            ifTemplate: "{% if item.name == componentName %} True {% endif %}"
            valueTemplate: "{{item.id}}"
            save_field: componentId
            template: "{% if componentId %} True {% else %} False {% endif %}"
            err_msg: "【{{componentName}}】所属模块不存在"

          - key: arrayValue
            enable: "{% if fixVersion %} True {% else %} False {% endif %}"
            foreach: "projectInfo.versions"
            ifTemplate: "{% if item.name == fixVersion %}True {% endif %}"
            valueTemplate: "{{item.id}}"
            save_field: fixVersionId
            template: "{% if fixVersionId %} True {% else %} False {% endif %}"
            err_msg: "【{{fixVersion}}】所属版本不存在"
        http: true
        data_json: create_issue.json

    .. code-block:: python
     :caption: create_issue.json
        #  create_issue.json ，require 进入公共文件。url、method、headers、data,都是requests 的api

        {
          "url": "{{'jira_server'|get_key}}/rest/api/2/issue",
          "method": "post",
          "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json"
          },
          "data": {
            "fields": {
              "project": {
                "id": "{{projectInfo.id}}"
              },
              "summary": {{summary|json_str}},
              "issuetype": {
                "id": "{{issueType}}"
              },
              "description": {{description|json_str}},
              {% if assignee  %}
              "assignee": {
                "name": "{{assignee}}"
              },
              {% endif %}
              "reporter": {
                "name": "{{reporter}}"
              },
              "priority": {
                "id": "{{priority}}"
              },
              {% if fixVersionId %}
              "fixVersions": [
                {
                  "id": "{{fixVersionId}}"
                }
              ],
              {% endif %}

              {% if componentId %}
              "components": [
                {
                  "id": "{{componentId}}"
                }
              ],
              {% endif %}
              {% if beans%}
              "customfield_10301": {{beans}},
              {% endif %}
              {% if label %}
              "labels": ["{{label}}"],
              {% endif %}
              {% if duedate %}
              "duedate": "{{duedate}}",
              {% endif %}
              {% if hasScript %}
              "customfield_10241": {
                "id":"{{hasScript}}"
              }
              {% endif %}
            }
          },
           require("../common/auth.common")
        }
    .. code-block:: json
     :caption: auth.common
        #auth.common 公共文件， 处理baseAuth ，输入jira 的账号和密码

        "auth": {
            "username": "{{username}}",
            "password": "{{password}}"
        }


    .. code-block:: python
     :caption: requests 的api

     def request(method, url, **kwargs):
         """Constructs and sends a :class:`Request <Request>`.

         :param method: method for the new :class:`Request` object.
         :param url: URL for the new :class:`Request` object.
         :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
         :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
         :param json: (optional) json data to send in the body of the :class:`Request`.
         :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
         :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
         :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
             ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
             or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
             defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
             to add for the file.
         :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
         :param timeout: (optional) How long to wait for the server to send data
             before giving up, as a float, or a :ref:`(connect timeout, read
             timeout) <timeouts>` tuple.
         :type timeout: float or tuple
         :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
         :type allow_redirects: bool
         :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
         :param verify: (optional) whether the SSL cert will be verified. A CA_BUNDLE path can also be provided. Defaults to ``True``.
         :param stream: (optional) if ``False``, the response content will be immediately downloaded.
         :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
         :return: :class:`Response <Response>` object
         :rtype: requests.Response

         Usage::

           >>> import requests
           >>> req = requests.request('GET', 'http://httpbin.org/get')
           <Response [200]>
         """

         # By using the 'with' statement we are sure the session is closed, thus we
         # avoid leaving sockets open which can trigger a ResourceWarning in some
         # cases, and look like a memory leak in others.
         with sessions.Session() as session:
             return session.request(method=method, url=url, **kwargs)

