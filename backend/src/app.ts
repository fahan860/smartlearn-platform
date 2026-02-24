import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import morgan from 'morgan';
import authRouter from './routes/auth';
import coursesRouter from './routes/courses';
import enrollmentsRouter from './routes/enrollments';
import interactionsRouter from './routes/interactions';
import recommendationsRouter from './routes/recommendations';
import { errorHandler, notFoundHandler } from './middleware/errorHandler';

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '1mb' }));
app.use(morgan('tiny'));

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use(limiter);

app.use('/api/auth', authRouter);
app.use('/api/courses', coursesRouter);
app.use('/api/enrollments', enrollmentsRouter);
app.use('/api/interactions', interactionsRouter);
app.use('/api/recommendations', recommendationsRouter);

app.get('/health', (req, res) => res.json({ status: 'ok' }));
app.get('/', (req, res) => {
  res.json({
    status: 'OK',
    message: 'Backend SmartLearn is running 🚀'
  });
});

app.use(notFoundHandler);
app.use(errorHandler);

export default app;
