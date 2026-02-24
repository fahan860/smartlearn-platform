-- ===========================================================================
-- SmartLearn - Canonical Operational MySQL Schema
-- Entities aligned with backend domain: users, courses, enrollments, interactions
-- Interaction vocabulary: view, enroll, complete
-- ===========================================================================

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS interactions;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE IF NOT EXISTS users (
	id VARCHAR(50) PRIMARY KEY,
	name VARCHAR(120) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	password_hash VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	INDEX idx_users_email (email),
	INDEX idx_users_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS courses (
	id VARCHAR(50) PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	level ENUM('beginner', 'intermediate', 'advanced') NOT NULL DEFAULT 'beginner',
	tags_json JSON NULL,
	duration_minutes INT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	INDEX idx_courses_level (level),
	FULLTEXT INDEX ftx_courses_text (title, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS enrollments (
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	user_id VARCHAR(50) NOT NULL,
	course_id VARCHAR(50) NOT NULL,
	status ENUM('enrolled', 'completed') NOT NULL DEFAULT 'enrolled',
	enrolled_at TIMESTAMP NOT NULL,
	completed_at TIMESTAMP NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	UNIQUE KEY uq_enrollments_user_course (user_id, course_id),
	INDEX idx_enrollments_user (user_id),
	INDEX idx_enrollments_course (course_id),
	INDEX idx_enrollments_status (status),
	CONSTRAINT fk_enrollments_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	CONSTRAINT fk_enrollments_course FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS interactions (
	id VARCHAR(50) PRIMARY KEY,
	user_id VARCHAR(50) NOT NULL,
	course_id VARCHAR(50) NOT NULL,
	interaction_type ENUM('view', 'enroll', 'complete') NOT NULL,
	metadata_json JSON NULL,
	interaction_timestamp TIMESTAMP NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	INDEX idx_interactions_user (user_id),
	INDEX idx_interactions_course (course_id),
	INDEX idx_interactions_type (interaction_type),
	INDEX idx_interactions_timestamp (interaction_timestamp),
	CONSTRAINT fk_interactions_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	CONSTRAINT fk_interactions_course FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

