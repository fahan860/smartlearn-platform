import request from 'supertest';
import mongoose from 'mongoose';
import jwt from 'jsonwebtoken';
import { MongoMemoryServer } from 'mongodb-memory-server';
import app from '../src/app';
import User from '../src/models/User';
import Course from '../src/models/Course';
import Interaction from '../src/models/Interaction';
import { config } from '../src/config';

let mongo: MongoMemoryServer;

beforeAll(async () => {
  mongo = await MongoMemoryServer.create();
  await mongoose.connect(mongo.getUri());
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongo.stop();
});

beforeEach(async () => {
  await Promise.all([
    User.deleteMany({}).exec(),
    Course.deleteMany({}).exec(),
    Interaction.deleteMany({}).exec()
  ]);
});

function signToken(userId: string, email: string): string {
  return jwt.sign({ sub: userId, email }, config.jwtSecret, { expiresIn: '1h' });
}

describe('POST /api/enrollments', () => {
  it('requires authentication', async () => {
    const course = await Course.create({
      title: 'ML Ops Essentials',
      description: 'Operational best practices for machine learning systems.',
      tags: ['mlops'],
      level: 'intermediate'
    });

    await request(app)
      .post('/api/enrollments')
      .send({ courseId: String(course._id) })
      .expect(401);
  });

  it('creates enrollment interaction and is idempotent', async () => {
    const user = await User.create({
      name: 'Enroll Tester',
      email: 'enroll@test.com',
      passwordHash: 'hash'
    });

    const course = await Course.create({
      title: 'API Design',
      description: 'Design robust and maintainable backend APIs.',
      tags: ['api', 'backend'],
      level: 'beginner'
    });

    const token = signToken(String(user._id), user.email);

    const first = await request(app)
      .post('/api/enrollments')
      .set('Authorization', `Bearer ${token}`)
      .send({ courseId: String(course._id), metadata: { source: 'test-suite' } })
      .expect(201);

    expect(first.body.enrollment).toBeDefined();
    expect(first.body.enrollment.action).toBe('enroll');

    const second = await request(app)
      .post('/api/enrollments')
      .set('Authorization', `Bearer ${token}`)
      .send({ courseId: String(course._id) })
      .expect(200);

    expect(second.body.enrollment).toBeDefined();
    expect(second.body.enrollment.action).toBe('enroll');

    const enrollments = await Interaction.find({
      user: user._id,
      course: course._id,
      action: 'enroll'
    }).exec();

    expect(enrollments).toHaveLength(1);
  });
});
