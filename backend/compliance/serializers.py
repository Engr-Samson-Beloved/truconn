from rest_framework import serializers
from .models import ComplianceAudit, ViolationReport


# For saved objects (DB model instances)
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


class ViolationReportModelSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    violation_type_display = serializers.CharField(source='get_violation_type_display', read_only=True)
    related_audit_name = serializers.CharField(source='related_audit.rule_name', read_only=True)

    class Meta:
        model = ViolationReport
        fields = [
            'id', 'organization', 'organization_name', 'violation_type',
            'violation_type_display', 'description', 'affected_users_count',
            'detected_at', 'reported_to_dpo', 'resolved', 'resolution_notes',
            'related_audit', 'related_audit_name'
        ]
        read_only_fields = ['detected_at']


# For compliance scan results (possibly unsaved dicts)
class ComplianceScanResultSerializer(serializers.Serializer):
    risk_score = serializers.IntegerField()
    total_violations = serializers.IntegerField()
    critical_count = serializers.IntegerField()
    high_count = serializers.IntegerField()
    medium_count = serializers.IntegerField()
    
    # Use plain Serializer for dicts to avoid KeyError
    violations = serializers.ListField(
        child=serializers.DictField(),  # expects a list of dicts, not model instances
        read_only=True
    )
    
    audit_records = serializers.ListField(
        child=serializers.DictField(),
        read_only=True
    )
