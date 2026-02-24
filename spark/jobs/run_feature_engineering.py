"""
Canonical entity preparation (Pandas fallback)
Outputs CSV files for MySQL tables: users, courses, enrollments, interactions
"""

import glob
import json
import os
from datetime import datetime

import pandas as pd


def latest_file(directory: str, pattern: str) -> str:
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        raise FileNotFoundError(f"No file found: {directory}/{pattern}")
    return max(files, key=os.path.getctime)


def load_raw(data_path: str = "data/raw"):
    users = pd.read_csv(latest_file(f"{data_path}/users", "users_*.csv"))
    courses = pd.read_csv(latest_file(f"{data_path}/courses", "courses_*.csv"))
    interactions = pd.read_csv(latest_file(f"{data_path}/interactions", "interactions_*.csv"))
    return users, courses, interactions


def normalize_users(users: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["id"] = users["_id"]
    df["name"] = (users["profile.firstName"].fillna("") + " " + users["profile.lastName"].fillna("")).str.strip()
    df["email"] = users["email"]
    df["password_hash"] = users["password"]
    df["created_at"] = pd.to_datetime(users["createdAt"], errors="coerce")
    return df


def normalize_courses(courses: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["id"] = courses["_id"]
    df["title"] = courses["title"]
    df["description"] = courses["description"]
    df["level"] = courses["level"].fillna("beginner")

    def to_json_array(raw):
        if pd.isna(raw):
            return None
        try:
            value = json.loads(raw) if isinstance(raw, str) else raw
            return json.dumps(value)
        except Exception:
            return json.dumps([str(raw)])

    df["tags_json"] = courses["tags"].apply(to_json_array) if "tags" in courses.columns else None
    df["duration_minutes"] = pd.to_numeric(courses.get("content.duration"), errors="coerce")
    df["created_at"] = pd.to_datetime(courses["createdAt"], errors="coerce")
    return df


def normalize_interactions(interactions: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["id"] = interactions["_id"]
    df["user_id"] = interactions["userId"]
    df["course_id"] = interactions["courseId"]
    df["interaction_type"] = interactions["type"].replace({"enrollment": "enroll", "completion": "complete"})
    df = df[df["interaction_type"].isin(["view", "enroll", "complete"])].copy()
    df["metadata_json"] = None
    df["interaction_timestamp"] = pd.to_datetime(interactions["timestamp"], errors="coerce")
    df["created_at"] = df["interaction_timestamp"]
    return df


def build_enrollments(interactions: pd.DataFrame) -> pd.DataFrame:
    enroll_df = interactions[interactions["interaction_type"].isin(["enroll", "complete"])].copy()

    enrolled_at = (
        enroll_df.groupby(["user_id", "course_id"], as_index=False)["interaction_timestamp"]
        .min()
        .rename(columns={"interaction_timestamp": "enrolled_at"})
    )
    completed_at = (
        enroll_df[enroll_df["interaction_type"] == "complete"]
        .groupby(["user_id", "course_id"], as_index=False)["interaction_timestamp"]
        .max()
        .rename(columns={"interaction_timestamp": "completed_at"})
    )

    grouped = enrolled_at.merge(completed_at, on=["user_id", "course_id"], how="left")

    grouped["status"] = grouped["completed_at"].apply(lambda v: "completed" if pd.notna(v) else "enrolled")
    grouped["created_at"] = grouped["enrolled_at"]
    return grouped[["user_id", "course_id", "status", "enrolled_at", "completed_at", "created_at"]]


def save_outputs(users: pd.DataFrame, courses: pd.DataFrame, enrollments: pd.DataFrame, interactions: pd.DataFrame, output_path: str = "data/processed"):
    os.makedirs(output_path, exist_ok=True)

    for folder, df in {
        "users": users,
        "courses": courses,
        "enrollments": enrollments,
        "interactions": interactions,
    }.items():
        folder_path = os.path.join(output_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        df.to_csv(os.path.join(folder_path, "part-00000.csv"), index=False)


def main():
    started = datetime.now()

    users_raw, courses_raw, interactions_raw = load_raw()
    users = normalize_users(users_raw)
    courses = normalize_courses(courses_raw)
    interactions = normalize_interactions(interactions_raw)
    enrollments = build_enrollments(interactions)

    save_outputs(users, courses, enrollments, interactions)

    elapsed = (datetime.now() - started).total_seconds()
    print("=" * 80)
    print("✅ CANONICAL PANDAS ENTITY PREPARATION COMPLETED")
    print("=" * 80)
    print(f"Duration: {elapsed:.2f}s")
    print(f"Users: {len(users)}")
    print(f"Courses: {len(courses)}")
    print(f"Enrollments: {len(enrollments)}")
    print(f"Interactions: {len(interactions)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
