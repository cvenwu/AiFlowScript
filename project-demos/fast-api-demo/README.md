# fast-api-demo

一个最小化的 FastAPI 示例项目。

## 环境要求

- Python >= 3.14
- [uv](https://github.com/astral-sh/uv)

## 运行项目

```bash
uv run uvicorn main:app --reload
```

启动后访问：

- API: http://127.0.0.1:8000
- 交互式文档（Swagger UI）: http://127.0.0.1:8000/docs

## 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/` | 返回欢迎信息 |
| GET | `/healthz` | 健康检查 |
