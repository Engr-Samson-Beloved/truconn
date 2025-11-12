"""
Verify that compliance migrations were applied successfully
Run: python verify_migrations.py (with venv activated)
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truconn.settings')
os.environ.setdefault('SECRET_KEY', 'dev-secret-key-for-verification')
os.environ.setdefault('DEBUG', 'True')

django.setup()

from django.db import connection
from compliance.models import ComplianceAudit, ViolationReport

def verify_tables():
    """Verify that compliance tables exist"""
    print("=" * 60)
    print("Verifying Compliance Migrations")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            # Check for PostgreSQL
            if 'postgresql' in connection.vendor:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name LIKE 'compliance_%'
                    ORDER BY table_name
                """)
            # Check for SQLite
            elif 'sqlite' in connection.vendor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name LIKE 'compliance_%'
                    ORDER BY name
                """)
            else:
                print(f"⚠️  Unsupported database: {connection.vendor}")
                return False
            
            tables = [row[0] for row in cursor.fetchall()]
            
            print(f"\n✅ Found {len(tables)} compliance table(s):")
            for table in tables:
                print(f"   - {table}")
            
            # Verify expected tables exist
            expected_tables = ['compliance_complianceaudit', 'compliance_violationreport']
            missing = [t for t in expected_tables if t not in tables]
            
            if missing:
                print(f"\n❌ Missing tables: {missing}")
                return False
            
            print("\n✅ All expected tables exist!")
            
            # Try to query the models
            print("\n📊 Testing model access...")
            audit_count = ComplianceAudit.objects.count()
            violation_count = ViolationReport.objects.count()
            
            print(f"   ComplianceAudit records: {audit_count}")
            print(f"   ViolationReport records: {violation_count}")
            
            print("\n" + "=" * 60)
            print("✅ MIGRATION VERIFICATION SUCCESSFUL!")
            print("=" * 60)
            print("\nThe compliance tables are ready to use.")
            print("You can now:")
            print("1. Restart your backend server")
            print("2. Test the compliance scanner at:")
            print("   http://localhost:3000/admin/organization/compliance")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error verifying tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = verify_tables()
    sys.exit(0 if success else 1)

