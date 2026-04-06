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

async function fetchWithTimeout(input: string, init: RequestInit, timeoutMs: number) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(input, { ...init, signal: controller.signal });
  } finally {
    clearTimeout(id);
  }
}

async function callMlService(
  payload: MlRecommendationRequest,
  opts: { timeoutMs?: number } = {}
): Promise<MlRecommendationResponse> {
  if (!config.mlServiceUrl) {
    throw new Error('ML_SERVICE_URL is not configured');
  }

  const response = await fetchWithTimeout(
    `${config.mlServiceUrl}/recommend`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    },
    opts.timeoutMs ?? 2000
  );

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

async function fallbackPopularCourses(excludeCourseIds: string[], limit = 20) {
  // Popularité = nombre d'interactions par course
  const pipeline: any[] = [
    { $match: { course: { $exists: true, $ne: null } } },
    ...(excludeCourseIds.length ? [{ $match: { course: { $nin: excludeCourseIds } } }] : []),
    { $group: { _id: '$course', score: { $sum: 1 } } },
    { $sort: { score: -1 } },
    { $limit: limit }
  ];

  const popular = await Interaction.aggregate(pipeline).exec();
  const ids = popular.map((x: any) => String(x._id)).filter(Boolean);

  if (ids.length > 0) {
    const courses = await Course.find({ _id: { $in: ids } }).exec();
    const byId = new Map(courses.map((c) => [String(c._id), c]));
    return ids.map((id) => byId.get(id)).filter(Boolean);
  }

  // Si pas de data: cours les plus récents
  return await Course.find({ _id: { $nin: excludeCourseIds } })
    .sort({ createdAt: -1 })
    .limit(limit)
    .exec();
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

  let orderedIds: string[] = [];

  try {
    const mlResult = await callMlService(
      {
        userId,
        candidateCourseIds,
        excludeCourseIds: excludedCourseIds,
        topK: 20
      },
      { timeoutMs: 2000 }
    );

    orderedIds = mlResult.courseIds.filter((id) => candidateCourseIds.includes(id));
  } catch (e) {
    console.warn('[recommendations] ML service failed, using fallback:', e);
  }

  if (orderedIds.length === 0) {
    return await fallbackPopularCourses(excludedCourseIds, 20);
  }

  const courses = await Course.find({ _id: { $in: orderedIds } }).exec();
  const byId = new Map(courses.map((course) => [String(course._id), course]));
  return orderedIds.map((id) => byId.get(id)).filter(Boolean);
}