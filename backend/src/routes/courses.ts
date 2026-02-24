import { Router } from 'express';
import { body } from 'express-validator';
import { createCourse, listCourses, getCourse } from '../controllers/courseController';
import authMiddleware from '../middleware/auth';
import { validateRequest } from '../middleware/validateRequest';
import { getCoursesFromMySQL } from '../controllers/courseController';


const router = Router();

router.get('/mysql', getCoursesFromMySQL);
router.get('/', listCourses);
router.get('/:id', getCourse);

router.post(
  '/',
  authMiddleware,
  [
    body('title').isString().isLength({ min: 3 }),
    body('description').isString().isLength({ min: 10 }),
    body('tags').optional().isArray({ min: 1 }),
    body('level').optional().isIn(['beginner', 'intermediate', 'advanced']),
    body('durationMinutes').optional().isNumeric()
  ],
  validateRequest,
  createCourse
);

export default router;
