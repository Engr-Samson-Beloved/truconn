"""
Test script to verify compliance engine setup
Run this after migrations are applied: python manage.py test compliance.test_compliance_setup
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from organization.models import Org
from compliance.models import ComplianceAudit, ViolationReport
from compliance.rules_engine import NDPRRulesEngine
from compliance.views import ComplianceScanView, ComplianceReportsView
from compliance.serializers import ComplianceAuditSerializer, ViolationReportSerializer

User = get_user_model()


class ComplianceSetupTestCase(TestCase):
    """Test that compliance engine is properly set up"""
    
    def setUp(self):
        """Create test data"""
        # Create organization user
        self.org_user = User.objects.create_user(
            email='testorg@example.com',
            password='testpass123',
            user_role='ORGANIZATION',
            first_name='Test',
            last_name='Org'
        )
        
        # Create organization
        self.org = Org.objects.create(
            user=self.org_user,
            name='Test Organization',
            email='testorg@example.com',
            address='123 Test St'
        )
    
    def test_models_exist(self):
        """Test that compliance models exist"""
        self.assertTrue(hasattr(ComplianceAudit, '_meta'))
        self.assertTrue(hasattr(ViolationReport, '_meta'))
    
    def test_can_create_audit(self):
        """Test creating a compliance audit"""
        audit = ComplianceAudit.objects.create(
            organization=self.org,
            rule_name='Test Rule',
            rule_description='Test Description',
            severity='HIGH',
            status='PENDING',
            recommendation='Test recommendation'
        )
        self.assertIsNotNone(audit.id)
        self.assertEqual(audit.organization, self.org)
    
    def test_can_create_violation_report(self):
        """Test creating a violation report"""
        audit = ComplianceAudit.objects.create(
            organization=self.org,
            rule_name='Test Rule',
            rule_description='Test Description',
            severity='CRITICAL',
            status='PENDING'
        )
        
        violation = ViolationReport.objects.create(
            organization=self.org,
            violation_type='CONSENT_VIOLATION',
            description='Test violation',
            related_audit=audit
        )
        self.assertIsNotNone(violation.id)
        self.assertEqual(violation.related_audit, audit)
    
    def test_rules_engine_exists(self):
        """Test that rules engine exists and has all rules"""
        self.assertTrue(hasattr(NDPRRulesEngine, 'RULES'))
        self.assertIn('CONSENT_VALIDITY', NDPRRulesEngine.RULES)
        self.assertIn('REVOCATION_HANDLING', NDPRRulesEngine.RULES)
        self.assertIn('PURPOSE_LIMITATION', NDPRRulesEngine.RULES)
    
    def test_rules_engine_can_run_checks(self):
        """Test that rules engine can run checks"""
        result = NDPRRulesEngine.run_all_checks(self.org)
        self.assertIn('risk_score', result)
        self.assertIn('total_violations', result)
        self.assertIn('violations', result)
        self.assertIsInstance(result['risk_score'], int)
        self.assertGreaterEqual(result['risk_score'], 0)
        self.assertLessEqual(result['risk_score'], 100)
    
    def test_serializers_exist(self):
        """Test that serializers exist"""
        audit = ComplianceAudit.objects.create(
            organization=self.org,
            rule_name='Test Rule',
            rule_description='Test Description',
            severity='MEDIUM'
        )
        
        serializer = ComplianceAuditSerializer(audit)
        self.assertIn('id', serializer.data)
        self.assertIn('rule_name', serializer.data)
        self.assertIn('severity', serializer.data)
    
    def test_views_exist(self):
        """Test that views exist"""
        self.assertTrue(hasattr(ComplianceScanView, 'post'))
        self.assertTrue(hasattr(ComplianceScanView, 'get'))
        self.assertTrue(hasattr(ComplianceReportsView, 'get'))


