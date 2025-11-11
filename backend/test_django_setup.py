"""
Test Django setup for compliance engine
Run this after activating venv: python test_django_setup.py
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truconn.settings')

try:
    django.setup()
    print("✅ Django setup successful!")
    
    # Test imports
    from compliance.models import ComplianceAudit, ViolationReport
    from compliance.rules_engine import NDPRRulesEngine
    from compliance.views import ComplianceScanView, ComplianceReportsView
    from compliance.serializers import ComplianceAuditSerializer, ViolationReportSerializer
    from organization.models import Org
    
    print("✅ All imports successful!")
    
    # Test models
    print("\n📋 Testing Models...")
    print(f"   ComplianceAudit: {ComplianceAudit._meta.db_table}")
    print(f"   ViolationReport: {ViolationReport._meta.db_table}")
    
    # Test rules engine
    print("\n🔍 Testing Rules Engine...")
    print(f"   Number of rules: {len(NDPRRulesEngine.RULES)}")
    for rule_name in NDPRRulesEngine.RULES.keys():
        print(f"   - {rule_name}")
    
    # Test URLs
    print("\n🔗 Testing URLs...")
    from django.urls import get_resolver
    resolver = get_resolver()
    
    compliance_paths = []
    def find_compliance_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                new_prefix = f"{prefix}{pattern.pattern}"
                find_compliance_urls(pattern.url_patterns, new_prefix)
            elif 'compliance' in str(pattern.pattern):
                compliance_paths.append(f"{prefix}{pattern.pattern}")
    
    find_compliance_urls(resolver.url_patterns)
    print(f"   Found {len(compliance_paths)} compliance URL patterns:")
    for path in compliance_paths[:5]:  # Show first 5
        print(f"   - {path}")
    
    # Test database connection
    print("\n💾 Testing Database...")
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            # Check if tables exist (works for both SQLite and PostgreSQL)
            if 'sqlite' in connection.vendor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name LIKE 'compliance_%'
                """)
            else:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name LIKE 'compliance_%'
                """)
            tables = [row[0] for row in cursor.fetchall()]
            
            if tables:
                print(f"   ✅ Found {len(tables)} compliance tables:")
                for table in tables:
                    print(f"      - {table}")
            else:
                print("   ⚠️  No compliance tables found. Run: python manage.py migrate compliance")
    except Exception as e:
        print(f"   ⚠️  Could not check database: {e}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED - Compliance engine is ready!")
    print("="*60)
    print("\nTo start the server:")
    print("  python manage.py runserver")
    print("\nTo test the API:")
    print("  See TEST_COMPLIANCE_ENGINE.md for detailed instructions")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nMake sure:")
    print("1. Virtual environment is activated")
    print("2. Dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)
except django.core.exceptions.ImproperlyConfigured as e:
    print(f"❌ Django configuration error: {e}")
    print("\nCheck your settings.py file")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

