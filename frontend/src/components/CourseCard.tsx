import React from 'react';
import { motion } from 'framer-motion';
import { Clock, Award } from 'lucide-react';
import { Course } from '../services/api';

interface CourseCardProps {
  course: Course;
  onClick: () => void;
}

export const CourseCard: React.FC<CourseCardProps> = ({ course, onClick }) => {
  const levelColors = {
    beginner: 'bg-green-100 text-green-800',
    intermediate: 'bg-blue-100 text-blue-800',
    advanced: 'bg-purple-100 text-purple-800',
  };

  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
      onClick={onClick}
      className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all cursor-pointer border border-gray-100 overflow-hidden"
    >
      {/* Gradient Header */}
      <div className="h-32 bg-gradient-to-br from-primary-500 to-indigo-600 relative">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="absolute bottom-3 left-4 right-4">
          <span
            className={`px-3 py-1 rounded-full text-xs font-semibold ${
              levelColors[course.level]
            }`}
          >
            {course.level}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">{course.title}</h3>
        <p className="text-gray-600 text-sm mb-4 line-clamp-3">{course.description}</p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {course.tags.slice(0, 3).map((tag, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-gray-100 text-gray-700 rounded-md text-xs font-medium"
            >
              {tag}
            </span>
          ))}
          {course.tags.length > 3 && (
            <span className="px-2 py-1 bg-gray-100 text-gray-500 rounded-md text-xs">
              +{course.tags.length - 3}
            </span>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between text-sm text-gray-500">
          {course.durationMinutes && (
            <div className="flex items-center space-x-1">
              <Clock className="w-4 h-4" />
              <span>{Math.floor(course.durationMinutes / 60)}h {course.durationMinutes % 60}m</span>
            </div>
          )}
          <div className="flex items-center space-x-1">
            <Award className="w-4 h-4" />
            <span>Certificate</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
