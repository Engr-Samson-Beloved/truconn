"""
Tests for compliance module
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from organization.models import Org
from compliance.models import ComplianceAudit, ViolationReport
from compliance.rules_engine import NDPRRulesEngine

User = get_user_model()


class ComplianceRulesEngineTestCase(TestCase):
    """Test NDPR compliance rules engine"""
    
    def setUp(self):
        """Set up test data"""
        # Create test organization user
        self.org_user = User.objects.create_user(
            email='org@test.com',
            password='testpass123',
            user_role='ORGANIZATION'
        )
        
        # Create organization
        self.org = Org.objects.create(
            user=self.org_user,
            name='Test Organization',
            email='org@test.com',
            address='123 Test St'
        )
    
    def test_risk_score_calculation(self):
        """Test risk score calculation"""
        violations = [
            {'rule': 'REVOCATION_HANDLING', 'details': {}},  # CRITICAL
            {'rule': 'CONSENT_VALIDITY', 'details': {}},  # HIGH
            {'rule': 'DATA_MINIMIZATION', 'details': {}},  # MEDIUM
        ]
        
        score = NDPRRulesEngine.calculate_risk_score(violations)
        # CRITICAL (20) + HIGH (15) + MEDIUM (10) = 45
        self.assertEqual(score, 45)
    
    def test_empty_violations_risk_score(self):
        """Test risk score with no violations"""
        score = NDPRRulesEngine.calculate_risk_score([])
        self.assertEqual(score, 0)
    
    def test_risk_score_cap(self):
        """Test risk score caps at 100"""
        # Create many violations to exceed 100
        violations = [
            {'rule': 'REVOCATION_HANDLING', 'details': {}} for _ in range(10)
        ]
        score = NDPRRulesEngine.calculate_risk_score(violations)
        self.assertEqual(score, 100)  # Should cap at 100


class ComplianceModelsTestCase(TestCase):
    """Test compliance models"""
    
    def setUp(self):
        """Set up test data"""
        self.org_user = User.objects.create_user(
            email='org@test.com',
            password='testpass123',
            user_role='ORGANIZATION'
        )
        self.org = Org.objects.create(
            user=self.org_user,
            name='Test Organization',
            email='org@test.com',
            address='123 Test St'
        )
    
    def test_compliance_audit_creation(self):
        """Test creating compliance audit record"""
        audit = ComplianceAudit.objects.create(
            organization=self.org,
            rule_name='Test Rule',
            rule_description='Test description',
            severity='HIGH',
            details={'test': 'data'},
            recommendation='Test recommendation'
        )
        
        self.assertEqual(audit.organization, self.org)
        self.assertEqual(audit.severity, 'HIGH')
        self.assertEqual(audit.status, 'PENDING')
        self.assertIsNotNone(audit.detected_at)
    
    def test_violation_report_creation(self):
        """Test creating violation report"""
        audit = ComplianceAudit.objects.create(
            organization=self.org,
            rule_name='Test Rule',
            rule_description='Test',
            severity='CRITICAL'
        )
        
        violation = ViolationReport.objects.create(
            organization=self.org,
            violation_type='CONSENT_VIOLATION',
            description='Test violation',
            related_audit=audit,
            reported_to_dpo=True
        )
        
        self.assertEqual(violation.organization, self.org)
        self.assertTrue(violation.reported_to_dpo)
        self.assertFalse(violation.resolved)


