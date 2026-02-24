"""
Smart Learning Platform - Data Generator
Phase 1: Generate realistic synthetic data for ML training

This module generates:
- Users (1000+): Realistic user profiles with learning preferences
- Courses (100+): Diverse courses across multiple categories
- Interactions (10000+): User-course interactions (views, enrolls, progress, completions)
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import yaml
from faker import Faker
import numpy as np
import pandas as pd
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataGenerator:
    """Generate synthetic learning platform data"""
    
    def __init__(self, config_path: str = "simulator/config/config.yaml"):
        """Initialize generator with configuration"""
        self.fake = Faker()
        self.config = self._load_config(config_path)
        
        # Set random seed for reproducibility
        seed = self.config.get('random_seed', 42)
        if seed:
            random.seed(seed)
            np.random.seed(seed)
            Faker.seed(seed)
        
        self.users = []
        self.courses = []
        self.interactions = []
        
        logger.info("Data Generator initialized")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        import os
        # Try multiple paths
        possible_paths = [
            config_path,
            os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml'),
            os.path.join(os.getcwd(), 'simulator', 'config', 'config.yaml'),
            os.path.join(os.getcwd(), 'config', 'config.yaml'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        logger.info(f"Loaded config from: {path}")
                        return config
                except Exception as e:
                    logger.warning(f"Error loading config from {path}: {e}")
        
        logger.warning(f"Config file not found at any location. Using defaults.")
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration with all required fields"""
        return {
            'database': {
                'mongodb_uri': 'mongodb://localhost:27017',
                'db_name': 'smart_learning'
            },
            'generation': {
                'num_users': 1200,
                'num_courses': 150,
                'num_interactions': 15000,
                'user_types': {
                    'beginner': 0.40,
                    'intermediate': 0.35,
                    'advanced': 0.25
                },
                'course_levels': {
                    'beginner': 0.45,
                    'intermediate': 0.35,
                    'advanced': 0.20
                },
                'interaction_weights': {
                    'view': 1.0,
                    'enroll': 0.3,
                    'progress': 0.7,
                    'complete': 0.4
                },
                'categories': [
                    {
                        'name': 'Programming',
                        'weight': 0.25,
                        'topics': ['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust', 'TypeScript']
                    },
                    {
                        'name': 'Data Science',
                        'weight': 0.20,
                        'topics': ['Machine Learning', 'Deep Learning', 'Data Analysis', 'Statistics', 'Data Visualization', 'Big Data']
                    },
                    {
                        'name': 'Web Development',
                        'weight': 0.20,
                        'topics': ['React', 'Angular', 'Vue.js', 'Node.js', 'HTML/CSS', 'REST APIs', 'GraphQL']
                    },
                    {
                        'name': 'Cloud & DevOps',
                        'weight': 0.15,
                        'topics': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform']
                    },
                    {
                        'name': 'Mobile Development',
                        'weight': 0.10,
                        'topics': ['React Native', 'Flutter', 'iOS Development', 'Android Development']
                    },
                    {
                        'name': 'Cybersecurity',
                        'weight': 0.10,
                        'topics': ['Network Security', 'Ethical Hacking', 'Cryptography', 'Security Auditing']
                    }
                ]
            },
            'output': {
                'base_path': 'data',
                'formats': ['json', 'csv'],
                'paths': {
                    'raw_courses': 'data/raw/courses',
                    'raw_users': 'data/raw/users',
                    'raw_interactions': 'data/raw/interactions',
                    'processed': 'data/processed'
                }
            },
            'random_seed': 42,
            'logging': {
                'level': 'INFO',
                'file': 'simulator/logs/data_generation.log'
            }
        }
    
    def generate_users(self) -> List[Dict[str, Any]]:
        """Generate realistic user profiles"""
        num_users = self.config['generation']['num_users']
        user_types = self.config['generation'].get('user_types', {
            'beginner': 0.40,
            'intermediate': 0.35,
            'advanced': 0.25
        })
        
        logger.info(f"Generating {num_users} users...")
        
        for i in tqdm(range(num_users), desc="Creating users"):
            # Determine user level
            level = np.random.choice(
                list(user_types.keys()),
                p=list(user_types.values())
            )
            
            # Generate user profile
            user = {
                '_id': f"user_{i+1:05d}",
                'username': self.fake.user_name() + str(random.randint(100, 999)),
                'email': self.fake.email(),
                'password': '$2b$10$hashedpassword',  # Placeholder hashed password
                'profile': {
                    'firstName': self.fake.first_name(),
                    'lastName': self.fake.last_name(),
                    'level': level,
                    'interests': self._generate_interests(),
                    'learningGoals': self._generate_learning_goals(level),
                    'avatar': f"https://i.pravatar.cc/150?u={i}",
                    'bio': self.fake.text(max_nb_chars=200),
                    'location': self.fake.city(),
                    'timezone': random.choice(['UTC', 'EST', 'PST', 'CET', 'JST'])
                },
                'statistics': {
                    'coursesEnrolled': 0,
                    'coursesCompleted': 0,
                    'totalLearningTime': 0,
                    'currentStreak': 0,
                    'longestStreak': 0
                },
                'preferences': {
                    'emailNotifications': random.choice([True, False]),
                    'weeklyDigest': random.choice([True, False]),
                    'darkMode': random.choice([True, False]),
                    'language': 'en'
                },
                'createdAt': self._random_past_date(days=365),
                'updatedAt': self._random_past_date(days=30),
                'lastLoginAt': self._random_past_date(days=7)
            }
            
            self.users.append(user)
        
        logger.info(f"✓ Generated {len(self.users)} users")
        return self.users
    
    def generate_courses(self) -> List[Dict[str, Any]]:
        """Generate diverse course catalog"""
        num_courses = self.config['generation']['num_courses']
        categories = self.config['generation'].get('categories', [])
        course_levels = self.config['generation'].get('course_levels', {
            'beginner': 0.45,
            'intermediate': 0.35,
            'advanced': 0.20
        })
        
        logger.info(f"Generating {num_courses} courses...")
        
        course_id = 1
        for i in tqdm(range(num_courses), desc="Creating courses"):
            # Select category and topic
            category = self._weighted_choice(categories)
            topic = random.choice(category['topics'])
            
            # Determine difficulty level
            level = np.random.choice(
                list(course_levels.keys()),
                p=list(course_levels.values())
            )
            
            # Generate realistic course data
            title = self._generate_course_title(topic, level)
            
            course = {
                '_id': f"course_{course_id:05d}",
                'title': title,
                'slug': title.lower().replace(' ', '-').replace('&', 'and'),
                'description': self._generate_course_description(topic, level),
                'category': category['name'],
                'topic': topic,
                'level': level,
                'instructor': {
                    'name': self.fake.name(),
                    'title': self._generate_instructor_title(),
                    'bio': self.fake.text(max_nb_chars=150),
                    'avatar': f"https://i.pravatar.cc/150?u=instructor{course_id}",
                    'rating': round(random.uniform(4.0, 5.0), 2)
                },
                'content': {
                    'duration': random.randint(300, 7200),  # 5 min to 2 hours
                    'modules': random.randint(4, 12),
                    'lessons': random.randint(15, 60),
                    'exercises': random.randint(10, 40),
                    'projects': random.randint(1, 5),
                    'language': 'English',
                    'subtitles': random.sample(['en', 'es', 'fr', 'de', 'pt', 'zh'], k=random.randint(2, 4))
                },
                'pricing': {
                    'type': random.choice(['free', 'paid', 'subscription']),
                    'amount': random.choice([0, 29.99, 49.99, 79.99, 99.99]),
                    'currency': 'USD'
                },
                'enrollment': {
                    'studentsEnrolled': random.randint(50, 5000),
                    'maxStudents': random.choice([None, 100, 500, 1000]),
                    'startDate': self._random_past_date(days=180),
                    'endDate': None  # Open enrollment
                },
                'ratings': {
                    'average': round(random.uniform(3.5, 5.0), 2),
                    'count': random.randint(10, 500),
                    'distribution': self._generate_rating_distribution()
                },
                'tags': self._generate_course_tags(topic, category['name']),
                'prerequisites': self._generate_prerequisites(level),
                'outcomes': self._generate_learning_outcomes(topic, level),
                'status': random.choices(
                    ['active', 'draft', 'archived'],
                    weights=[0.85, 0.10, 0.05],
                    k=1
                )[0],
                'featured': random.random() < 0.15,  # 15% are featured
                'certificate': random.random() < 0.7,  # 70% offer certificates
                'createdAt': self._random_past_date(days=365),
                'updatedAt': self._random_past_date(days=60)
            }
            
            self.courses.append(course)
            course_id += 1
        
        logger.info(f"✓ Generated {len(self.courses)} courses")
        return self.courses
    
    def generate_interactions(self) -> List[Dict[str, Any]]:
        """Generate realistic user-course interactions"""
        if not self.users or not self.courses:
            raise ValueError("Generate users and courses first!")
        
        num_interactions = self.config['generation']['num_interactions']
        weights = self.config['generation'].get('interaction_weights', {
            'view': 1.0,
            'enroll': 0.3,
            'progress': 0.7,
            'complete': 0.4
        })
        
        logger.info(f"Generating {num_interactions} interactions...")
        
        # Only active courses can have interactions
        active_courses = [c for c in self.courses if c['status'] == 'active']
        
        interaction_id = 1
        for _ in tqdm(range(num_interactions), desc="Creating interactions"):
            user = random.choice(self.users)
            course = random.choice(active_courses)
            
            # Determine interaction type based on realistic progression
            interaction_type = self._determine_interaction_type(weights)
            
            interaction = {
                '_id': f"interaction_{interaction_id:06d}",
                'userId': user['_id'],
                'courseId': course['_id'],
                'type': interaction_type,
                'timestamp': self._random_past_date(days=180),
                'metadata': self._generate_interaction_metadata(interaction_type, course),
                'device': random.choice(['desktop', 'mobile', 'tablet']),
                'platform': random.choice(['web', 'ios', 'android']),
                'sessionId': f"session_{random.randint(100000, 999999)}"
            }
            
            # Add type-specific data
            if interaction_type == 'enroll':
                interaction['enrollmentDate'] = interaction['timestamp']
                interaction['paymentStatus'] = 'completed' if course['pricing']['type'] == 'paid' else 'free'
            
            elif interaction_type == 'progress':
                interaction['progress'] = {
                    'percentage': random.randint(1, 99),
                    'lessonsCompleted': random.randint(1, course['content']['lessons'] - 1),
                    'timeSpent': random.randint(300, 3600),  # seconds
                    'lastLessonId': f"lesson_{random.randint(1, 50)}"
                }
            
            elif interaction_type == 'complete':
                interaction['completion'] = {
                    'completedAt': interaction['timestamp'],
                    'finalGrade': random.randint(70, 100),
                    'certificate': course['certificate'],
                    'certificateId': f"cert_{interaction_id:08d}" if course['certificate'] else None,
                    'timeSpent': random.randint(3600, 18000)  # 1-5 hours
                }
            
            self.interactions.append(interaction)
            interaction_id += 1
        
        logger.info(f"✓ Generated {len(self.interactions)} interactions")
        return self.interactions
    
    def save_data(self):
        """Save generated data to files"""
        output_config = self.config.get('output', {})
        formats = output_config.get('formats', ['json', 'csv'])
        base_path = output_config.get('base_path', 'data')
        
        paths = output_config.get('paths', {
            'raw_courses': f'{base_path}/raw/courses',
            'raw_users': f'{base_path}/raw/users',
            'raw_interactions': f'{base_path}/raw/interactions'
        })
        
        logger.info("Saving generated data...")
        
        # Create directories
        for path in paths.values():
            os.makedirs(path, exist_ok=True)
        
        # Generate timestamp for this dataset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save users
        if 'json' in formats:
            self._save_json(self.users, f"{paths['raw_users']}/users_{timestamp}.json")
        if 'csv' in formats:
            self._save_csv(self.users, f"{paths['raw_users']}/users_{timestamp}.csv")
        
        # Save courses
        if 'json' in formats:
            self._save_json(self.courses, f"{paths['raw_courses']}/courses_{timestamp}.json")
        if 'csv' in formats:
            self._save_csv(self.courses, f"{paths['raw_courses']}/courses_{timestamp}.csv")
        
        # Save interactions
        if 'json' in formats:
            self._save_json(self.interactions, f"{paths['raw_interactions']}/interactions_{timestamp}.json")
        if 'csv' in formats:
            self._save_csv(self.interactions, f"{paths['raw_interactions']}/interactions_{timestamp}.csv")
        
        # Save summary statistics
        self._save_summary(f"{base_path}/generation_summary_{timestamp}.json")
        
        logger.info(f"✓ Data saved successfully to {base_path}/")
    
    def _save_json(self, data: List[Dict], filepath: str):
        """Save data as JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"  Saved: {filepath}")
    
    def _save_csv(self, data: List[Dict], filepath: str):
        """Save data as CSV (flattened)"""
        df = pd.json_normalize(data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"  Saved: {filepath}")
    
    def _save_summary(self, filepath: str):
        """Save generation summary statistics"""
        summary = {
            'generation_timestamp': datetime.now().isoformat(),
            'config': self.config,
            'statistics': {
                'users': {
                    'total': len(self.users),
                    'by_level': self._count_by_field(self.users, 'profile.level')
                },
                'courses': {
                    'total': len(self.courses),
                    'by_category': self._count_by_field(self.courses, 'category'),
                    'by_level': self._count_by_field(self.courses, 'level'),
                    'by_status': self._count_by_field(self.courses, 'status')
                },
                'interactions': {
                    'total': len(self.interactions),
                    'by_type': self._count_by_field(self.interactions, 'type')
                }
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, default=str)
        logger.info(f"  Saved summary: {filepath}")
    
    def _count_by_field(self, data: List[Dict], field: str) -> Dict[str, int]:
        """Count occurrences by nested field"""
        counts = {}
        for item in data:
            value = item
            for key in field.split('.'):
                value = value.get(key, 'unknown')
            counts[str(value)] = counts.get(str(value), 0) + 1
        return counts
    
    # Helper methods for realistic data generation
    
    def _generate_interests(self) -> List[str]:
        """Generate random interests"""
        all_interests = [
            'Programming', 'Web Development', 'Mobile Apps', 'Data Science',
            'Machine Learning', 'AI', 'Cloud Computing', 'DevOps',
            'Cybersecurity', 'Game Development', 'UI/UX Design', 'Databases'
        ]
        return random.sample(all_interests, k=random.randint(2, 5))
    
    def _generate_learning_goals(self, level: str) -> List[str]:
        """Generate learning goals based on level"""
        goals_map = {
            'beginner': [
                'Learn programming fundamentals',
                'Build my first project',
                'Understand basic concepts',
                'Get started with coding'
            ],
            'intermediate': [
                'Master advanced concepts',
                'Build portfolio projects',
                'Improve problem-solving skills',
                'Learn best practices'
            ],
            'advanced': [
                'Become an expert',
                'Contribute to open source',
                'Lead technical projects',
                'Mentor others'
            ]
        }
        return random.sample(goals_map.get(level, goals_map['beginner']), k=random.randint(1, 3))
    
    def _weighted_choice(self, categories: List[Dict]) -> Dict:
        """Choose category based on weight"""
        weights = [c.get('weight', 1.0) for c in categories]
        return random.choices(categories, weights=weights, k=1)[0]
    
    def _generate_course_title(self, topic: str, level: str) -> str:
        """Generate realistic course title"""
        templates = [
            f"Complete {topic} {level.capitalize()} Course",
            f"Master {topic}: From {level.capitalize()} to Pro",
            f"{topic} Fundamentals" if level == 'beginner' else f"Advanced {topic}",
            f"Learn {topic} in 30 Days",
            f"{topic} Bootcamp: {level.capitalize()} Edition",
            f"Professional {topic} Development",
            f"{topic}: A Comprehensive Guide"
        ]
        return random.choice(templates)
    
    def _generate_course_description(self, topic: str, level: str) -> str:
        """Generate course description"""
        return f"A comprehensive {level}-level course covering {topic}. {self.fake.text(max_nb_chars=200)}"
    
    def _generate_instructor_title(self) -> str:
        """Generate instructor title"""
        titles = [
            'Senior Software Engineer',
            'Tech Lead',
            'Principal Developer',
            'CTO',
            'Software Architect',
            'Full Stack Developer',
            'Data Scientist',
            'ML Engineer'
        ]
        return random.choice(titles)
    
    def _generate_rating_distribution(self) -> Dict[str, int]:
        """Generate realistic rating distribution (skewed towards higher ratings)"""
        total = random.randint(50, 500)
        distribution = np.random.dirichlet([1, 1, 2, 4, 8]) * total
        return {
            '5': int(distribution[4]),
            '4': int(distribution[3]),
            '3': int(distribution[2]),
            '2': int(distribution[1]),
            '1': int(distribution[0])
        }
    
    def _generate_course_tags(self, topic: str, category: str) -> List[str]:
        """Generate relevant tags"""
        base_tags = [topic.lower(), category.lower()]
        additional = ['beginner-friendly', 'hands-on', 'project-based', 'video', 'interactive']
        return base_tags + random.sample(additional, k=random.randint(2, 4))
    
    def _generate_prerequisites(self, level: str) -> List[str]:
        """Generate prerequisites based on level"""
        if level == 'beginner':
            return ['Basic computer skills', 'Willingness to learn']
        elif level == 'intermediate':
            return ['Programming fundamentals', 'Basic understanding of algorithms']
        else:
            return ['Strong programming background', 'Data structures knowledge', 'Previous project experience']
    
    def _generate_learning_outcomes(self, topic: str, level: str) -> List[str]:
        """Generate learning outcomes"""
        return [
            f"Master {topic} concepts",
            f"Build real-world projects using {topic}",
            "Solve complex problems",
            "Apply best practices and design patterns"
        ][:random.randint(3, 4)]
    
    def _determine_interaction_type(self, weights: Dict[str, float]) -> str:
        """Determine interaction type following realistic progression"""
        # Simplified: view → enroll → progress → complete
        rand = random.random()
        
        if rand < 0.4:
            return 'view'
        elif rand < 0.6:
            return 'enroll'
        elif rand < 0.85:
            return 'progress'
        else:
            return 'complete'
    
    def _generate_interaction_metadata(self, interaction_type: str, course: Dict) -> Dict:
        """Generate metadata for interaction"""
        metadata = {
            'courseTitle': course['title'],
            'courseCategory': course['category'],
            'courseTopic': course['topic']
        }
        
        if interaction_type == 'view':
            metadata['viewDuration'] = random.randint(30, 600)  # seconds
            metadata['sourceRef'] = random.choice(['search', 'recommendation', 'direct', 'social'])
        
        return metadata
    
    def _random_past_date(self, days: int = 365) -> str:
        """Generate random past datetime as ISO string"""
        days_ago = random.randint(0, days)
        date = datetime.now() - timedelta(days=days_ago)
        return date.isoformat()


def main():
    """Main execution function"""
    print("=" * 70)
    print("Smart Learning Platform - Data Generator")
    print("Phase 1: Synthetic Data Generation")
    print("=" * 70)
    print()
    
    # Initialize generator
    generator = DataGenerator()
    
    # Generate data
    generator.generate_users()
    generator.generate_courses()
    generator.generate_interactions()
    
    # Save to files
    generator.save_data()
    
    print()
    print("=" * 70)
    print("✓ Data generation complete!")
    print("=" * 70)
    print("\nGenerated:")
    print(f"  • {len(generator.users)} users")
    print(f"  • {len(generator.courses)} courses")
    print(f"  • {len(generator.interactions)} interactions")
    print("\nNext steps:")
    print("  1. Review generated data in data/raw/")
    print("  2. Run import script: python simulator/scripts/import_to_mongodb.py")
    print("  3. Verify data in MongoDB")
    print()


if __name__ == "__main__":
    main()
