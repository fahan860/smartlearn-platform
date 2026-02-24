import mongoose from 'mongoose';
import bcrypt from 'bcrypt';
import User from '../models/User';
import Course from '../models/Course';
import LearningPath from '../models/LearningPath';
import { config } from '../config';

async function seed() {
  await mongoose.connect(config.mongoUri);
  console.log('Connected to DB');

  // clear small demo datasets
  await User.deleteMany({}).exec();
  await Course.deleteMany({}).exec();
  await LearningPath.deleteMany({}).exec();

  const passwordHash = await bcrypt.hash('Password123!', 12);
  const demoUser = new User({ name: 'Demo User', email: 'demo@example.com', passwordHash });
  await demoUser.save();

  const courses = [
    { title: 'Intro to Python', description: 'Learn Python basics', tags: ['python', 'programming'], level: 'beginner', durationMinutes: 180 },
    { title: 'Data Structures in Python', description: 'Intermediate DS using Python', tags: ['python', 'data-structures'], level: 'intermediate', durationMinutes: 240 },
    { title: 'Machine Learning Basics', description: 'Intro to ML concepts and workflows', tags: ['ml', 'data-science'], level: 'beginner', durationMinutes: 300 }
  ];

  const created = [] as any[];
  for (const c of courses) {
    const course = new Course(c);
    await course.save();
    created.push(course);
  }

  const lp = new LearningPath({ title: 'Data Science Path', description: 'Path to learn data science', courses: created.map((c) => c._id), tags: ['data-science'] });
  await lp.save();

  console.log('Seed complete');
  await mongoose.disconnect();
}

seed().catch((err) => {
  console.error(err);
  process.exit(1);
});
