import os
import logging
import pytest

from common.query_engine.datafustion import DataFusionEngine
from common.query_engine.postgresql import PostgresEngine


# Configure logging
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def datafusion_engine():
    file_path = "datacreator/students_data.parquet"
    return DataFusionEngine("students", file_path)


@pytest.fixture(scope="module")
def postgres_engine():
    db_name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    return PostgresEngine(db_name, user, password, host, port)


############## test datafustion ##############

def test_datafusion_sync_query(datafusion_engine):
    result = datafusion_engine.execute_read_query_sync(
        "SELECT COUNT(*) as total FROM students")
    assert result == [{'total': 1000000}]


############## test postgresql ##############

def test_postgresql_sync_query(postgres_engine):
    result = postgres_engine.execute_read_query_sync(
        "SELECT COUNT(*) as total FROM students")
    assert result == [{'total': 1000000}]

@pytest.mark.asyncio
async def test_postgresql_async_query(postgres_engine):
    result = await postgres_engine.execute_read_query_async("SELECT 1")
    assert result == [{'?column?': 1}]


@pytest.mark.asyncio
async def test_setup_db(postgres_engine, datafusion_engine):
    ddl_query = """
        DROP TABLE IF EXISTS students;

        CREATE TABLE students (
            student_id INTEGER PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            gender VARCHAR(32),
            dob DATE,
            enrollment_year INTEGER,
            major VARCHAR(255),
            gpa NUMERIC(3, 2),
            country VARCHAR(255),
            is_active BOOLEAN
        );
    """
    assert await postgres_engine.execute_write_query_async(ddl_query)

    insert_query = """
        INSERT INTO students (
            student_id, full_name, email, gender, dob,
            enrollment_year, major, gpa, country, is_active
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """

    offset = 0
    limit = 1_000

    while True:
        student_dataset = datafusion_engine.execute_read_query_sync(
            f"SELECT * FROM students OFFSET {offset} LIMIT {limit}"
        )

        if not student_dataset:
            break

        values = [
            (
                row["student_id"],
                row["full_name"],
                row["email"],
                row["gender"],
                row["dob"],
                row["enrollment_year"],
                row["major"],
                row["gpa"],
                row["country"],
                row["is_active"],
            )
            for row in student_dataset
        ]

        status = await postgres_engine.execute_write_query_async(insert_query, values)
        logger.info(f"data insertion {status} {offset}")
        offset += limit

    total_records = await postgres_engine.execute_read_query_async(
        "SELECT COUNT(*) as total FROM students"
    )
    logger.info(f"data insertion completed {total_records}")