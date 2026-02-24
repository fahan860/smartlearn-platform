"""
Spark Job: Canonical Entity Preparation
Builds normalized CSV datasets for MySQL operational tables:
- users
- courses
- enrollments
- interactions
"""

from datetime import datetime
import glob
import os
import sys

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col,
    concat_ws,
    coalesce,
    current_timestamp,
    date_format,
    from_json,
    lit,
    min as spark_min,
    max as spark_max,
    to_json,
    to_timestamp,
    when,
)
from pyspark.sql.types import ArrayType, StringType


class CanonicalEntityJob:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.users_df = None
        self.courses_df = None
        self.interactions_df = None

    def _find_latest_file(self, directory: str, pattern: str) -> str:
        files = glob.glob(os.path.join(directory, pattern))
        if not files:
            raise FileNotFoundError(f"No file found: {directory}/{pattern}")
        return max(files, key=os.path.getctime)

    def load_data(self, data_path: str = "data/raw"):
        users_file = self._find_latest_file(f"{data_path}/users", "users_*.csv")
        courses_file = self._find_latest_file(f"{data_path}/courses", "courses_*.csv")
        interactions_file = self._find_latest_file(f"{data_path}/interactions", "interactions_*.csv")

        self.users_df = self.spark.read.csv(users_file, header=True, inferSchema=True)
        self.courses_df = self.spark.read.csv(courses_file, header=True, inferSchema=True)
        self.interactions_df = self.spark.read.csv(interactions_file, header=True, inferSchema=True)

        self.interactions_df = self.interactions_df.withColumn(
            "interaction_type",
            when(col("type") == "enrollment", lit("enroll"))
            .when(col("type") == "completion", lit("complete"))
            .otherwise(col("type")),
        )

    def build_users(self) -> DataFrame:
        users = self.users_df.select(
            col("_id").alias("id"),
            concat_ws(" ", col("profile.firstName"), col("profile.lastName")).alias("name"),
            col("email"),
            col("password").alias("password_hash"),
            to_timestamp(col("createdAt")).alias("created_at"),
        )
        return users

    def build_courses(self) -> DataFrame:
        tags_array = from_json(col("tags"), ArrayType(StringType()))
        courses = self.courses_df.select(
            col("_id").alias("id"),
            col("title"),
            col("description"),
            col("level"),
            to_json(tags_array).alias("tags_json"),
            col("content.duration").cast("int").alias("duration_minutes"),
            to_timestamp(col("createdAt")).alias("created_at"),
        )
        return courses

    def build_enrollments(self) -> DataFrame:
        enroll_candidates = self.interactions_df.filter(col("interaction_type").isin(["enroll", "complete"]))

        enrollments = (
            enroll_candidates.groupBy(col("userId").alias("user_id"), col("courseId").alias("course_id"))
            .agg(
                spark_min(to_timestamp(col("timestamp"))).alias("enrolled_at"),
                spark_max(
                    when(col("interaction_type") == "complete", to_timestamp(col("timestamp"))).otherwise(None)
                ).alias("completed_at"),
            )
            .withColumn(
                "status",
                when(col("completed_at").isNotNull(), lit("completed")).otherwise(lit("enrolled")),
            )
            .withColumn("created_at", coalesce(col("enrolled_at"), current_timestamp()))
            .select("user_id", "course_id", "status", "enrolled_at", "completed_at", "created_at")
        )

        return enrollments

    def build_interactions(self) -> DataFrame:
        interactions = (
            self.interactions_df.filter(col("interaction_type").isin(["view", "enroll", "complete"]))
            .select(
                col("_id").alias("id"),
                col("userId").alias("user_id"),
                col("courseId").alias("course_id"),
                col("interaction_type"),
                lit(None).cast("string").alias("metadata_json"),
                to_timestamp(col("timestamp")).alias("interaction_timestamp"),
                coalesce(to_timestamp(col("timestamp")), current_timestamp()).alias("created_at"),
            )
        )
        return interactions

    def save(self, df: DataFrame, output_path: str, folder: str):
        target = f"{output_path}/{folder}"
        df.coalesce(1).write.mode("overwrite").option("header", "true").csv(target)

    def run(self, data_path: str = "data/raw", output_path: str = "data/processed"):
        start = datetime.now()
        self.load_data(data_path)

        users = self.build_users()
        courses = self.build_courses()
        enrollments = self.build_enrollments()
        interactions = self.build_interactions()

        os.makedirs(output_path, exist_ok=True)
        self.save(users, output_path, "users")
        self.save(courses, output_path, "courses")
        self.save(enrollments, output_path, "enrollments")
        self.save(interactions, output_path, "interactions")

        duration = (datetime.now() - start).total_seconds()
        print("=" * 80)
        print("✅ CANONICAL ENTITY PREPARATION COMPLETED")
        print("=" * 80)
        print(f"Duration: {duration:.2f}s")
        print(f"Users: {users.count()}")
        print(f"Courses: {courses.count()}")
        print(f"Enrollments: {enrollments.count()}")
        print(f"Interactions: {interactions.count()}")
        print("=" * 80)


if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("SmartLearn-CanonicalEntities")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        CanonicalEntityJob(spark).run()
    except Exception as exc:
        print(f"❌ Entity preparation failed: {exc}")
        sys.exit(1)
    finally:
        spark.stop()
