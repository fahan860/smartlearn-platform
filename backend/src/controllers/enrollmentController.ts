import { Response } from 'express';
import mongoose from 'mongoose';
import Course from '../models/Course';
import Interaction from '../models/Interaction';
import { AuthRequest } from '../middleware/auth';

export async function createEnrollment(req: AuthRequest, res: Response) {
  try {
    const userId = req.userId;
    if (!userId) return res.status(401).json({ error: 'Unauthorized' });

    const { courseId, metadata } = req.body as { courseId: string; metadata?: Record<string, unknown> };

    if (!mongoose.Types.ObjectId.isValid(courseId)) {
      return res.status(400).json({ error: 'Invalid courseId' });
    }

    const course = await Course.findById(courseId).select('_id').exec();
    if (!course) return res.status(404).json({ error: 'Course not found' });

    const existing = await Interaction.findOne({
      user: userId,
      course: courseId,
      action: 'enroll'
    }).exec();

    if (existing) {
      return res.status(200).json({
        enrollment: {
          _id: existing._id,
          user: existing.user,
          course: existing.course,
          action: existing.action,
          createdAt: existing.createdAt
        }
      });
    }

    const enrollment = await Interaction.create({
      user: userId,
      course: courseId,
      action: 'enroll',
      metadata: metadata ?? {}
    });

    return res.status(201).json({
      enrollment: {
        _id: enrollment._id,
        user: enrollment.user,
        course: enrollment.course,
        action: enrollment.action,
        createdAt: enrollment.createdAt
      }
    });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: 'Failed to create enrollment' });
  }
}
