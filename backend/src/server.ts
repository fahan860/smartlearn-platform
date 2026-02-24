import mongoose from 'mongoose';
import app from './app';
import { config } from './config';

const signals: NodeJS.Signals[] = ['SIGINT', 'SIGTERM'];

mongoose
  .connect(config.mongoUri)
  .then(() => {
    console.log('Connected to MongoDB');
    const server = app.listen(config.port, () => console.log(`Server running on port ${config.port}`));

    signals.forEach((sig) => {
      process.on(sig, async () => {
        console.log(`Received ${sig}, shutting down...`);
        server.close();
        await mongoose.disconnect();
        process.exit(0);
      });
    });
  })
  .catch((err) => {
    console.error('Mongo connection error', err);
    process.exit(1);
  });

process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection', reason);
});
