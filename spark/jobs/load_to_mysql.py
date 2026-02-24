"""
Load canonical processed CSV files into MySQL operational tables:
- users
- courses
- enrollments
- interactions
"""

import glob
import os
import sys
from datetime import datetime

import mysql.connector
import pandas as pd
from mysql.connector import Error


class MySQLLoader:
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "", database: str = "smartlearn"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                return True
        except Error as error:
            print(f"❌ MySQL connection failed: {error}")
        return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def find_csv(self, directory: str) -> str:
        files = glob.glob(os.path.join(directory, "*.csv"))
        if not files:
            files = glob.glob(os.path.join(directory, "*", "*.csv"))
        if not files:
            raise FileNotFoundError(f"No CSV file in {directory}")
        return max(files, key=os.path.getctime)

    def clear_tables(self):
        for table in ["interactions", "enrollments", "courses", "users"]:
            self.cursor.execute(f"DELETE FROM {table}")
        self.connection.commit()

    def load_users(self, csv_dir: str) -> int:
        df = pd.read_csv(self.find_csv(csv_dir))

        query = """
            INSERT INTO users (id, name, email, password_hash, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email = VALUES(email),
                password_hash = VALUES(password_hash),
                created_at = VALUES(created_at)
        """

        rows = [
            (
                row["id"],
                row["name"],
                row["email"],
                row["password_hash"],
                row["created_at"],
            )
            for _, row in df.iterrows()
        ]

        self.cursor.executemany(query, rows)
        self.connection.commit()
        return len(rows)

    def load_courses(self, csv_dir: str) -> int:
        df = pd.read_csv(self.find_csv(csv_dir))

        query = """
            INSERT INTO courses (id, title, description, level, tags_json, duration_minutes, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                description = VALUES(description),
                level = VALUES(level),
                tags_json = VALUES(tags_json),
                duration_minutes = VALUES(duration_minutes),
                created_at = VALUES(created_at)
        """

        rows = [
            (
                row["id"],
                row["title"],
                row["description"],
                row["level"],
                row["tags_json"] if pd.notna(row["tags_json"]) else None,
                int(row["duration_minutes"]) if pd.notna(row["duration_minutes"]) else None,
                row["created_at"],
            )
            for _, row in df.iterrows()
        ]

        self.cursor.executemany(query, rows)
        self.connection.commit()
        return len(rows)

    def load_enrollments(self, csv_dir: str) -> int:
        df = pd.read_csv(self.find_csv(csv_dir))

        query = """
            INSERT INTO enrollments (user_id, course_id, status, enrolled_at, completed_at, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                status = VALUES(status),
                enrolled_at = VALUES(enrolled_at),
                completed_at = VALUES(completed_at),
                created_at = VALUES(created_at)
        """

        rows = [
            (
                row["user_id"],
                row["course_id"],
                row["status"],
                row["enrolled_at"],
                row["completed_at"] if pd.notna(row["completed_at"]) else None,
                row["created_at"],
            )
            for _, row in df.iterrows()
        ]

        self.cursor.executemany(query, rows)
        self.connection.commit()
        return len(rows)

    def load_interactions(self, csv_dir: str) -> int:
        df = pd.read_csv(self.find_csv(csv_dir))
        df = df[df["interaction_type"].isin(["view", "enroll", "complete"])]

        query = """
            INSERT INTO interactions (id, user_id, course_id, interaction_type, metadata_json, interaction_timestamp, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                user_id = VALUES(user_id),
                course_id = VALUES(course_id),
                interaction_type = VALUES(interaction_type),
                metadata_json = VALUES(metadata_json),
                interaction_timestamp = VALUES(interaction_timestamp),
                created_at = VALUES(created_at)
        """

        rows = [
            (
                row["id"],
                row["user_id"],
                row["course_id"],
                row["interaction_type"],
                row["metadata_json"] if pd.notna(row["metadata_json"]) else None,
                row["interaction_timestamp"],
                row["created_at"],
            )
            for _, row in df.iterrows()
        ]

        self.cursor.executemany(query, rows)
        self.connection.commit()
        return len(rows)

    def verify(self):
        for table in ["users", "courses", "enrollments", "interactions"]:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"✓ {table}: {count}")

    def run(self, data_path: str = "data/processed", clear: bool = False) -> bool:
        if not self.connect():
            return False

        started = datetime.now()

        try:
            if clear:
                self.clear_tables()

            stats = {
                "users": self.load_users(f"{data_path}/users"),
                "courses": self.load_courses(f"{data_path}/courses"),
                "enrollments": self.load_enrollments(f"{data_path}/enrollments"),
                "interactions": self.load_interactions(f"{data_path}/interactions"),
            }

            self.verify()

            elapsed = (datetime.now() - started).total_seconds()
            print("=" * 80)
            print("✅ MYSQL LOAD COMPLETED")
            print("=" * 80)
            print(f"Duration: {elapsed:.2f}s")
            for key, value in stats.items():
                print(f"{key}: {value}")
            print("=" * 80)
            return True
        except Exception as error:
            print(f"❌ Load failed: {error}")
            self.connection.rollback()
            return False
        finally:
            self.disconnect()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load canonical processed data into MySQL")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--user", default="root")
    parser.add_argument("--password", default="")
    parser.add_argument("--database", default="smartlearn")
    parser.add_argument("--data-path", default="data/processed")
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    loader = MySQLLoader(
        host=args.host,
        user=args.user,
        password=args.password,
        database=args.database,
    )

    ok = loader.run(data_path=args.data_path, clear=args.clear)
    sys.exit(0 if ok else 1)
