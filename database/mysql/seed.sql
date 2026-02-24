-- ===========================================================================
-- SmartLearn - Canonical Operational Seed Data
-- Tables: users, courses, enrollments, interactions
-- Interaction vocabulary: view, enroll, complete
-- ===========================================================================

START TRANSACTION;

DELETE FROM interactions;
DELETE FROM enrollments;
DELETE FROM courses;
DELETE FROM users;

INSERT INTO users (id, name, email, password_hash, created_at) VALUES
('user_00001', 'Alice Martin', 'alice@example.com', '$2b$10$examplehashalice', DATE_SUB(NOW(), INTERVAL 30 DAY)),
('user_00002', 'Bob Leroy', 'bob@example.com', '$2b$10$examplehashbob', DATE_SUB(NOW(), INTERVAL 20 DAY)),
('user_00003', 'Chloe Bernard', 'chloe@example.com', '$2b$10$examplehashchloe', DATE_SUB(NOW(), INTERVAL 12 DAY));

INSERT INTO courses (id, title, description, level, tags_json, duration_minutes, created_at) VALUES
(
  'course_00001',
  'Intro to Python',
  'Learn Python fundamentals with hands-on exercises.',
  'beginner',
  JSON_ARRAY('python', 'programming', 'basics'),
  180,
  DATE_SUB(NOW(), INTERVAL 40 DAY)
),
(
  'course_00002',
  'Data Structures in Python',
  'Understand lists, dicts, trees and algorithmic problem solving.',
  'intermediate',
  JSON_ARRAY('python', 'data-structures'),
  240,
  DATE_SUB(NOW(), INTERVAL 35 DAY)
),
(
  'course_00003',
  'Machine Learning Foundations',
  'Core ML concepts, workflows and model evaluation.',
  'intermediate',
  JSON_ARRAY('ml', 'data-science', 'modeling'),
  300,
  DATE_SUB(NOW(), INTERVAL 25 DAY)
);

INSERT INTO enrollments (user_id, course_id, status, enrolled_at, completed_at, created_at) VALUES
('user_00001', 'course_00001', 'completed', DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_SUB(NOW(), INTERVAL 10 DAY)),
('user_00001', 'course_00002', 'enrolled', DATE_SUB(NOW(), INTERVAL 2 DAY), NULL, DATE_SUB(NOW(), INTERVAL 2 DAY)),
('user_00002', 'course_00001', 'enrolled', DATE_SUB(NOW(), INTERVAL 6 DAY), NULL, DATE_SUB(NOW(), INTERVAL 6 DAY)),
('user_00002', 'course_00003', 'completed', DATE_SUB(NOW(), INTERVAL 9 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 9 DAY)),
('user_00003', 'course_00003', 'enrolled', DATE_SUB(NOW(), INTERVAL 4 DAY), NULL, DATE_SUB(NOW(), INTERVAL 4 DAY));

INSERT INTO interactions (id, user_id, course_id, interaction_type, metadata_json, interaction_timestamp, created_at) VALUES
('interaction_000001', 'user_00001', 'course_00001', 'view', JSON_OBJECT('source', 'catalog'), DATE_SUB(NOW(), INTERVAL 12 DAY), DATE_SUB(NOW(), INTERVAL 12 DAY)),
('interaction_000002', 'user_00001', 'course_00001', 'enroll', JSON_OBJECT('source', 'course_detail'), DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_SUB(NOW(), INTERVAL 10 DAY)),
('interaction_000003', 'user_00001', 'course_00001', 'complete', JSON_OBJECT('finalGrade', 91), DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_SUB(NOW(), INTERVAL 3 DAY)),
('interaction_000004', 'user_00001', 'course_00002', 'view', JSON_OBJECT('source', 'recommendation'), DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 2 DAY)),
('interaction_000005', 'user_00001', 'course_00002', 'enroll', JSON_OBJECT('source', 'course_detail'), DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 2 DAY)),
('interaction_000006', 'user_00002', 'course_00001', 'view', JSON_OBJECT('source', 'search'), DATE_SUB(NOW(), INTERVAL 7 DAY), DATE_SUB(NOW(), INTERVAL 7 DAY)),
('interaction_000007', 'user_00002', 'course_00001', 'enroll', JSON_OBJECT('source', 'course_detail'), DATE_SUB(NOW(), INTERVAL 6 DAY), DATE_SUB(NOW(), INTERVAL 6 DAY)),
('interaction_000008', 'user_00002', 'course_00003', 'view', JSON_OBJECT('source', 'catalog'), DATE_SUB(NOW(), INTERVAL 11 DAY), DATE_SUB(NOW(), INTERVAL 11 DAY)),
('interaction_000009', 'user_00002', 'course_00003', 'enroll', JSON_OBJECT('source', 'course_detail'), DATE_SUB(NOW(), INTERVAL 9 DAY), DATE_SUB(NOW(), INTERVAL 9 DAY)),
('interaction_000010', 'user_00002', 'course_00003', 'complete', JSON_OBJECT('finalGrade', 88), DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY)),
('interaction_000011', 'user_00003', 'course_00003', 'view', JSON_OBJECT('source', 'catalog'), DATE_SUB(NOW(), INTERVAL 5 DAY), DATE_SUB(NOW(), INTERVAL 5 DAY)),
('interaction_000012', 'user_00003', 'course_00003', 'enroll', JSON_OBJECT('source', 'course_detail'), DATE_SUB(NOW(), INTERVAL 4 DAY), DATE_SUB(NOW(), INTERVAL 4 DAY));

COMMIT;
