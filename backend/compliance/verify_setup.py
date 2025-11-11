"""
Verification script for compliance module setup
Run this to verify the compliance engine is properly configured
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truconn.settings')
django.setup()

from django.apps import apps
from django.urls import get_resolver
from compliance.models import ComplianceAudit, ViolationReport
from compliance.rules_engine import NDPRRulesEngine


def verify_models():
    """Verify compliance models are registered"""
    print("✓ Checking models...")
    try:
        assert apps.is_installed('compliance'), "Compliance app not in INSTALLED_APPS"
        assert ComplianceAudit in apps.get_app_config('compliance').models.values(), "ComplianceAudit model not found"
        assert ViolationReport in apps.get_app_config('compliance').models.values(), "ViolationReport model not found"
        print("  ✓ Models registered correctly")
        return True
    except Exception as e:
        print(f"  ✗ Model verification failed: {e}")
        return False


def verify_urls():
    """Verify compliance URLs are registered"""
    print("✓ Checking URLs...")
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
        
        if found_paths:
            print(f"  ✓ Compliance URLs found: {len(found_paths)} paths")
            return True
        else:
            print("  ✗ Compliance URLs not found")
            return False
    except Exception as e:
        print(f"  ✗ URL verification failed: {e}")
        return False


def verify_rules_engine():
    """Verify rules engine is functional"""
    print("✓ Checking rules engine...")
    try:
        assert hasattr(NDPRRulesEngine, 'RULES'), "RULES not defined"
        assert len(NDPRRulesEngine.RULES) >= 8, f"Expected at least 8 rules, found {len(NDPRRulesEngine.RULES)}"
        assert hasattr(NDPRRulesEngine, 'run_all_checks'), "run_all_checks method not found"
        assert hasattr(NDPRRulesEngine, 'calculate_risk_score'), "calculate_risk_score method not found"
        assert hasattr(NDPRRulesEngine, 'create_audit_records'), "create_audit_records method not found"
        
        # Test risk score calculation
        test_violations = [
            {'rule': 'REVOCATION_HANDLING', 'details': {}},
            {'rule': 'CONSENT_VALIDITY', 'details': {}},
        ]
        score = NDPRRulesEngine.calculate_risk_score(test_violations)
        assert isinstance(score, int), "Risk score should be integer"
        assert 0 <= score <= 100, "Risk score should be between 0 and 100"
        
        print(f"  ✓ Rules engine functional ({len(NDPRRulesEngine.RULES)} rules)")
        print(f"  ✓ Risk score calculation working (test score: {score})")
        return True
    except Exception as e:
        print(f"  ✗ Rules engine verification failed: {e}")
        return False


def verify_serializers():
    """Verify serializers are properly defined"""
    print("✓ Checking serializers...")
    try:
        from compliance.serializers import (
            ComplianceAuditSerializer,
            ViolationReportSerializer,
            ComplianceScanResultSerializer
        )
        
        assert ComplianceAuditSerializer, "ComplianceAuditSerializer not found"
        assert ViolationReportSerializer, "ViolationReportSerializer not found"
        assert ComplianceScanResultSerializer, "ComplianceScanResultSerializer not found"
        
        print("  ✓ All serializers defined")
        return True
    except Exception as e:
        print(f"  ✗ Serializer verification failed: {e}")
        return False


def verify_views():
    """Verify views are properly defined"""
    print("✓ Checking views...")
    try:
        from compliance.views import (
            ComplianceScanView,
            ComplianceReportsView,
            ComplianceAuditDetailView
        )
        
        assert ComplianceScanView, "ComplianceScanView not found"
        assert ComplianceReportsView, "ComplianceReportsView not found"
        assert ComplianceAuditDetailView, "ComplianceAuditDetailView not found"
        
        print("  ✓ All views defined")
        return True
    except Exception as e:
        print(f"  ✗ View verification failed: {e}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("NDPR Compliance Engine - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        verify_models,
        verify_urls,
        verify_rules_engine,
        verify_serializers,
        verify_views,
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Check failed with exception: {e}")
            results.append(False)
        print()
    
    print("=" * 60)
    if all(results):
        print("✓ ALL CHECKS PASSED - Compliance engine is ready!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run migrations: python manage.py makemigrations compliance")
        print("2. Apply migrations: python manage.py migrate")
        print("3. Test the API endpoints")
        return 0
    else:
        print("✗ SOME CHECKS FAILED - Please review errors above")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())


