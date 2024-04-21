# FrameWorld_Backend
dlyqs的个人网站项目，基于Nuxt3+Django的前后端框架，包含影视资源导航搜索、ChatGPT的api代理实现、个人创新的帧评论播放器等功能，也包含注册登录等基础功能。
主要定位是作为个人视频创作者的工作流智能助手网站。

此目录是后端部分，对应前端部分的地址：
- [https://github.com/dlyqs/FrameWorld_Web](https://github.com/dlyqs/FrameWorld_Web)

## 声明
后端基于Django架构，数据库使用MySQL，初始时的gpt代理对话功能模块参考开源项目：
- [https://github.com/WongSaang/chatgpt-ui](https://github.com/WongSaang/chatgpt-ui)
- [https://github.com/WongSaang/chatgpt-ui-server](https://github.com/WongSaang/chatgpt-ui-server)

但只保留了其唯一的接受发送的功能逻辑，删去了其它大部分功能，并进行了整理、优化、重构。除此之外所有功能代码均为自主编写（借助了ChatGPT）。


## 功能
（部分已实现、部分是设想）
- 数据持久化，支持 Mysql、PostgreSQL 和 Sqlite 等数据库。
- Django自带的管理面板、支持用户、对话和消息、api key管理等


## 本地开发配置
- python版本：3.8（后续可能会换成3.10或者更新的LTS版本，推荐使用虚拟环境）

1、安装依赖
~~~
pip install -r requirements.txt
~~~
环境配置常见解决方法：
换镜像源下载、管理python版本、手动下载依赖等等。

2、数据库和前后端通信
- 自己建立数据库，在后端.env文件中配置数据库连接信息DB_URL。若使用默认的sqlite数据库，则为sqlite:///PATH 。
~~~
python manage.py makemigrations
python manage.py migrate
~~~

3、启动后端
~~~
python manage.py runserver
~~~
如果后台Django没账号，可以在后台创建一个超级用户。
~~~
python manage.py createsuperuser
~~~

默认前端地址：http://localhost:3000
默认后端地址：http://localhost:8000/admin

4、api 设置
可以到后端管理系统添加，也可以在backend/chat/llm.py中修改。
如果用的是国内api转接而非官方api，需要修改类似：
~~~
openai_env = {
    'api_key': 'your-api-key',
    'api_base': 'https://xxx.com/v1',
}
~~~

5、其他
- 后端 CSRF 白名单  

如果你在访问管理后台的时候遇到 `CSRF verification failed`，可能你的 `APP_DOMAIN` 没有配置对。在 `wsgi-server` 服务下有个环境变量 `wsgi-server`。 它的值应该是 `backend-web-server` 的地址+端口, 默认： `localhost:9000`。
  
假如我把 `chagpt.com` 这个域名解析到了服务器，并且我的 `backend-web-server` 服务绑定了 9000 这个端口。正确的配置如下：

```
backend-wsgi-server:
    image: wongsaang/chatgpt-ui-wsgi-server:latest
    environment:
      - APP_DOMAIN=chagpt.com:9000
```

- 节俭模式控制（是否记录上下文）  

该功能默认处于开启状态，你可以在管理后台的 `Chat->Settings` 中关闭它，在 Settings 中有一个 `open_frugal_mode_control` 的设置项，把它的值设置为 `False`。