import { Router } from 'express';
import { body } from 'express-validator';
import authMiddleware from '../middleware/auth';
import { validateRequest } from '../middleware/validateRequest';
import { createEnrollment } from '../controllers/enrollmentController';

const router = Router();

router.post(
  '/',
  authMiddleware,
  [
    body('courseId').isString().notEmpty(),
    body('metadata').optional().isObject()
  ],
  validateRequest,
  createEnrollment
);

export default router;
