import { Request, Response } from 'express';
import { validationResult } from 'express-validator';
import Interaction from '../models/Interaction';
import { AuthRequest } from '../middleware/auth';

export async function recordInteraction(req: AuthRequest, res: Response) {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

    const userId = req.userId;
    if (!userId) return res.status(401).json({ error: 'Unauthorized' });

    const { course, action, metadata } = req.body;
    const interaction = new Interaction({ user: userId, course, action, metadata });
    await interaction.save();
    res.status(201).json(interaction);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to record interaction' });
  }
}

export async function getMyInteractions(req: AuthRequest, res: Response) {
  try {
    const userId = req.userId;
    if (!userId) return res.status(401).json({ error: 'Unauthorized' });

    const interactions = await Interaction.find({ user: userId }).sort({ createdAt: -1 }).limit(200).exec();
    res.json(interactions);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch interactions' });
  }
}
