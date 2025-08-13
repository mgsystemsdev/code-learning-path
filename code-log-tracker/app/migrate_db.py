#!/usr/bin/env python3
"""
Migration script to convert old learning tracker database to new enhanced structure.
Run this script to migrate your existing data to the new smart tracker format.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from app.db import init_db, find_or_create_item, insert_or_update_session, slugify

def migrate_database():
    """Migrate from old database structure to new enhanced structure"""
    
    # Paths
    old_db_path = Path("learning_tracker.db")
    backup_path = Path("learning_tracker_backup.db")
    
    if not old_db_path.exists():
        print("No existing database found. Starting fresh with enhanced structure.")
        init_db()
        return
    
    print("🔄 Starting database migration...")
    
    # Create backup
    print("📦 Creating backup of existing database...")
    import shutil
    shutil.copy2(old_db_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    # Connect to old database
    old_con = sqlite3.connect(old_db_path)
    old_cur = old_con.cursor()
    
    # Check if it's already the new structure
    old_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
    if old_cur.fetchone():
        print("✅ Database already appears to be in the new format!")
        old_con.close()
        return
    
    # Get old data
    print("📊 Reading existing sessions...")
    try:
        old_cur.execute("""
            SELECT id, date, type, exercise_name, project_name, activity_name, 
                   description, lifecycle, hours_spent, tags, difficulty, domain, 
                   points_awarded, project_progress_pct
            FROM sessions ORDER BY date, id
        """)
        old_sessions = old_cur.fetchall()
        print(f"📈 Found {len(old_sessions)} existing sessions")
    except sqlite3.OperationalError as e:
        print(f"❌ Error reading old sessions: {e}")
        print("🔧 Assuming clean database, initializing new structure...")
        old_con.close()
        init_db()
        return
    
    old_con.close()
    
    # Initialize new database structure
    print("🗃️ Initializing new database structure...")
    init_db()
    
    # Migration mappings
    domain_to_language = {
        'Python Basics': 'python',
        'APIs': 'python',
        'Data': 'python', 
        'ML': 'python',
        'DevOps': 'git',
        'Security': 'python',
        'Cloud': 'git',
        'DB/SQL': 'sql',
        'Frontend': 'javascript'
    }
    
    domain_to_topic = {
        'Python Basics': 'Python Basics',
        'APIs': 'APIs & HTTP',
        'Data': 'Data Science',
        'ML': 'Machine Learning',
        'DevOps': 'DevOps & Deployment',
        'Security': 'Security',
        'Cloud': 'AWS Cloud Services',
        'DB/SQL': 'Database Integration',
        'Frontend': 'DOM Manipulation'
    }
    
    status_mapping = {
        'Planned': 'Planned',
        'In Progress': 'In Progress',
        'Blocked': 'Blocked',
        'Done': 'Completed',
        'Reviewed': 'Completed'
    }
    
    # Process each old session
    print("🔄 Migrating sessions...")
    migrated_count = 0
    errors = []
    
    for old_session in old_sessions:
        try:
            (old_id, date, session_type, exercise_name, project_name, activity_name,
             description, lifecycle, hours_spent, tags, difficulty, domain,
             points_awarded, project_progress_pct) = old_session
            
            # Determine work item name and language
            if session_type == 'Exercise' and exercise_name:
                work_item_name = exercise_name
                language_code = domain_to_language.get(domain, 'python')
            elif session_type == 'Project' and project_name:
                work_item_name = project_name
                if activity_name:
                    work_item_name += f" - {activity_name}"
                language_code = domain_to_language.get(domain, 'python')
            else:
                # Skip malformed sessions
                continue
            
            # Find or create item
            item_id, is_new, _ = find_or_create_item(language_code, session_type, work_item_name)
            
            if not item_id:
                errors.append(f"Failed to create item for: {work_item_name}")
                continue
            
            # Map old fields to new structure
            mapped_status = status_mapping.get(lifecycle, 'In Progress')
            mapped_topic = domain_to_topic.get(domain, 'Basics')
            mapped_difficulty = difficulty or 'Beginner'
            
            # Create session data
            session_data = {
                'item_id': item_id,
                'date': date,
                'status': mapped_status,
                'hours_spent': float(hours_spent or 0),
                'notes': description or '',
                'tags': tags or '',
                'difficulty': mapped_difficulty,
                'topic': mapped_topic
            }
            
            # Insert session
            new_session_id = insert_or_update_session(session_data)
            migrated_count += 1
            
            if migrated_count % 10 == 0:
                print(f"  📝 Migrated {migrated_count} sessions...")
            
        except Exception as e:
            errors.append(f"Error migrating session {old_id}: {e}")
            continue
    
    # Show results
    print(f"\n✅ Migration completed!")
    print(f"📊 Successfully migrated: {migrated_count} sessions")
    
    if errors:
        print(f"⚠️  Errors encountered: {len(errors)}")
        for error in errors[:5]:  # Show first 5 errors
            print(f"   - {error}")
        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more")
    
    print(f"\n📦 Original database backed up to: {backup_path}")
    print("🚀 Your enhanced learning tracker is ready to use!")

def create_sample_data():
    """Create some sample data to demonstrate the new features"""
    print("\n🎭 Creating sample data...")
    
    # Sample Python sessions
    sample_sessions = [
        {
            'language_code': 'python',
            'type': 'Exercise',
            'work_item_name': 'Pandas DataFrame Tutorial',
            'hours': 2.5,
            'notes': 'Learned about data manipulation with pandas dataframes',
            'status': 'Completed'
        },
        {
            'language_code': 'python',
            'type': 'Project', 
            'work_item_name': 'Web Scraper for Job Listings',
            'hours': 3.0,
            'notes': 'Built scraper using requests and beautifulsoup',
            'status': 'In Progress'
        },
        {
            'language_code': 'javascript',
            'type': 'Exercise',
            'work_item_name': 'React Hooks Practice',
            'hours': 1.5,
            'notes': 'Practiced useState and useEffect hooks',
            'status': 'Completed'
        }
    ]
    
    for sample in sample_sessions:
        try:
            # Find or create item
            item_id, is_new, _ = find_or_create_item(
                sample['language_code'], 
                sample['type'], 
                sample['work_item_name']
            )
            
            if item_id:
                session_data = {
                    'item_id': item_id,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'status': sample['status'],
                    'hours_spent': sample['hours'],
                    'notes': sample['notes'],
                    'tags': '',
                    'difficulty': 'Intermediate',
                    'topic': 'Sample'
                }
                
                insert_or_update_session(session_data)
                print(f"  ✅ Added: {sample['work_item_name']}")
        except Exception as e:
            print(f"  ❌ Error adding sample: {e}")

def show_migration_summary():
    """Show summary of migrated data"""
    print("\n📈 Migration Summary:")
    
    con = sqlite3.connect("learning_tracker.db")
    cur = con.cursor()
    
    # Count items by language and type
    cur.execute("""
        SELECT language_code, type, COUNT(*) 
        FROM items 
        WHERE is_active=1 
        GROUP BY language_code, type
        ORDER BY language_code, type
    """)
    
    print("\n📚 Items by Language & Type:")
    for lang, item_type, count in cur.fetchall():
        print(f"  {lang.title()} {item_type}s: {count}")
    
    # Count total sessions
    cur.execute("SELECT COUNT(*) FROM sessions")
    total_sessions = cur.fetchone()[0]
    print(f"\n📝 Total Sessions: {total_sessions}")
    
    # Recent activity
    cur.execute("""
        SELECT date, COUNT(*) 
        FROM sessions 
        WHERE date >= date('now', '-7 days')
        GROUP BY date 
        ORDER BY date DESC
    """)
    
    recent = cur.fetchall()
    if recent:
        print("\n📅 Recent Activity (last 7 days):")
        for date, count in recent:
            print(f"  {date}: {count} sessions")
    
    con.close()

if __name__ == "__main__":
    print("🚀 Enhanced Learning Tracker Migration")
    print("=" * 40)
    
    try:
        # Run migration
        migrate_database()
        
        # Ask about sample data
        response = input("\n❓ Would you like to add some sample data to test the new features? (y/N): ")
        if response.lower().startswith('y'):
            create_sample_data()
        
        # Show summary
        show_migration_summary()
        
        print("\n🎉 All done! You can now run the enhanced learning tracker:")
        print("   python -m app.main")
        
    except KeyboardInterrupt:
        print("\n❌ Migration cancelled by user")
    except Exception as e:
        print(f"\n💥 Migration failed: {e}")
        print("Please check your database and try again.")