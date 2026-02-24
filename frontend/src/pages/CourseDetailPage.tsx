import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ChevronLeft, Clock, Award, Bookmark, Share2 } from 'lucide-react';
import { Layout } from '../components/Layout';
import { coursesApi, interactionsApi, Course } from '../services/api';
import toast from 'react-hot-toast';

const CourseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);

  useEffect(() => {
    if (!id) {
      navigate('/courses');
      return;
    }
    loadCourse();
  }, [id, navigate]);

  const loadCourse = async () => {
    try {
      const data = await coursesApi.get(id!);
      setCourse(data);
    } catch (error) {
      toast.error('Failed to load course');
      navigate('/courses');
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async () => {
    if (!course) return;
    setEnrolling(true);
    try {
      await interactionsApi.record(course._id, 'enroll');
      toast.success('Successfully enrolled in this course!');
    } catch (error) {
      toast.error('Failed to enroll');
    } finally {
      setEnrolling(false);
    }
  };

  const handleGoBack = () => {
    navigate('/courses');
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

  if (!course) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Course not found</h2>
            <button
              onClick={handleGoBack}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
            >
              Back to Courses
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back button */}
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={handleGoBack}
          className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 mb-8 transition"
        >
          <ChevronLeft className="w-5 h-5" />
          <span>Back to Courses</span>
        </motion.button>

        {/* Course Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-primary-600 to-indigo-600 rounded-2xl p-8 text-white mb-8"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="inline-block bg-white/20 px-3 py-1 rounded-full text-sm font-semibold mb-4">
                {course.level.charAt(0).toUpperCase() + course.level.slice(1)} Level
              </div>
              <h1 className="text-4xl font-bold mb-4">{course.title}</h1>
              <p className="text-lg text-white/90 mb-6">{course.description}</p>

              <div className="flex flex-wrap gap-4">
                {course.durationMinutes && (
                  <div className="flex items-center space-x-2">
                    <Clock className="w-5 h-5" />
                    <span>{course.durationMinutes} minutes</span>
                  </div>
                )}
                <div className="flex items-center space-x-2">
                  <Award className="w-5 h-5" />
                  <span>Certificate Included</span>
                </div>
              </div>
            </div>

            <div className="flex gap-3 ml-4">
              <button className="p-3 bg-white/20 hover:bg-white/30 rounded-lg transition">
                <Bookmark className="w-5 h-5" />
              </button>
              <button className="p-3 bg-white/20 hover:bg-white/30 rounded-lg transition">
                <Share2 className="w-5 h-5" />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Content Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 lg:grid-cols-3 gap-8"
        >
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* About */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">About This Course</h2>
              <p className="text-gray-600 leading-relaxed mb-4">{course.description}</p>
              <p className="text-gray-600 leading-relaxed">
                This course is designed to provide comprehensive learning experience with practical
                applications and real-world examples. Whether you're a beginner or looking to enhance
                your skills, this course offers valuable insights and hands-on training.
              </p>
            </div>

            {/* Tags */}
            {course.tags && course.tags.length > 0 && (
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Topics Covered</h2>
                <div className="flex flex-wrap gap-3">
                  {course.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-4 py-2 bg-primary-100 text-primary-700 rounded-lg font-semibold"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Prerequisites */}
            {course.prerequisites && course.prerequisites.length > 0 && (
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Prerequisites</h2>
                <p className="text-gray-600">
                  This course has {course.prerequisites.length} prerequisite(s). Make sure you have
                  completed the recommended courses before enrolling.
                </p>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 sticky top-20"
            >
              <button
                onClick={handleEnroll}
                disabled={enrolling}
                className="w-full bg-gradient-to-r from-primary-600 to-indigo-600 hover:shadow-lg disabled:opacity-50 text-white font-bold py-3 px-6 rounded-lg transition mb-4"
              >
                {enrolling ? 'Enrolling...' : 'Enroll Now'}
              </button>

              <button className="w-full border-2 border-gray-200 hover:border-primary-600 text-gray-900 font-semibold py-3 px-6 rounded-lg transition">
                Save for Later
              </button>

              {/* Course Stats */}
              <div className="mt-8 space-y-4 pt-8 border-t border-gray-200">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Course Level</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {course.level.charAt(0).toUpperCase() + course.level.slice(1)}
                  </p>
                </div>

                {course.durationMinutes && (
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Duration</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {Math.floor(course.durationMinutes / 60)}h{' '}
                      {course.durationMinutes % 60 > 0 ? `${course.durationMinutes % 60}m` : ''}
                    </p>
                  </div>
                )}

                <div>
                  <p className="text-sm text-gray-600 mb-1">Course ID</p>
                  <p className="text-sm font-mono text-gray-500 truncate">{course._id}</p>
                </div>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default CourseDetailPage;
