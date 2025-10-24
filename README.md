# SleekFlow Collaborative TO-DO List Application
**Objective:** Develop a scalable and well-designed TODO list API application that allows users to manage their TODOs, demonstrating your backend development skills, API design expertise, and software engineering best practices.

**Project Overview**

1. **TODO List API Application**
   1. *Core Features*
      1. TODOs CRUD
         1. Each TODO has:
            1. Unique ID
            2. Name
            3. Description
            4. Due Date
            5. Status (e.g., Not Started, In Progress, Completed)
      2. Filtering (e.g., by status, due date)
      3. Sorting (e.g., by due date, status, name)
   2. *Nice-to-have Features*
      1. Additional attributes for each TODO (e.g., priority, tags)
      2. User authentication and registration
      3. Team features
         1. Authorization (e.g., role-based access control)
         2. Real-time collaboration (e.g., shared TODO lists, activity feeds)
      4. DevOps (e.g., CI/CD pipeline, Docker, Kubernetes, Helm)
      5. Architecture diagram
      6. Any other improvements or features you'd like to add
2. **Design Requirements**
   1. *Technical Design*
      1. Adhere to SOLID principles
      2. Use Test-Driven Development (TDD)
      3. Ensure code and design consistency
   2. *API Design*
      1. Use clear and consistent naming conventions
      2. Implement proper model mapping (e.g., DTOs, ViewModels)
   3. *Documentation*
      1. Include README with instructions for setup and usage
      2. Document API endpoints and functionality
3. **Deliverables**
   1. A GitHub repository containing your source code
   2. A Swagger document or Postman collection for your API
   3. **Be prepared to present a live demo of your application during the upcoming interview, demonstrating the core features and code structure.** Please ensure you have your development environment ready and the application running locally before the interview.

**Guidelines**

1. Use a modern backend programming language and framework (e.g., [ASP.NET](http://asp.net/) Core, Python with Flask or Django, Node.js with Express, Java with Spring Boot, etc.).
2. Choose a suitable database for storing TODOs and user data (e.g., PostgreSQL, MongoDB, MySQL, MSSQL).
3. Implement error handling and validations for API requests.
4. Write unit tests and integration tests for the core functionality.
5. Ensure your application can be easily run and tested locally.


# Tech Stack
- Backend: Python (Flask + Flask-RESTX)
- Database: PostgreSQL, MongoDB, Redis
- Auth: JWT (Flask-JWT-Extended)
- Testing: pytest
- DevOps: Docker, Docker Compose, GitHub Actions


# Architecture
todo-list-api/
├── .github/                          # GitHub 配置文件
│   └── workflows/
│       └── ci.yml                    # CI/CD 流水线配置（自动化测试、构建）
├── app/                              # 应用核心代码
│   ├── __init__.py                   # 应用初始化（注册扩展、路由）
│   ├── config.py                     # 配置文件（数据库连接、JWT 密钥等）
│   ├── models/                       # 数据模型层
│   │   ├── __init__.py               # 模型统一导出
│   │   ├── users/                    # 用户/权限模型（PostgreSQL）
│   │   │   ├── __init__.py           # 用户相关模型导出
│   │   │   ├── user.py               # 用户核心模型（认证、基础信息）
│   │   │   └── permission.py         # 列表权限模型（VIEW/EDIT 权限）
│   │   └── todos/                    # TODO 模型（MongoDB）
│   │       ├── __init__.py           # TODO 相关模型导出
│   │       ├── list.py               # TODO 列表模型（元数据）
│   │       └── item.py               # TODO 项模型（具体待办内容）
│   ├── dto/                          # 数据传输对象（Pydantic 验证）
│   │   ├── __init__.py               # DTO 统一导出
│   │   ├── user_dto.py               # 用户相关 DTO（注册、登录）
│   │   └── todo_dto.py               # TODO 相关 DTO（创建、更新）
│   ├── services/                     # 业务逻辑层
│   │   ├── __init__.py               # 服务统一导出
│   │   ├── user_service.py           # 用户服务（注册、登录、权限验证）
│   │   └── todo_service.py           # TODO 服务（列表/项的 CRUD、过滤排序）
│   ├── controllers/                  # API 控制器层（Flask-RESTful）
│   │   ├── __init__.py               # 控制器统一导出
│   │   ├── auth_controller.py        # 认证控制器（注册、登录接口）
│   │   ├── todo_list_controller.py   # TODO 列表控制器（列表 CRUD 接口）
│   │   └── todo_item_controller.py   # TODO 项控制器（项 CRUD、过滤接口）
│   ├── extensions/                   # 第三方扩展初始化
│   │   ├── __init__.py               # 扩展统一导出
│   │   ├── db_postgres.py            # PostgreSQL 连接初始化、会话管理
│   │   ├── db_mongo.py               # MongoDB 连接初始化、集合获取
│   │   └── jwt.py                    # JWT 扩展初始化（认证、令牌回调）
│   └── utils/                        # 工具类
│       ├── __init__.py               # 工具统一导出
│       ├── errors.py                 # 自定义异常（资源不存在、权限不足等）
│       └── error_handlers.py         # 全局异常处理装饰器
├── tests/                            # 测试用例
│   ├── __init__.py                   # 测试统一导出
│   ├── conftest.py                   # 测试 fixtures（Flask 应用、数据库客户端）
│   ├── unit/                         # 单元测试（业务逻辑）
│   │   ├── test_user_service.py      # 用户服务测试
│   │   └── test_todo_service.py      # TODO 服务测试
│   └── integration/                  # 集成测试（API 接口）
│       ├── test_auth_api.py          # 认证接口测试
│       └── test_todo_api.py          # TODO 接口测试
├── init_scripts/                     # 数据库初始化脚本
│   ├── postgres_init.sql             # PostgreSQL 初始化（创建表、测试用户）
│   └── mongo_init.js                 # MongoDB 初始化（创建集合、测试数据）
├── Pipfile                           # 依赖管理（生产/开发依赖分离）
├── Pipfile.lock                      # 依赖版本锁定（确保环境一致性）
├── docker-compose.yml                # 开发环境配置（API + 双数据库 + 管理工具）
├── Dockerfile.dev                    # 开发用 Dockerfile（依赖安装、代码挂载）
└── README.md                         # 项目说明（启动步骤、API 文档、演示指南）
# How to Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Aaron963/todo_list_api
   cd todo-list-api
2. Start services with Docker Compose:
    ```bash
   docker compose -f .\docker-compose.yml up --build
