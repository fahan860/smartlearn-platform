import Course from '../models/Course';
import Interaction from '../models/Interaction';
import { config } from '../config';

type MlRecommendationRequest = {
  userId: string;
  candidateCourseIds: string[];
  excludeCourseIds: string[];
  topK: number;
};

type MlRecommendationResponse = {
  courseIds: string[];
};

async function callMlService(payload: MlRecommendationRequest): Promise<MlRecommendationResponse> {
  if (!config.mlServiceUrl) {
    throw new Error('ML_SERVICE_URL is not configured');
  }

  const response = await fetch(`${config.mlServiceUrl}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const body = await response.text().catch(() => '');
    throw new Error(`ML service request failed (${response.status}): ${body}`);
  }

  const data = (await response.json()) as MlRecommendationResponse;
  if (!Array.isArray(data.courseIds)) {
    throw new Error('Invalid ML service response: courseIds is missing');
  }

  return data;
}

export async function generateRecommendations(userId: string) {
  const recentInteractions = await Interaction.find({ user: userId })
    .sort({ createdAt: -1 })
    .limit(300)
    .select('course')
    .exec();

  const excludedCourseIds = Array.from(
    new Set(recentInteractions.map((interaction) => String(interaction.course)))
  );

  const candidateCourses = await Course.find({
    _id: { $nin: excludedCourseIds }
  })
    .select('_id')
    .limit(1000)
    .exec();

  const candidateCourseIds = candidateCourses.map((course) => String(course._id));
  if (candidateCourseIds.length === 0) {
    return [];
  }

  const mlResult = await callMlService({
    userId,
    candidateCourseIds,
    excludeCourseIds: excludedCourseIds,
    topK: 20
  });

  const orderedIds = mlResult.courseIds.filter((id) => candidateCourseIds.includes(id));
  if (orderedIds.length === 0) {
    return [];
  }

  const courses = await Course.find({ _id: { $in: orderedIds } }).exec();
  const byId = new Map(courses.map((course) => [String(course._id), course]));
  return orderedIds.map((id) => byId.get(id)).filter(Boolean);
}
