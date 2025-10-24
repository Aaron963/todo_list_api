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
- Backend: Python (Flask + Flask-Restful)
- Database: PostgreSQL, MongoDB, Redis
- Auth: JWT (Flask-JWT-Extended)
- Testing: pytest
- DevOps: Docker, Docker Compose, GitHub Actions


# Architecture
```bash
todo-list-api/
├── .github/                          # GitHub configuration files
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline config (auto-testing, building)
├── app/                              # Core application code
│   ├── __init__.py                   # App initialization (register extensions, routes)
│   ├── config.py                     # Configuration (DB connections, JWT secrets, etc.)
│   ├── models/                       # Data models layer
│   │   ├── __init__.py               # Unified model export
│   │   ├── users/                    # User/Permission models (PostgreSQL)
│   │   │   ├── __init__.py           # User-related model export
│   │   │   ├── user.py               # Core user model (auth, basic info)
│   │   │   └── permission.py         # List permission model (VIEW/EDIT permissions)
│   │   └── todos/                    # TODO models (MongoDB)
│   │       ├── __init__.py           # TODO-related model export
│   │       ├── list.py               # TODO list model (metadata)
│   │       └── item.py               # TODO item model (specific task content)
│   ├── dto/                          # Data Transfer Objects (Pydantic validation)
│   │   ├── __init__.py               # Unified DTO export
│   │   ├── user_dto.py               # User-related DTOs (registration, login)
│   │   └── todo_dto.py               # TODO-related DTOs (creation, update)
│   ├── services/                     # Business logic layer
│   │   ├── __init__.py               # Unified service export
│   │   ├── user_service.py           # User service (registration, login, permission check)
│   │   └── todo_service.py           # TODO service (CRUD, filtering, sorting for lists/items)
│   ├── controllers/                  # API controller layer (Flask-RESTful)
│   │   ├── __init__.py               # Unified controller export
│   │   ├── auth_controller.py        # Auth controller (registration, login endpoints)
│   │   ├── todo_list_controller.py   # TODO list controller (list CRUD endpoints)
│   │   └── todo_item_controller.py   # TODO item controller (item CRUD, filtering endpoints)
│   ├── extensions/                   # Third-party extension initialization
│   │   ├── __init__.py               # Unified extension export
│   │   ├── db/db_postgres.py            # PostgreSQL connection init & session management
│   │   ├── db/db_mongo.py               # MongoDB connection init & collection retrieval
│   │   └── jwt/jwt.py                    # JWT extension init (auth, token callbacks)
│   └── utils/                        # Utility classes
│       ├── __init__.py               # Unified utility export
│       ├── errors.py                 # Custom exceptions (resource not found, permission denied, etc.)
│       └── error_handlers.py         # Global exception handling decorator
├── tests/                            # Test cases
│   ├── __init__.py                   # Unified test export
│   ├── conftest.py                   # Test fixtures (Flask app, DB clients)
│   ├── unit/                         # Unit tests (business logic)
│   │   ├── test_user_service.py      # User service tests
│   │   └── test_todo_service.py      # TODO service tests
│   └── integration/                  # Integration tests (API endpoints)
│       ├── test_auth_api.py          # Auth API tests
│       └── test_todo_api.py          # TODO API tests
├── scripts/                          # DB initialization scripts
│   ├── postgres_init.sql             # PostgreSQL init (table creation, test user)
│   └── mongo_init.js                 # MongoDB init (collection creation, test data)
├── Pipfile                           # Dependency management (separates prod/dev dependencies)
├── Pipfile.lock                      # Dependency version lock (ensures env consistency)
├── docker-compose.yml                # Dev environment config (API + dual DB + management tools)
├── Dockerfile.dev                    # Dev-focused Dockerfile (dependency install, code mounting)
└── README.md                         # Project documentation (setup steps, API docs, demo guide)
```

# How to Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Aaron963/todo_list_api
   cd todo-list-api
   ```

2. Start services with Docker Compose:
    ```bash
   docker compose -f .\docker-compose.yml up --build
   ```

# API Documentaion

https://winter-astronaut-286841.postman.co/workspace/My-Workspace~a1448db5-4ee7-4e5a-8f01-7d870c73d919/collection/19369308-81ee660a-c614-4002-9993-f166636ee969?action=share&creator=19369308&active-environment=19369308-b05be95c-b0fa-4277-aa0c-4676c116cf8c