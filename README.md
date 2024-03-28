# chatgpt_django_frame
基于开源项目的修改和二次开发

原项目：
- 客户端，基于 [Nuxt](https://nuxt.com/)，项目地址：[https://github.com/WongSaang/chatgpt-ui](https://github.com/WongSaang/chatgpt-ui)
- 服务端，基于 [Django](https://djangoproject.com/)，项目地址：[https://github.com/WongSaang/chatgpt-ui-server](https://github.com/WongSaang/chatgpt-ui-server)

## 功能与特性
### 客户端
- 用户系统，支持用户注册、登录、修改密码等。
- 用户界面多语言，支持多种语言。
- 数据持久化，支持 Mysql、PostgreSQL 和 Sqlite 等数据库。
- 异步对话，支持多个对话同时进行。
- 历史对话管理。
- 持续聊天，让 ChatGPT 客户历史聊天记录回答问题，得出更好的答案。
- 网页搜索能力，让 ChatGPT 获取最新信息。
- 便捷的工具，支持一键复制消息和代码块，以及重新编辑消息等。
- 常用指令管理，用户可存储和编辑自己的常用指令。
- PWA，支持安装到桌面。
- 用户 Token 使用量统计
- 支持配置多个 API Key

### 服务端
- 服务端拥有一个管理面板
- 用户管理
- 对话和消息管理
- 常用配置


## 本地开发配置
1、安装前后端依赖
前端
~~~
yarn install
~~~
后端
~~~
pip install -r requirements.txt
~~~
环境配置常见解决方法：
换镜像源下载、管理node版本、手动下载依赖等等。

2、数据库和前后端通信
- 自己建立数据库，在后端.env文件中配置数据库连接信息
- 前端不需要管数据库，在前端.env文件中配置后端服务地址，也可以直接在frontend/server/middleware/apiProxy.ts 修改。
- 如果修改了后端地址端口还是没用，需要在本地环境变量中添加。

3、启动前后端
到这应该没啥大问题了
前端
~~~
yarn dev
~~~
后端
~~~
python manage.py runserver
~~~
然后就可以打开浏览器访问了。
如果后台Django没账号，可以在后台创建一个超级用户。
~~~
python manage.py createsuperuser
~~~

前端地址：http://localhost:3000
后端地址：http://localhost:8000/admin


4、OpenAI api
可以到后端管理系统添加，也可以在backend/chat/llm.py中修改。
如果用的是国内api转接而非官方api，需要修改
~~~
openai_env = {
    'api_key': 'your-api-key',
    'api_base': 'https://xxx.com/v1',
}
~~~