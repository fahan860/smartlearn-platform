import dotenv from 'dotenv';

dotenv.config();

interface AppConfig {
  mongoUri: string;
  jwtSecret: string;
  port: number;
  mlServiceUrl?: string;
  environment: 'development' | 'test' | 'production';
  mysql: {
    host: string;
    port: number;
    user: string;
    password: string;
    database: string;
  };
}

function requireEnv(name: string, fallback?: string): string {
  const value = process.env[name] ?? fallback;
  if (!value) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return value;
}

const environment = (process.env.NODE_ENV as AppConfig['environment']) || 'development';
const defaultMongo = environment === 'production' ? undefined : process.env.MONGODB_URI_TEST || 'mongodb://127.0.0.1:27017/learning';
const defaultJwt = environment === 'production' ? undefined : process.env.JWT_SECRET || 'dev-secret';

export const config: AppConfig = {
  mongoUri: requireEnv('MONGODB_URI', defaultMongo),
  jwtSecret: requireEnv('JWT_SECRET', defaultJwt),
  port: Number(process.env.PORT || 4000),
  mlServiceUrl: process.env.ML_SERVICE_URL,
  environment,
  mysql: {
    host: process.env.MYSQL_HOST || 'localhost',
    port: Number(process.env.MYSQL_PORT || 3306),
    user: process.env.MYSQL_USER || 'root',
    password: process.env.MYSQL_PASSWORD || 'root',
    database: process.env.MYSQL_DATABASE || 'smartlearn'
  }
};
