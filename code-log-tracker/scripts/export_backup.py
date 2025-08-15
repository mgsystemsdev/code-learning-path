"""
Export and backup data from Supabase to local files.
"""

import os
import json
import csv
import pandas as pd
from datetime import datetime
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseBackup:
    """Handle Supabase data export and backup operations."""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not self.url or not self.service_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in environment")
        
        self.supabase = create_client(self.url, self.service_key)
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def export_table_to_csv(self, table_name: str, filename: str = None) -> str:
        """Export a table to CSV file."""
        try:
            # Get all data from table
            response = self.supabase.table(table_name).select("*").execute()
            
            if not response.data:
                print(f"⚠️  No data found in table '{table_name}'")
                return None
            
            # Create filename
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{table_name}_{timestamp}.csv"
            
            filepath = self.backup_dir / filename
            
            # Convert to DataFrame and export
            df = pd.DataFrame(response.data)
            df.to_csv(filepath, index=False)
            
            print(f"✅ Exported {len(response.data)} records from '{table_name}' to {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error exporting table '{table_name}': {e}")
            return None
    
    def export_all_tables(self) -> dict:
        """Export all main tables."""
        tables = ["languages", "items", "sessions", "config"]
        results = {}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for table in tables:
            filename = f"{table}_{timestamp}.csv"
            filepath = self.export_table_to_csv(table, filename)
            results[table] = filepath
        
        return results
    
    def create_full_backup(self) -> str:
        """Create a complete backup with metadata."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = self.backup_dir / f"full_backup_{timestamp}"
        backup_folder.mkdir(exist_ok=True)
        
        print(f"📦 Creating full backup in {backup_folder}")
        
        # Export each table
        tables = ["languages", "items", "sessions", "config"]
        backup_info = {
            "backup_date": datetime.now().isoformat(),
            "tables": {},
            "stats": {}
        }
        
        for table in tables:
            try:
                response = self.supabase.table(table).select("*").execute()
                
                if response.data:
                    # Save as CSV
                    csv_file = backup_folder / f"{table}.csv"
                    df = pd.DataFrame(response.data)
                    df.to_csv(csv_file, index=False)
                    
                    # Save as JSON
                    json_file = backup_folder / f"{table}.json"
                    with open(json_file, 'w') as f:
                        json.dump(response.data, f, indent=2, default=str)
                    
                    backup_info["tables"][table] = {
                        "csv_file": str(csv_file),
                        "json_file": str(json_file),
                        "record_count": len(response.data)
                    }
                    
                    backup_info["stats"][table] = len(response.data)
                    
                    print(f"✅ Backed up {table}: {len(response.data)} records")
                else:
                    print(f"⚠️  No data in table '{table}'")
                    backup_info["tables"][table] = {"record_count": 0}
                    backup_info["stats"][table] = 0
                    
            except Exception as e:
                print(f"❌ Error backing up table '{table}': {e}")
                backup_info["tables"][table] = {"error": str(e)}
        
        # Save backup metadata
        metadata_file = backup_folder / "backup_info.json"
        with open(metadata_file, 'w') as f:
            json.dump(backup_info, f, indent=2)
        
        print(f"📋 Backup metadata saved to {metadata_file}")
        print(f"🎉 Full backup completed: {backup_folder}")
        
        return str(backup_folder)
    
    def export_user_data(self, user_id: str) -> str:
        """Export data for a specific user."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_folder = self.backup_dir / f"user_{user_id[:8]}_{timestamp}"
        user_folder.mkdir(exist_ok=True)
        
        print(f"👤 Exporting data for user {user_id}")
        
        # Export user-specific data
        tables_with_user_filter = ["languages", "items", "sessions", "config"]
        
        for table in tables_with_user_filter:
            try:
                response = (
                    self.supabase.table(table)
                    .select("*")
                    .eq("user_id", user_id)
                    .execute()
                )
                
                if response.data:
                    # Save as CSV
                    csv_file = user_folder / f"{table}.csv"
                    df = pd.DataFrame(response.data)
                    df.to_csv(csv_file, index=False)
                    
                    print(f"✅ Exported user {table}: {len(response.data)} records")
                else:
                    print(f"⚠️  No {table} data for user")
                    
            except Exception as e:
                print(f"❌ Error exporting user {table}: {e}")
        
        return str(user_folder)
    
    def get_backup_stats(self) -> dict:
        """Get statistics about available backups."""
        if not self.backup_dir.exists():
            return {"message": "No backups found"}
        
        backups = []
        for backup_path in self.backup_dir.iterdir():
            if backup_path.is_dir() and "backup" in backup_path.name:
                metadata_file = backup_path / "backup_info.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        backups.append({
                            "folder": backup_path.name,
                            "date": metadata.get("backup_date"),
                            "stats": metadata.get("stats", {})
                        })
        
        return {
            "total_backups": len(backups),
            "backups": sorted(backups, key=lambda x: x["date"], reverse=True)
        }

def main():
    """Main backup operations."""
    print("🎓 Smart Learning Tracker - Supabase Backup Tool")
    print("=" * 50)
    
    try:
        backup = SupabaseBackup()
        
        print("\nSelect backup option:")
        print("1. Export single table")
        print("2. Export all tables")
        print("3. Create full backup")
        print("4. Export user data")
        print("5. Show backup statistics")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            table_name = input("Enter table name (languages/items/sessions/config): ").strip()
            backup.export_table_to_csv(table_name)
            
        elif choice == "2":
            results = backup.export_all_tables()
            print(f"\n✅ Exported {len(results)} tables")
            
        elif choice == "3":
            backup_path = backup.create_full_backup()
            print(f"\n🎉 Full backup created: {backup_path}")
            
        elif choice == "4":
            user_id = input("Enter user ID: ").strip()
            user_path = backup.export_user_data(user_id)
            print(f"\n✅ User data exported: {user_path}")
            
        elif choice == "5":
            stats = backup.get_backup_stats()
            print(f"\n📊 Backup Statistics:")
            print(json.dumps(stats, indent=2))
            
        else:
            print("❌ Invalid choice")
    
    except Exception as e:
        print(f"❌ Backup operation failed: {e}")

if __name__ == "__main__":
    main()
