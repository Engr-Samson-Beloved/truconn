"""
Script to run trust score migrations
Run: python run_trust_migrations.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truconn.settings')

# Set default env vars if not set
if 'SECRET_KEY' not in os.environ:
    os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
if 'DEBUG' not in os.environ:
    os.environ['DEBUG'] = 'True'

django.setup()

from django.core.management import call_command
from django.db import connection

def run_migrations():
    """Run organization migrations"""
    print("=" * 60)
    print("Running Trust Score Migrations")
    print("=" * 60)
    
    try:
        # Run migrations
        print("\n📦 Running migrations...")
        call_command('migrate', 'organization', verbosity=2)
        
        # Verify columns exist
        print("\n✅ Verifying migrations...")
        with connection.cursor() as cursor:
            if 'postgresql' in connection.vendor:
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'organization_org' 
                    AND column_name LIKE 'trust_%'
                    ORDER BY column_name
                """)
            elif 'sqlite' in connection.vendor:
                cursor.execute("""
                    SELECT name FROM pragma_table_info('organization_org')
                    WHERE name LIKE 'trust_%'
                    ORDER BY name
                """)
            else:
                print("⚠️  Unsupported database type")
                return
            
            columns = [row[0] for row in cursor.fetchall()]
            
            expected_columns = [
                'trust_score',
                'trust_level',
                'trust_score_last_calculated',
                'trust_certificate_issued',
                'trust_certificate_issued_at'
            ]
            
            print(f"\n📊 Found {len(columns)} trust score columns:")
            for col in columns:
                print(f"   ✓ {col}")
            
            missing = [col for col in expected_columns if col not in columns]
            if missing:
                print(f"\n❌ Missing columns: {missing}")
                return False
            else:
                print("\n✅ All trust score columns exist!")
        
        # Check IntegrityRecord table
        print("\n📦 Checking IntegrityRecord table...")
        with connection.cursor() as cursor:
            if 'postgresql' in connection.vendor:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name = 'organization_integrityrecord'
                """)
            elif 'sqlite' in connection.vendor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='organization_integrityrecord'
                """)
            
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
                print("✅ IntegrityRecord table exists!")
            else:
                print("⚠️  IntegrityRecord table not found (may need migration)")
        
        print("\n" + "=" * 60)
        print("✅ MIGRATIONS COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Restart your backend server")
        print("2. Test the trust score system")
        print("3. Update existing organizations:")
        print("   python manage.py shell")
        print("   >>> from organization.models import Org")
        print("   >>> for org in Org.objects.all():")
        print("   ...     org.update_trust_score()")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_migrations()
    sys.exit(0 if success else 1)

