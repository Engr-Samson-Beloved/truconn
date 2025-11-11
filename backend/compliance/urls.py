from django.urls import path
from .views import ComplianceScanView, ComplianceReportsView, ComplianceAuditDetailView

urlpatterns = [
    path('scan/', ComplianceScanView.as_view(), name='compliance-scan'),
    path('reports/', ComplianceReportsView.as_view(), name='compliance-reports'),
    path('reports/<int:org_id>/', ComplianceReportsView.as_view(), name='compliance-reports-org'),
    path('audit/<int:audit_id>/', ComplianceAuditDetailView.as_view(), name='compliance-audit-detail'),
]


