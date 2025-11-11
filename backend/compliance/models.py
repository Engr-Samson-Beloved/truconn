from django.db import models
from django.conf import settings
from organization.models import Org, AccessRequest
from django.utils import timezone
from datetime import timedelta


class ComplianceAudit(models.Model):
    """Stores compliance audit records for organizations"""
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('RESOLVED', 'Resolved'),
        ('INVESTIGATING', 'Under Investigation'),
        ('IGNORED', 'False Positive'),
    ]
    
    organization = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='compliance_audits')
    rule_name = models.CharField(max_length=200)
    rule_description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)  # Store rule-specific details
    recommendation = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-detected_at']
        indexes = [
            models.Index(fields=['organization', '-detected_at']),
            models.Index(fields=['status', 'severity']),
        ]
    
    def __str__(self):
        return f"{self.organization.name} - {self.rule_name} ({self.severity})"


class ViolationReport(models.Model):
    """Stores violation reports for regulatory compliance"""
    VIOLATION_TYPE_CHOICES = [
        ('CONSENT_VIOLATION', 'Consent Violation'),
        ('DATA_RETENTION', 'Data Retention Policy Violation'),
        ('ACCESS_CONTROL', 'Unauthorized Access'),
        ('PRIVACY_BREACH', 'Privacy Breach'),
        ('AUDIT_FAILURE', 'Audit Trail Failure'),
        ('PURPOSE_LIMITATION', 'Purpose Limitation Violation'),
    ]
    
    organization = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='violation_reports')
    violation_type = models.CharField(max_length=50, choices=VIOLATION_TYPE_CHOICES)
    description = models.TextField()
    affected_users_count = models.IntegerField(default=0)
    detected_at = models.DateTimeField(auto_now_add=True)
    reported_to_dpo = models.BooleanField(default=False)  # Data Protection Office
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    related_audit = models.ForeignKey(ComplianceAudit, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-detected_at']
        indexes = [
            models.Index(fields=['organization', '-detected_at']),
            models.Index(fields=['violation_type', 'resolved']),
        ]
    
    def __str__(self):
        return f"{self.organization.name} - {self.get_violation_type_display()} ({self.detected_at.date()})"

