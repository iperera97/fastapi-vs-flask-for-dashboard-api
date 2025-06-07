import csv
import random
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker

fake = Faker()

CSV_FILE = "students_data.csv"
PARQUET_FILE = "students_data.parquet"
NUM_RECORDS = 1_000_000
FIELDS = [
    "student_id", "full_name", "email", "gender", "dob", "enrollment_year",
    "major", "gpa", "country", "is_active"
]

majors = [
    "Computer Science", "Business", "Psychology", "Engineering",
    "Biology", "Education", "Mathematics", "Economics"
]

genders = ["Male", "Female", "Non-binary", "Other"]

def generate_row(index):
    return {
        "student_id": f"{100000 + index}",
        "full_name": fake.name(),
        "email": fake.email(),
        "gender": random.choice(genders),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=30).isoformat(),
        "enrollment_year": random.randint(2015, 2024),
        "major": random.choice(majors),
        "gpa": round(random.uniform(2.0, 4.0), 2),
        "country": fake.country(),
        "is_active": random.choice([True, False]),
    }

def write_csv():
    with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for i in range(NUM_RECORDS):
            if i % 10000 == 0:
                print(f"Generated {i} records...")
            writer.writerow(generate_row(i))
    print(f"✅ Done! Wrote {NUM_RECORDS} records to {CSV_FILE}")

def convert_csv_to_parquet():
    print("🔄 Converting CSV to Parquet...")
    df = pd.read_csv(CSV_FILE)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, PARQUET_FILE)
    print(f"✅ Saved Parquet file: {PARQUET_FILE}")

if __name__ == "__main__":
    write_csv()
    convert_csv_to_parquet()
