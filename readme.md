# Analytics Engine PoC: FastAPI vs Flask

This proof-of-concept compares performance and integration between **Flask** and **FastAPI** using two different backends:

* **Apache DataFusion** (in-process SQL engine over Parquet)
* **PostgreSQL** (traditional RDBMS)

---

## 🔧 Run Locally

### 1. Create and Activate Virtual Environment

```
virtualenv --python=$(which python3.10) .venv
source .venv/bin/activate
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Create `.env` File and Export Variables

Create a `.env` file with the following content:

```
export DB_NAME="test"
export DB_USER="admin"
export DB_PASSWORD="admin"
export DB_HOST="localhost"
export DB_PORT="5432"
```

Then load the environment variables:

```
source .env
```

---

### 4. Start PostgreSQL

You can either:

* Run a local PostgreSQL instance manually, or
* Use Docker (see Docker section below)

---

### 5. Seed Dummy Data to Database

```
pytest tests/test_query_engine.py -s -k test_setup_db
```

---

### 6. Run FastAPI App Locally

```
PYTHONPATH=. uvicorn fastapi_app.app:app --reload
```

---

### 7. Run Flask App Locally

```
PYTHONPATH=. python flask_app/app.py
```

---

## 🐳 Run with Docker Compose

### 1. Build and Run the Stack in Detached Mode

```
docker compose up --build -d
```

---

* Flask app is exposed on `http://localhost:3000`
* Fast api is exposed on `http://localhost:3001`
* PostgreSQL runs inside the `analytics_db` container

---


## For load test used apache benchmark
ab -n 10000 -c 200 -l http://localhost:3001/datafusion
