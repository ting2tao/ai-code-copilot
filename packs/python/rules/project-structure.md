---
trigger: always_on
name: python-project-structure
description: Python 项目结构与模块边界
globs: "*.py,pyproject.toml,requirements.txt"
---
# Python 项目结构

- 优先识别项目现有布局：`src/` layout、扁平 package、FastAPI/Django/Celery 等。
- Web 入口层只做协议转换、鉴权、参数校验，不写复杂业务逻辑。
- 业务服务、数据访问、外部客户端应分层放置，并通过依赖注入或显式参数连接。
- 测试目录结构应能映射被测模块，避免所有测试堆在一个大文件里。
- 配置通过环境变量、配置文件或项目既有配置系统读取，不硬编码在模块导入阶段。
