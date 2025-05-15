
🎓 Academic-Assignment-Management-Backend-Service

This is a backend service for a classroom for managing 
a simple academic system involving Students, Teachers, Assignments, and a Principal. 
The API supports creation, submission, grading, and listing of assignments, with role-based access for each entity.


🚀 Features
✅ Student can:

Create and edit draft assignments

Submit assignments to teachers

View their assignments

✅ Teacher can:

View submitted assignments

Grade assignments assigned to them

✅ Principal can:

View all teachers

View all submitted or graded assignments

Re-grade assignments already graded by teachers

✅ Administered using Flask, SQLAlchemy, Alembic, and SQLite

⚙️ Setup Instructions
### Clone the Repository

```commandline
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

```

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```

### SQL Assignment
Two SQL files to be implemented:

tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql

tests/SQL/count_assignments_in_each_grade.sql

Run tests for these using:
```
pytest tests/SQL/sql_test.py
```

🏗️ Project Structure

Academic-Assignment-Management-Backend-Service/
│
├── core/                       # Core application logic
│   ├── apis/                   # API routes and handlers
│   ├── models/                 # Database models
│   ├── migrations/             # Alembic DB migration files
│   └── server.py               # Flask entry point
│
├── tests/                      # Unit & SQL tests
│
├── requirements.txt            # Python dependencies
├── run.sh                      # Script to start the server
├── README.md                   # Project documentation
└── docker-compose.yml (optional)

🛠 Tech Stack
💻 Backend
Python 3.13

Flask – Lightweight WSGI web application framework

SQLAlchemy – ORM for database operations

Alembic – For database migrations

🧪 Testing & Coverage
pytest – Testing framework

pytest-cov – Code coverage plugin

SQLite – Lightweight embedded database for local development

Postman – For testing REST APIs

📦 Package & Environment Management
virtualenv – For isolated Python environments

pip – Python package installer

🐳 Optional (Docker Support)
Docker

docker-compose

👨‍💻 Author
Sujit Prakash Tadadikar

