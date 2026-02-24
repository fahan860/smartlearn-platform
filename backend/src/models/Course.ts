import mongoose, { Schema } from 'mongoose';

export interface ICourse extends mongoose.Document {
  title: string;
  description: string;
  tags: string[];
  level: 'beginner' | 'intermediate' | 'advanced';
  durationMinutes?: number;
  prerequisites?: mongoose.Types.ObjectId[];
  createdAt: Date;
}

const courseSchema = new Schema<ICourse>({
  title: { type: String, required: true },
  description: { type: String, required: true },
  tags: [{ type: String }],
  level: { type: String, enum: ['beginner', 'intermediate', 'advanced'], default: 'beginner' },
  durationMinutes: { type: Number },
  prerequisites: [{ type: Schema.Types.ObjectId, ref: 'Course' }],
  createdAt: { type: Date, default: Date.now }
});

courseSchema.index({ title: 'text', description: 'text', tags: 'text' });

const Course = mongoose.model<ICourse>('Course', courseSchema);
export default Course;
