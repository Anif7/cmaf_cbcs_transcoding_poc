# Clean Code & Architectural Rules

To ensure high-quality and maintainable code, all development in this repository MUST follow these core principles:

## 1. Clean Code Principles
- **Single Responsibility Principle (SRP)**: Each class, module, and function should have one, and only one, reason to change. Extract complex logic into dedicated helper methods or classes.
- **Level of Abstraction**: Maintain consistent levels of abstraction within a single function or class. High-level policy should be decoupled from low-level implementation details.
- **Better Naming**: Use intent-revealing names for variables, functions, and classes. Avoid generic names like `data`, `process`, or `handler` without specific context.
- **Minimize Comments & Docstrings**: Do not include unnecessary comments or docstrings. Only include them if the task is critical or the logic is not easily understandable. Code should be self-explanatory.

## 2. Structural Patterns
- **Domain Layer (`app/domain/`)**: All business logic and external tool orchestration (FFmpeg, Shaka, Rclone) must reside here. This layer should be independent of frameworks (Django/FastAPI) where possible.
- **Models Layer (`app/models/`)**: Dedicated to database schemas and state persistence.
- **Views Layer (`app/views/`)**: Dedicated to API request handling and interaction with the domain layer.
- **Tasks Layer (`app/tasks/`)**: Dedicated to asynchronous task definitions (Celery).

## 3. Tool Orchestration
- **Explicit CLI Wrappers**: All subprocess calls to external tools MUST be wrapped in dedicated, well-named service classes within the domain layer.
- **Sub-task Execution**: Complex tool commands should be built and validated via separate methods to ensure SRP compliance.
