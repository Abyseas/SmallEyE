# Web Short video后端Demo
> 使用 Python + FastAPI + qiniu sdk 开发后端



## 安装

> 运行环境：**python版本：3.9.13**



### 第三方库导入

**方式一：requirements.txt安装**

```bash
pip install -r requirements.txt
```

**方式二：手动安装**

安装七牛云

```bash
pip install qiniu
```

安装FastAPI

```bash
pip install fastapi
pip install uvicorn[standard]
pip install python-multipart
pip install SQLAlchemy
```



### 运行

启动服务器

```bash
uvicorn main:app --reload
```

交互式API文档

跳转到 http://127.0.0.1:8000/docs
