import mongoose, { Schema } from 'mongoose';

export interface ILearningPath extends mongoose.Document {
  title: string;
  description: string;
  courses: mongoose.Types.ObjectId[];
  tags?: string[];
  createdAt: Date;
}

const learningPathSchema = new Schema<ILearningPath>({
  title: { type: String, required: true },
  description: { type: String, required: true },
  courses: [{ type: Schema.Types.ObjectId, ref: 'Course', required: true }],
  tags: [{ type: String }],
  createdAt: { type: Date, default: Date.now }
});

const LearningPath = mongoose.model<ILearningPath>('LearningPath', learningPathSchema);
export default LearningPath;
