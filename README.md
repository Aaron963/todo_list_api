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

# How to Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Aaron963/todo_list_api
   cd todo-list-api
2. Start services with Docker Compose:
    ```bash
   docker compose -f .\docker-compose.yml up --build
