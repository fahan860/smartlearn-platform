import { Router } from 'express';
import { body } from 'express-validator';
import { recordInteraction, getMyInteractions } from '../controllers/interactionController';
import authMiddleware from '../middleware/auth';
import { validateRequest } from '../middleware/validateRequest';

const router = Router();

router.post(
  '/record',
  authMiddleware,
  [
    body('course').isString(),
    body('action').isIn(['view', 'enroll', 'complete']),
    body('metadata').optional().isObject()
  ],
  validateRequest,
  recordInteraction
);

router.get('/me', authMiddleware, getMyInteractions);

export default router;
