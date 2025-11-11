"""
Quick validation script to check compliance engine setup
Run: python manage.py shell < compliance/validate_setup.py
Or: python -c "import django; django.setup(); exec(open('compliance/validate_setup.py').read())"
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truconn.settings')
django.setup()

from django.apps import apps
from django.urls import get_resolver
from compliance.models import ComplianceAudit, ViolationReport
from compliance.rules_engine import NDPRRulesEngine
from compliance.views import ComplianceScanView, ComplianceReportsView
from compliance.serializers import ComplianceAuditSerializer, ViolationReportSerializer

def check_models():
    """Check if models are registered"""
    print("🔍 Checking Models...")
    try:
        assert apps.is_installed('compliance'), "❌ Compliance app not in INSTALLED_APPS"
        assert ComplianceAudit in apps.get_app_config('compliance').models.values(), "❌ ComplianceAudit model not found"
        assert ViolationReport in apps.get_app_config('compliance').models.values(), "❌ ViolationReport model not found"
        print("✅ Models are registered correctly")
        return True
    except AssertionError as e:
        print(f"❌ {e}")
        return False

def check_urls():
    """Check if URLs are configured"""
    print("\n🔍 Checking URLs...")
    try:
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
        
        expected_paths = ['/api/compliance/scan/', '/api/compliance/reports/', '/api/compliance/audit/']
        found_paths = [p for p in compliance_paths if any(exp in p for exp in expected_paths)]
        
        if len(found_paths) >= 2:
            print(f"✅ Compliance URLs found: {len(found_paths)} paths")
            for path in found_paths:
                print(f"   - {path}")
            return True
        else:
            print("❌ Compliance URLs not found")
            return False
    except Exception as e:
        print(f"❌ Error checking URLs: {e}")
        return False

def check_rules_engine():
    """Check if rules engine is functional"""
    print("\n🔍 Checking Rules Engine...")
    try:
        assert hasattr(NDPRRulesEngine, 'RULES'), "❌ RULES not defined"
        assert len(NDPRRulesEngine.RULES) >= 8, f"❌ Expected 8+ rules, found {len(NDPRRulesEngine.RULES)}"
        assert hasattr(NDPRRulesEngine, 'run_all_checks'), "❌ run_all_checks method not found"
        assert hasattr(NDPRRulesEngine, 'calculate_risk_score'), "❌ calculate_risk_score method not found"
        
        # Check all required rules exist
        required_rules = ['CONSENT_VALIDITY', 'REVOCATION_HANDLING', 'PURPOSE_LIMITATION']
        for rule in required_rules:
            assert rule in NDPRRulesEngine.RULES, f"❌ Required rule {rule} not found"
        
        print(f"✅ Rules engine is functional ({len(NDPRRulesEngine.RULES)} rules)")
        return True
    except AssertionError as e:
        print(f"❌ {e}")
        return False

def check_serializers():
    """Check if serializers exist"""
    print("\n🔍 Checking Serializers...")
    try:
        assert ComplianceAuditSerializer, "❌ ComplianceAuditSerializer not found"
        assert ViolationReportSerializer, "❌ ViolationReportSerializer not found"
        print("✅ Serializers are defined")
        return True
    except AssertionError as e:
        print(f"❌ {e}")
        return False

def check_views():
    """Check if views exist"""
    print("\n🔍 Checking Views...")
    try:
        assert ComplianceScanView, "❌ ComplianceScanView not found"
        assert ComplianceReportsView, "❌ ComplianceReportsView not found"
        assert hasattr(ComplianceScanView, 'post'), "❌ ComplianceScanView.post not found"
        assert hasattr(ComplianceScanView, 'get'), "❌ ComplianceScanView.get not found"
        print("✅ Views are properly set up")
        return True
    except AssertionError as e:
        print(f"❌ {e}")
        return False

def check_database():
    """Check if database tables exist"""
    print("\n🔍 Checking Database...")
    try:
        from django.db import connection
        cursor = connection.cursor()
        
        # Check if tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('compliance_complianceaudit', 'compliance_violationreport')
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'compliance_complianceaudit' in tables and 'compliance_violationreport' in tables:
            print("✅ Database tables exist")
            return True
        else:
            print(f"❌ Database tables not found. Found: {tables}")
            print("   Run: python manage.py migrate compliance")
            return False
    except Exception as e:
        print(f"⚠️  Could not check database: {e}")
        print("   This is OK if using PostgreSQL or migrations not run yet")
        return None

def main():
    """Run all checks"""
    print("=" * 60)
    print("NDPR Compliance Engine - Setup Validation")
    print("=" * 60)
    
    results = []
    results.append(check_models())
    results.append(check_urls())
    results.append(check_rules_engine())
    results.append(check_serializers())
    results.append(check_views())
    db_result = check_database()
    if db_result is not None:
        results.append(db_result)
    
    print("\n" + "=" * 60)
    passed = sum([r for r in results if r is True])
    total = len([r for r in results if r is not None])
    
    if passed == total:
        print("✅ ALL CHECKS PASSED - Compliance engine is ready!")
        print("\nNext steps:")
        print("1. Run migrations: python manage.py migrate compliance")
        print("2. Start server: python manage.py runserver")
        print("3. Test endpoints: See TEST_COMPLIANCE_ENGINE.md")
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("\nPlease fix the issues above before proceeding.")
    
    print("=" * 60)

if __name__ == '__main__':
    main()

