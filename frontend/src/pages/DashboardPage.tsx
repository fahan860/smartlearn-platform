import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, BookOpen, Target, Award } from 'lucide-react';
import { Layout } from '../components/Layout';
import { CourseCard } from '../components/CourseCard';
import { coursesApi, interactionsApi, Course, Interaction, recommendationsApi } from '../services/api';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const DashboardPage: React.FC = () => {
  const [recentCourses, setRecentCourses] = useState<Course[]>([]);
  const [interactions, setInteractions] = useState<Interaction[]>([]);
  const [recommendations, setRecommendations] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [coursesData, interactionsData, recommendationsData] = await Promise.all([
        coursesApi.list(),
        interactionsApi.getMyInteractions(),
        recommendationsApi.get().catch(() => []),
      ]);

      setRecentCourses(coursesData.slice(0, 3));
      setInteractions(interactionsData.slice(0, 5));
      setRecommendations(recommendationsData.slice(0, 3));
    } catch (error) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
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

  const stats = [
    {
      icon: <BookOpen className="w-6 h-6" />,
      label: 'Courses Viewed',
      value: interactions.filter((i) => i.action === 'view').length,
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: <Target className="w-6 h-6" />,
      label: 'Enrolled',
      value: interactions.filter((i) => i.action === 'enroll').length,
      color: 'from-green-500 to-green-600',
    },
    {
      icon: <Award className="w-6 h-6" />,
      label: 'Completed',
      value: interactions.filter((i) => i.action === 'complete').length,
      color: 'from-purple-500 to-purple-600',
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      label: 'Completion Rate',
      value: interactions.filter((i) => i.action === 'enroll').length > 0
        ? `${Math.round((interactions.filter((i) => i.action === 'complete').length / interactions.filter((i) => i.action === 'enroll').length) * 100)}%`
        : '0%',
      color: 'from-orange-500 to-orange-600',
    },
  ];

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
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome Back! 👋</h1>
          <p className="text-gray-600 text-lg">Continue your learning journey where you left off</p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl p-6 shadow-md border border-gray-100"
            >
              <div className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${stat.color} text-white mb-4`}>
                {stat.icon}
              </div>
              <p className="text-gray-600 text-sm mb-1">{stat.label}</p>
              <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
            </motion.div>
          ))}
        </div>

        {/* Recommended For You */}
        {recommendations.length > 0 && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mb-12"
          >
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-1">Recommended For You</h2>
                <p className="text-gray-600">Personalized courses based on your learning history</p>
              </div>
              <button
                onClick={() => navigate('/recommendations')}
                className="px-4 py-2 text-primary-600 hover:text-primary-700 font-medium transition-colors"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.map((course) => (
                <CourseCard
                  key={course._id}
                  course={course}
                  onClick={() => handleCourseClick(course._id)}
                />
              ))}
            </div>
          </motion.section>
        )}

        {/* Recent Courses */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-1">Popular Courses</h2>
              <p className="text-gray-600">Explore trending courses in your field</p>
            </div>
            <button
              onClick={() => navigate('/courses')}
              className="px-4 py-2 text-primary-600 hover:text-primary-700 font-medium transition-colors"
            >
              View All
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentCourses.map((course) => (
              <CourseCard
                key={course._id}
                course={course}
                onClick={() => handleCourseClick(course._id)}
              />
            ))}
          </div>
        </motion.section>

        {/* Empty State */}
        {interactions.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl p-12 text-center shadow-md border border-gray-100 mt-8"
          >
            <div className="bg-gradient-to-br from-primary-100 to-indigo-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <BookOpen className="w-10 h-10 text-primary-600" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Start Your Learning Journey</h3>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Explore our course catalog and find the perfect courses to achieve your goals
            </p>
            <button
              onClick={() => navigate('/courses')}
              className="px-6 py-3 bg-gradient-to-r from-primary-600 to-indigo-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
            >
              Browse Courses
            </button>
          </motion.div>
        )}
      </div>
    </Layout>
  );
};

export default DashboardPage;
