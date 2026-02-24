import request from 'supertest';
import mongoose from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';
import app from '../src/app';
import User from '../src/models/User';

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
  await User.deleteMany({}).exec();
});

test('signup and login flow', async () => {
  const signupRes = await request(app)
    .post('/api/auth/signup')
    .send({ name: 'Test', email: 'test@example.com', password: 'Password123!' })
    .expect(201);

  expect(signupRes.body.token).toBeTruthy();

  const loginRes = await request(app)
    .post('/api/auth/login')
    .send({ email: 'test@example.com', password: 'Password123!' })
    .expect(200);

  expect(loginRes.body.token).toBeTruthy();
});
