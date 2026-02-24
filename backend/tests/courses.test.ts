import request from 'supertest';
import mongoose from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';
import app from '../src/app';
import Course from '../src/models/Course';

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
  await Course.deleteMany({}).exec();
});

describe('GET /api/courses', () => {
  it('returns courses list', async () => {
    await Course.create([
      {
        title: 'Intro to TypeScript',
        description: 'Learn TypeScript fundamentals and typing patterns.',
        tags: ['typescript', 'backend'],
        level: 'beginner',
        durationMinutes: 120
      },
      {
        title: 'Advanced Node.js',
        description: 'Deep dive into Node.js internals and performance tuning.',
        tags: ['node', 'performance'],
        level: 'advanced',
        durationMinutes: 180
      }
    ]);

    const response = await request(app).get('/api/courses').expect(200);

    expect(Array.isArray(response.body)).toBe(true);
    expect(response.body).toHaveLength(2);
    expect(response.body.map((course: { title: string }) => course.title)).toEqual(
      expect.arrayContaining(['Intro to TypeScript', 'Advanced Node.js'])
    );
  });

  it('filters by level', async () => {
    await Course.create([
      {
        title: 'Backend Foundations',
        description: 'Solid backend basics for beginners.',
        tags: ['backend'],
        level: 'beginner'
      },
      {
        title: 'Distributed Systems',
        description: 'Reliable architecture at scale.',
        tags: ['systems'],
        level: 'advanced'
      }
    ]);

    const response = await request(app)
      .get('/api/courses')
      .query({ level: 'advanced' })
      .expect(200);

    expect(response.body).toHaveLength(1);
    expect(response.body[0].title).toBe('Distributed Systems');
    expect(response.body[0].level).toBe('advanced');
  });
});
