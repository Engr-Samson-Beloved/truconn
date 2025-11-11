from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from organization.models import Org
from organization.permissions import IsOrganization
from .rules_engine import NDPRRulesEngine
from .models import ComplianceAudit, ViolationReport
from .serializers import (
    ComplianceAuditSerializer, 
    ViolationReportSerializer,
    ComplianceScanResultSerializer
)
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone


class ComplianceScanView(APIView):
    """Run compliance scan for an organization"""
    permission_classes = [IsAuthenticated, IsOrganization]
    
    def post(self, request):
        """Run full compliance scan"""
        try:
            organization = get_object_or_404(Org, user=request.user)
            
            # Run compliance checks
            scan_result = NDPRRulesEngine.run_all_checks(organization)
            
            # Create audit records
            audit_records = NDPRRulesEngine.create_audit_records(organization, scan_result)
            
            # Serialize audit records
            audit_serializer = ComplianceAuditSerializer(audit_records, many=True)
            
            # Prepare response data
            result_data = {
                'risk_score': scan_result['risk_score'],
                'total_violations': scan_result['total_violations'],
                'critical_count': scan_result['critical_count'],
                'high_count': scan_result['high_count'],
                'medium_count': scan_result['medium_count'],
                'violations': scan_result['violations'],
                'audit_records': audit_serializer.data,
            }
            
            serializer = ComplianceScanResultSerializer(result_data)
            return Response({
                'message': 'Compliance scan completed successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Compliance scan failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """Get latest compliance scan results"""
        try:
            organization = get_object_or_404(Org, user=request.user)
            
            # Get latest audit records (last 30 days)
            thirty_days_ago = timezone.now() - timedelta(days=30)
            audits = ComplianceAudit.objects.filter(
                organization=organization,
                detected_at__gte=thirty_days_ago
            ).order_by('-detected_at')
            
            # Calculate current risk score
            pending_audits = audits.filter(status='PENDING')
            if pending_audits.exists():
                # Map rule names back to rule keys for risk calculation
                rule_name_to_key = {v['name']: k for k, v in NDPRRulesEngine.RULES.items()}
                risk_score = NDPRRulesEngine.calculate_risk_score([
                    {
                        'rule': rule_name_to_key.get(audit.rule_name, 'UNKNOWN'),
                        'details': audit.details
                    }
                    for audit in pending_audits
                ])
            else:
                risk_score = 0
            
            # Count violations by severity
            critical_count = pending_audits.filter(severity='CRITICAL').count()
            high_count = pending_audits.filter(severity='HIGH').count()
            medium_count = pending_audits.filter(severity='MEDIUM').count()
            
            return Response({
                'risk_score': risk_score,
                'total_violations': pending_audits.count(),
                'critical_count': critical_count,
                'high_count': high_count,
                'medium_count': medium_count,
                'audits': ComplianceAuditSerializer(audits[:10], many=True).data,  # Latest 10
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve compliance data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ComplianceReportsView(APIView):
    """Get compliance reports for an organization"""
    permission_classes = [IsAuthenticated, IsOrganization]
    
    def get(self, request, org_id=None):
        """Get compliance reports"""
        try:
            # If org_id provided, check if user is admin or same org
            if org_id:
                organization = get_object_or_404(Org, pk=org_id)
                # For now, only allow own organization
                if organization.user != request.user and not request.user.is_staff:
                    return Response({
                        'error': 'Permission denied'
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                organization = get_object_or_404(Org, user=request.user)
            
            # Get audit records
            audits = ComplianceAudit.objects.filter(
                organization=organization
            ).order_by('-detected_at')
            
            # Get violation reports
            violations = ViolationReport.objects.filter(
                organization=organization
            ).order_by('-detected_at')
            
            # Calculate statistics
            total_audits = audits.count()
            pending_audits = audits.filter(status='PENDING').count()
            resolved_audits = audits.filter(status='RESOLVED').count()
            unresolved_violations = violations.filter(resolved=False).count()
            
            return Response({
                'organization': {
                    'id': organization.id,
                    'name': organization.name,
                },
                'statistics': {
                    'total_audits': total_audits,
                    'pending_audits': pending_audits,
                    'resolved_audits': resolved_audits,
                    'unresolved_violations': unresolved_violations,
                },
                'audits': ComplianceAuditSerializer(audits, many=True).data,
                'violations': ViolationReportSerializer(violations, many=True).data,
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve compliance reports: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ComplianceAuditDetailView(APIView):
    """Manage individual compliance audit records"""
    permission_classes = [IsAuthenticated, IsOrganization]
    
    def get(self, request, audit_id):
        """Get audit details"""
        try:
            organization = get_object_or_404(Org, user=request.user)
            audit = get_object_or_404(
                ComplianceAudit, 
                pk=audit_id, 
                organization=organization
            )
            
            serializer = ComplianceAuditSerializer(audit)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve audit: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, audit_id):
        """Update audit status (e.g., mark as resolved)"""
        try:
            organization = get_object_or_404(Org, user=request.user)
            audit = get_object_or_404(
                ComplianceAudit,
                pk=audit_id,
                organization=organization
            )
            
            # Update status
            new_status = request.data.get('status')
            if new_status in dict(ComplianceAudit.STATUS_CHOICES).keys():
                audit.status = new_status
                if new_status == 'RESOLVED':
                    audit.resolved_at = timezone.now()
                audit.save()
            
            serializer = ComplianceAuditSerializer(audit)
            return Response({
                'message': 'Audit updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to update audit: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

