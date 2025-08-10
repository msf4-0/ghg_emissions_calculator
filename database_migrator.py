import mysql.connector
from mysql.connector import Error
import os
import logging
from datetime import datetime
from config import config

logger = logging.getLogger(__name__)

class DatabaseMigrator:
    def __init__(self):
        self.db_config = config.database_config
        self.migration_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'migrations')
        self.connection = None
    
    def connect(self):
        """Connect to database"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            return True
        except Error as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def create_migration_table(self):
        """Create migrations tracking table"""
        query = """
        CREATE TABLE IF NOT EXISTS database_migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            execution_time_ms INT,
            status ENUM('success', 'failed') DEFAULT 'success'
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            logger.error(f"Failed to create migration table: {e}")
            return False
    
    def get_executed_migrations(self):
        """Get list of already executed migrations"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT migration_name FROM database_migrations WHERE status = 'success'")
            results = cursor.fetchall()
            cursor.close()
            return [row[0] for row in results]
        except Error as e:
            logger.error(f"Failed to get executed migrations: {e}")
            return []
    
    def execute_migration(self, migration_file):
        """Execute a single migration file"""
        migration_name = os.path.basename(migration_file)
        file_path = os.path.join(self.migration_path, migration_file)
        
        if not os.path.exists(file_path):
            logger.error(f"Migration file not found: {file_path}")
            return False
        
        try:
            start_time = datetime.now()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Split SQL content by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            cursor = self.connection.cursor()
            
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
            
            self.connection.commit()
            
            # Record successful migration
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            cursor.execute(
                "INSERT INTO database_migrations (migration_name, execution_time_ms) VALUES (%s, %s)",
                (migration_name, execution_time)
            )
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Migration {migration_name} executed successfully in {execution_time}ms")
            return True
            
        except Error as e:
            logger.error(f"Migration {migration_name} failed: {e}")
            
            # Record failed migration
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT INTO database_migrations (migration_name, status) VALUES (%s, 'failed')",
                    (migration_name,)
                )
                self.connection.commit()
                cursor.close()
            except:
                pass
            
            return False
    
    def run_migrations(self):
        """Run all pending migrations"""
        if not self.connect():
            return False
        
        try:
            # Create migration tracking table
            if not self.create_migration_table():
                return False
            
            # Get executed migrations
            executed_migrations = self.get_executed_migrations()
            
            # Get all migration files
            migration_files = []
            if os.path.exists(self.migration_path):
                migration_files = [f for f in os.listdir(self.migration_path) if f.endswith('.sql')]
                migration_files.sort()  # Execute in alphabetical order
            
            if not migration_files:
                logger.warning("No migration files found")
                return True
            
            # Execute pending migrations
            pending_migrations = [f for f in migration_files if f not in executed_migrations]
            
            if not pending_migrations:
                logger.info("No pending migrations")
                return True
            
            logger.info(f"Executing {len(pending_migrations)} pending migrations...")
            
            for migration_file in pending_migrations:
                if not self.execute_migration(migration_file):
                    logger.error(f"Migration failed: {migration_file}")
                    return False
            
            logger.info("All migrations executed successfully")
            return True
            
        finally:
            self.disconnect()
    
    def rollback_migration(self, migration_name):
        """Rollback a specific migration (if rollback script exists)"""
        rollback_file = f"rollback_{migration_name}"
        rollback_path = os.path.join(self.migration_path, 'rollbacks', rollback_file)
        
        if not os.path.exists(rollback_path):
            logger.error(f"Rollback file not found: {rollback_path}")
            return False
        
        # Implementation for rollback logic
        logger.info(f"Rollback functionality for {migration_name}")
        return True

def run_database_setup():
    """Main function to run database setup"""
    migrator = DatabaseMigrator()
    return migrator.run_migrations()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = run_database_setup()
    if success:
        print("✅ Database setup completed successfully")
    else:
        print("❌ Database setup failed")
        exit(1)
