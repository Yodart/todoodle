# Todoodle

![Flask](https://img.shields.io/badge/Flask-Web%20Framework-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-blue)
![JWT](https://img.shields.io/badge/JWT-Authentication-yellow)
![CRUD](https://img.shields.io/badge/CRUD%20Operations-green)

This Todo API is built using Flask and Python, offering CRUD (Create, Read, Update, Delete) operations for managing tasks. The data is stored in a PostgreSQL database, and it includes JWT authentication for secure access. 🐍

## Features

- Create, read, update, and delete tasks (CRUD operations).
- Secure authentication using JWT (JSON Web Tokens).
- Storage of task data in a PostgreSQL database.
- Built with Flask, a lightweight and easy-to-extend web framework.

## Getting Started

### Prerequisites

Before running the Todo API, make sure you have the following prerequisites installed:

- Python 3.x
- PostgreSQL database
- Required Python packages (Flask, psycopg2, jwt, random_word)

### Installation

1. Clone the repository (if using version control):
```bash
git clone https://github.com/YourUsername/todo-api.git
cd todo-api
```

2. Install the required Python packages:
```bash
pip install Flask psycopg2 jwt random_word
```

3. Create a PostgreSQL database and configure the connection in the db.py file.

4. Run the application:
```bash
python app.py
```

## Usage

### Authentication

To access protected routes, you need to authenticate using JWT (JSON Web Tokens). Follow these steps:
1. **Register a User**: Send a POST request to `/user` with a JSON payload containing `name` and `password`.
2. **Login**: Send a POST request to `/login` with a JSON payload containing `name` and `password`. You will receive a JWT token in response.
3. **Use the JWT Token**: Include the JWT token in the `x-access-token` header when making requests to protected routes, such as `/todos`.

### CRUD Operations
- **Create a Todo**: Send a POST request to `/todos` with a JSON payload containing `title` to create a new task.
- **Read Todos**: Send a GET request to `/todos` to retrieve a list of tasks. You can specify the `limit` and `offset` as query parameters for pagination.
- **Read a Single Todo**: Send a GET request to `/todo/<todo_id>` to retrieve a single task by its ID.
- **Update a Todo**: Send a PUT request to `/todo/<todo_id>` with a JSON payload containing `title` and/or `completed` to update a task.
- **Delete a Todo**: Send a DELETE request to `/todo/<todo_id>` to delete a task by its ID.
- **Get Users**: Send a GET request to `/users` to retrieve a list of registered users. You can specify the `limit` and `offset` as query parameters for pagination.

For more details on the API endpoints and their usage, refer to the code and documentation in the project's files.
