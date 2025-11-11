from django.contrib import admin
from .models import ComplianceAudit, ViolationReport


@admin.register(ComplianceAudit)
class ComplianceAuditAdmin(admin.ModelAdmin):
    list_display = ['organization', 'rule_name', 'severity', 'status', 'detected_at']
    list_filter = ['severity', 'status', 'detected_at']
    search_fields = ['organization__name', 'rule_name', 'rule_description']
    readonly_fields = ['detected_at']
    ordering = ['-detected_at']


@admin.register(ViolationReport)
class ViolationReportAdmin(admin.ModelAdmin):
    list_display = ['organization', 'violation_type', 'resolved', 'detected_at', 'reported_to_dpo']
    list_filter = ['violation_type', 'resolved', 'reported_to_dpo', 'detected_at']
    search_fields = ['organization__name', 'description']
    readonly_fields = ['detected_at']
    ordering = ['-detected_at']


