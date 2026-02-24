import mongoose, { Schema } from 'mongoose';

export type InteractionAction = 'view' | 'enroll' | 'complete';

export interface IInteraction extends mongoose.Document {
  user: mongoose.Types.ObjectId;
  course: mongoose.Types.ObjectId;
  action: InteractionAction;
  metadata?: Record<string, any>;
  createdAt: Date;
}

const interactionSchema = new Schema<IInteraction>({
  user: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  course: { type: Schema.Types.ObjectId, ref: 'Course', required: true },
  action: { type: String, enum: ['view', 'enroll', 'complete'], required: true },
  metadata: { type: Schema.Types.Mixed },
  createdAt: { type: Date, default: Date.now }
});

interactionSchema.index({ user: 1, createdAt: -1 });

const Interaction = mongoose.model<IInteraction>('Interaction', interactionSchema);
export default Interaction;
