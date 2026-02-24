import { Request, Response } from 'express';
import { validationResult } from 'express-validator';
import Course from '../models/Course';

export async function createCourse(req: Request, res: Response) {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

    const { title, description, tags, level, durationMinutes, prerequisites } = req.body;
    const course = new Course({ title, description, tags, level, durationMinutes, prerequisites });
    await course.save();
    res.status(201).json(course);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create course' });
  }
}

export async function listCourses(req: Request, res: Response) {
  try {
    const { tag, level, q } = req.query as any;
    const filter: any = {};
    if (tag) filter.tags = tag;
    if (level) filter.level = level;
    if (q) filter.$text = { $search: q };

    const courses = await Course.find(filter).limit(100).exec();
    res.json(courses);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to list courses' });
  }
}

export async function getCourse(req: Request, res: Response) {
  try {
    const { id } = req.params;
    const course = await Course.findById(id).exec();
    if (!course) return res.status(404).json({ error: 'Course not found' });
    res.json(course);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch course' });
  }
}
import mysqlPool from '../services/mysql.service';

export const getCoursesFromMySQL = async (req: Request, res: Response) => {
  try {
    const [rows] = await mysqlPool.query(
      `SELECT
        id,
        title,
        description,
        level
      FROM courses
      ORDER BY created_at DESC
      LIMIT 100`
    );
    res.json(rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'MySQL error' });
  }
};

