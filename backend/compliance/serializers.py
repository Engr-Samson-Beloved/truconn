from rest_framework import serializers
from .models import ComplianceAudit, ViolationReport


class ComplianceAuditSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = ComplianceAudit
        fields = [
            'id', 'organization', 'organization_name', 'rule_name', 
            'rule_description', 'severity', 'status', 'detected_at', 
            'resolved_at', 'details', 'recommendation'
        ]
        read_only_fields = ['detected_at']


class ViolationReportSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    violation_type_display = serializers.CharField(source='get_violation_type_display', read_only=True)
    
    class Meta:
        model = ViolationReport
        fields = [
            'id', 'organization', 'organization_name', 'violation_type',
            'violation_type_display', 'description', 'affected_users_count',
            'detected_at', 'reported_to_dpo', 'resolved', 'resolution_notes',
            'related_audit'
        ]
        read_only_fields = ['detected_at']


class ComplianceScanResultSerializer(serializers.Serializer):
    """Serializer for compliance scan results"""
    risk_score = serializers.IntegerField()
    total_violations = serializers.IntegerField()
    critical_count = serializers.IntegerField()
    high_count = serializers.IntegerField()
    medium_count = serializers.IntegerField()
    violations = serializers.ListField()
    audit_records = ComplianceAuditSerializer(many=True, read_only=True)

