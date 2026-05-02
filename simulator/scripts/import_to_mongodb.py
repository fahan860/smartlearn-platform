"""
Smart Learning Platform - MongoDB Import Script
Import generated synthetic data into MongoDB

Usage:
    python simulator/scripts/import_to_mongodb.py [options]

Options:
    --data-dir: Path to generated data directory (default: data/raw)
    --db-uri: MongoDB connection URI (default: mongodb://localhost:27017)
    --db-name: Database name (default: smart_learning)
    --clear: Clear existing collections before import (default: False)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import glob

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, BulkWriteError
except ImportError:
    print("Error: pymongo not installed. Run: pip install pymongo")
    sys.exit(1)

from tqdm import tqdm


class MongoDBImporter:
    """Import generated data into MongoDB"""
    
    def __init__(self, db_uri: str, db_name: str):
        """Initialize MongoDB connection"""
        self.db_uri = db_uri
        self.db_name = db_name
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            print(f"Connecting to MongoDB: {self.db_uri}")
            self.client = MongoClient(self.db_uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[self.db_name]
            print(f"✓ Connected to database: {self.db_name}")
            return True
        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ Disconnected from MongoDB")
    
    def clear_collections(self, collections: List[str]):
        """Clear specified collections"""
        print("\nClearing existing collections...")
        for collection_name in collections:
            result = self.db[collection_name].delete_many({})
            print(f"  • Deleted {result.deleted_count} documents from '{collection_name}'")
    
    def import_collection(self, collection_name: str, data: List[Dict[str, Any]]) -> bool:
        """Import data into a collection"""
        if not data:
            print(f"  ✗ No data to import for '{collection_name}'")
            return False
        
        try:
            collection = self.db[collection_name]
            
            # Convert _id fields to appropriate type
            processed_data = []
            for item in data:
                # Keep _id as string or let MongoDB generate ObjectId
                processed_data.append(item)
            
            # Bulk insert
            result = collection.insert_many(processed_data, ordered=False)
            print(f"  ✓ Imported {len(result.inserted_ids)} documents into '{collection_name}'")
            return True
            
        except BulkWriteError as e:
            print(f"  ⚠ Partial import to '{collection_name}': {e.details['nInserted']} succeeded, {len(e.details['writeErrors'])} failed")
            return False
        except Exception as e:
            print(f"  ✗ Error importing to '{collection_name}': {e}")
            return False
    
    def create_indexes(self):
        """Create indexes for better query performance"""
        print("\nCreating indexes...")
        
        indexes = [
            ('users', [('email', 1)], {'unique': True}),
            ('users', [('username', 1)], {'unique': True}),
            ('users', [('profile.level', 1)], {}),
            ('courses', [('category', 1)], {}),
            ('courses', [('topic', 1)], {}),
            ('courses', [('level', 1)], {}),
            ('courses', [('status', 1)], {}),
            ('courses', [('tags', 1)], {}),
            ('interactions', [('userId', 1)], {}),
            ('interactions', [('courseId', 1)], {}),
            ('interactions', [('type', 1)], {}),
            ('interactions', [('timestamp', -1)], {}),
            ('interactions', [('userId', 1, 'courseId', 1)], {})
        ]
        
        for collection_name, keys, options in indexes:
            try:
                index_name = self.db[collection_name].create_index(keys, **options)
                print(f"  ✓ Created index '{index_name}' on '{collection_name}'")
            except Exception as e:
                print(f"  ⚠ Index creation warning for '{collection_name}': {e}")
    
    def verify_import(self) -> Dict[str, int]:
        """Verify imported data counts"""
        print("\nVerifying imported data...")
        
        counts = {}
        for collection_name in ['users', 'courses', 'interactions']:
            count = self.db[collection_name].count_documents({})
            counts[collection_name] = count
            print(f"  • {collection_name}: {count} documents")
        
        return counts


def find_latest_data_files(data_dir: str) -> Dict[str, str]:
    """Find the most recent generated data files"""
    files = {
        'users': None,
        'courses': None,
        'interactions': None
    }
    
    for data_type in files.keys():
        pattern = os.path.join(data_dir, data_type, f"{data_type}_*.json")
        matching_files = glob.glob(pattern)
        
        if matching_files:
            # Get the most recent file
            files[data_type] = max(matching_files, key=os.path.getctime)
    
    return files


def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Load JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  ✓ Loaded {len(data)} records from {os.path.basename(filepath)}")
        return data
    except Exception as e:
        print(f"  ✗ Error loading {filepath}: {e}")
        return []


def main():
    """Main import execution"""
    parser = argparse.ArgumentParser(
        description='Import generated data into MongoDB'
    )
    parser.add_argument(
        '--data-dir',
        default='../data/raw',
        help='Path to generated data directory'
    )
    parser.add_argument(
        '--db-uri',
        default='mongodb://localhost:27017',
        help='MongoDB connection URI'
    )
    parser.add_argument(
        '--db-name',
        default='smart_learning',
        help='Database name'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear existing collections before import'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Smart Learning Platform - MongoDB Data Import")
    print("=" * 70)
    print()
    
    # Find latest data files
    print("Locating data files...")
    data_files = find_latest_data_files(args.data_dir)
    
    missing_files = [k for k, v in data_files.items() if v is None]
    if missing_files:
        print(f"\n✗ Error: Missing data files for: {', '.join(missing_files)}")
        print(f"   Generate data first: python simulator/src/data_generator.py")
        return 1
    
    print("\nFound data files:")
    for data_type, filepath in data_files.items():
        print(f"  • {data_type}: {os.path.basename(filepath)}")
    
    # Load data files
    print("\nLoading data files...")
    data = {}
    for data_type, filepath in data_files.items():
        data[data_type] = load_json_file(filepath)
        if not data[data_type]:
            print(f"✗ Failed to load {data_type} data")
            return 1
    
    # Connect to MongoDB
    print()
    importer = MongoDBImporter(args.db_uri, args.db_name)
    if not importer.connect():
        return 1
    
    try:
        # Clear collections if requested
        if args.clear:
            importer.clear_collections(['users', 'courses', 'interactions'])
        
        # Import collections
        print("\nImporting data to MongoDB...")
        success = True
        success &= importer.import_collection('users', data['users'])
        success &= importer.import_collection('courses', data['courses'])
        success &= importer.import_collection('interactions', data['interactions'])
        
        if not success:
            print("\n⚠ Import completed with warnings")
        
        # Create indexes
        importer.create_indexes()
        
        # Verify import
        counts = importer.verify_import()
        
        print()
        print("=" * 70)
        print("✓ Import completed successfully!")
        print("=" * 70)
        print(f"\nDatabase: {args.db_name}")
        print(f"Total documents: {sum(counts.values())}")
        print("\nNext steps:")
        print("  1. Verify data in MongoDB: mongosh")
        print("  2. Start the backend server")
        print("  3. Test API endpoints")
        print()
        
    finally:
        importer.disconnect()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
