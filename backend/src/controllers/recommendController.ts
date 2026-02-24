import { Response } from 'express';
import { AuthRequest } from '../middleware/auth';
import { generateRecommendations } from '../services/recommendationService';

export async function recommend(req: AuthRequest, res: Response) {
  try {
    const userId = req.userId;
    if (!userId) return res.status(401).json({ error: 'Unauthorized' });

    const recs = await generateRecommendations(userId);
    res.json({ recommendations: recs });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to generate recommendations' });
  }
}
