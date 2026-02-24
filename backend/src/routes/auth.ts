import { Router } from 'express';
import { body } from 'express-validator';
import { signup, login, getMe } from '../controllers/authController';
import { validateRequest } from '../middleware/validateRequest';
import authMiddleware from '../middleware/auth';

const router = Router();

router.post(
  '/signup',
  [
    body('name').isString().isLength({ min: 2 }),
    body('email').isEmail(),
    body('password').isLength({ min: 8 })
  ],
  validateRequest,
  signup
);

router.post(
  '/login',
  [
    body('email').isEmail(),
    body('password').isLength({ min: 8 })
  ],
  validateRequest,
  login
);

router.get('/me', authMiddleware, getMe);

export default router;
