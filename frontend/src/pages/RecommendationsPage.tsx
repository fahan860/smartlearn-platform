import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, RefreshCw, TrendingUp } from 'lucide-react';
import { Layout } from '../components/Layout';
import { CourseCard } from '../components/CourseCard';
import { recommendationsApi, interactionsApi, Course } from '../services/api';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const RecommendationsPage: React.FC = () => {
  const [recommendations, setRecommendations] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      const data = await recommendationsApi.get();
      setRecommendations(data);
    } catch (error) {
      toast.error('Failed to load recommendations');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    loadRecommendations();
  };

  const handleCourseClick = async (courseId: string) => {
    try {
      await interactionsApi.record(courseId, 'view');
      navigate(`/courses/${courseId}`);
    } catch (error) {
      console.error('Failed to record interaction', error);
      navigate(`/courses/${courseId}`);
    }
  };

  const handleEnroll = async (courseId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await interactionsApi.record(courseId, 'enroll');
      toast.success('Enrolled successfully!');
    } catch (error) {
      toast.error('Failed to enroll');
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-3 mb-2">
                <div className="bg-gradient-to-br from-yellow-400 to-orange-500 p-2 rounded-lg">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-4xl font-bold text-gray-900">Recommended For You</h1>
              </div>
              <p className="text-gray-600 text-lg">
                Personalized course recommendations based on your learning journey
              </p>
            </div>
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center space-x-2 px-4 py-2 bg-white border-2 border-gray-200 text-gray-700 rounded-lg font-medium hover:border-primary-600 hover:text-primary-600 transition-all disabled:opacity-50"
            >
              <RefreshCw className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
          </div>
        </motion.div>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-r from-primary-50 to-indigo-50 rounded-xl p-6 mb-8 border border-primary-100"
        >
          <div className="flex items-start space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">How Recommendations Work</h3>
              <p className="text-gray-700">
                Our AI analyzes your learning history, course interactions, and progress to suggest
                courses that match your interests and skill level. The more you learn, the better our
                recommendations become!
              </p>
            </div>
          </div>
        </motion.div>

        {/* Recommendations Grid */}
        {recommendations.length > 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {recommendations.map((course, index) => (
              <motion.div
                key={course._id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index }}
                className="relative"
              >
                <CourseCard course={course} onClick={() => handleCourseClick(course._id)} />
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={(e) => handleEnroll(course._id, e)}
                  className="absolute top-4 right-4 px-4 py-2 bg-white/90 backdrop-blur-sm text-primary-600 rounded-lg font-semibold shadow-lg hover:bg-white transition-all z-10"
                >
                  Enroll Now
                </motion.button>
              </motion.div>
            ))}
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl p-12 text-center shadow-md border border-gray-100"
          >
            <div className="bg-gradient-to-br from-yellow-100 to-orange-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-10 h-10 text-orange-600" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">No Recommendations Yet</h3>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Start exploring courses and interacting with content to receive personalized
              recommendations tailored to your learning goals
            </p>
            <button
              onClick={() => navigate('/courses')}
              className="px-6 py-3 bg-gradient-to-r from-primary-600 to-indigo-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
            >
              Explore Courses
            </button>
          </motion.div>
        )}

        {/* Tips Section */}
        {recommendations.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-12 bg-white rounded-xl p-8 shadow-md border border-gray-100"
          >
            <h3 className="text-xl font-bold text-gray-900 mb-4">💡 Pro Tips</h3>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start space-x-3">
                <span className="text-primary-600 font-bold">•</span>
                <span>Complete courses to unlock more advanced recommendations</span>
              </li>
              <li className="flex items-start space-x-3">
                <span className="text-primary-600 font-bold">•</span>
                <span>Explore different topics to diversify your skill set</span>
              </li>
              <li className="flex items-start space-x-3">
                <span className="text-primary-600 font-bold">•</span>
                <span>Track your progress to see how recommendations evolve</span>
              </li>
            </ul>
          </motion.div>
        )}
      </div>
    </Layout>
  );
};

export default RecommendationsPage;
