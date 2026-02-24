# Docker Usage in the Smart Learning Platform

## Why Docker?

Docker is used to provide a consistent, isolated, and reproducible environment
for all backend services and databases used in the project.

Without Docker, installing and configuring services like MySQL, MongoDB, or
Apache Spark directly on the host machine can lead to:
- Version conflicts
- Port collisions
- Environment-specific bugs
- Difficult setup for new developers or reviewers

## Role of Docker in this project

Each major component runs in its own container:

- MySQL: relational database for users, courses, and enrollments
- MongoDB: storage for user interactions and events
- (Future) Apache Spark: offline data processing and machine learning
- (Optional) Backend API container

This approach allows:
- Easy setup with minimal system dependencies
- Clean separation of services
- Production-like architecture

## Benefits

- Reproducibility across machines
- Easy teardown and reset of services
- Clear service boundaries
- Industry-standard DevOps practice

Docker is used only for infrastructure and does not affect application logic.
