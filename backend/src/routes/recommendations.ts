import { Router } from 'express';
import { recommend } from '../controllers/recommendController';
import authMiddleware from '../middleware/auth';

const router = Router();

router.get('/', authMiddleware, recommend);

export default router;
