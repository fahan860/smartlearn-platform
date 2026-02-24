import request from 'supertest';
import jwt from 'jsonwebtoken';
import mongoose from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';
import app from '../src/app';
import User from '../src/models/User';
import { config } from '../src/config';
import { generateRecommendations } from '../src/services/recommendationService';

jest.mock('../src/services/recommendationService', () => ({
  generateRecommendations: jest.fn()
}));

const mockedGenerateRecommendations = generateRecommendations as jest.MockedFunction<typeof generateRecommendations>;

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
  mockedGenerateRecommendations.mockReset();
  await User.deleteMany({}).exec();
});

function signToken(userId: string, email: string): string {
  return jwt.sign({ sub: userId, email }, config.jwtSecret, { expiresIn: '1h' });
}

describe('GET /api/recommendations', () => {
  it('requires authentication', async () => {
    await request(app).get('/api/recommendations').expect(401);
  });

  it('returns recommendations from ML service layer', async () => {
    const user = await User.create({
      name: 'Reco Tester',
      email: 'reco@test.com',
      passwordHash: 'hash'
    });

    const token = signToken(String(user._id), user.email);

    mockedGenerateRecommendations.mockResolvedValue([
      {
        _id: new mongoose.Types.ObjectId(),
        title: 'System Design for Backend Engineers',
        description: 'Scalable architecture, resilience patterns, and trade-offs.',
        tags: ['architecture', 'backend'],
        level: 'advanced',
        createdAt: new Date()
      } as any
    ]);

    const response = await request(app)
      .get('/api/recommendations')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);

    expect(mockedGenerateRecommendations).toHaveBeenCalledTimes(1);
    expect(mockedGenerateRecommendations).toHaveBeenCalledWith(String(user._id));
    expect(Array.isArray(response.body.recommendations)).toBe(true);
    expect(response.body.recommendations).toHaveLength(1);
    expect(response.body.recommendations[0].title).toBe('System Design for Backend Engineers');
  });
});
