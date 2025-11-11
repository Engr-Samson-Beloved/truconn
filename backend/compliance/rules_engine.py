"""
NDPR Compliance Rules Engine
Implements automated checks based on Nigeria Data Protection Regulation
"""
from datetime import timedelta
from django.utils import timezone
from organization.models import AccessRequest, Org
from consents.models import UserConsent
from .models import ComplianceAudit, ViolationReport


class NDPRRulesEngine:
    """Engine for checking NDPR compliance rules"""
    
    # NDPR Rule Definitions
    RULES = {
        'CONSENT_VALIDITY': {
            'name': 'Consent Validity Check',
            'description': 'Ensures all data access has valid, explicit consent',
            'severity': 'HIGH',
        },
        'PURPOSE_LIMITATION': {
            'name': 'Purpose Limitation',
            'description': 'Data access must align with stated purpose',
            'severity': 'HIGH',
        },
        'DATA_MINIMIZATION': {
            'name': 'Data Minimization',
            'description': 'Organizations should only request necessary data',
            'severity': 'MEDIUM',
        },
        'RETENTION_POLICY': {
            'name': 'Data Retention Policy',
            'description': 'Data should not be retained beyond stated purpose',
            'severity': 'MEDIUM',
        },
        'ACCESS_CONTROL': {
            'name': 'Access Control',
            'description': 'Unauthorized access attempts detected',
            'severity': 'CRITICAL',
        },
        'AUDIT_TRAIL': {
            'name': 'Audit Trail Completeness',
            'description': 'All data access must be logged and auditable',
            'severity': 'HIGH',
        },
        'REVOCATION_HANDLING': {
            'name': 'Consent Revocation Handling',
            'description': 'Revoked consents must be respected immediately',
            'severity': 'CRITICAL',
        },
        'EXCESSIVE_REQUESTS': {
            'name': 'Excessive Data Requests',
            'description': 'Unusual pattern of data access requests detected',
            'severity': 'MEDIUM',
        },
    }
    
    @staticmethod
    def check_consent_validity(organization: Org) -> list:
        """Check if all approved access requests have valid consent"""
        violations = []
        approved_requests = AccessRequest.objects.filter(
            organization=organization,
            status='APPROVED'
        )
        
        for request in approved_requests:
            # Check if user still has consent granted
            user_consent = UserConsent.objects.filter(
                user=request.user,
                consent=request.consent,
                access=True
            ).first()
            
            if not user_consent:
                violations.append({
                    'rule': 'CONSENT_VALIDITY',
                    'details': {
                        'access_request_id': request.id,
                        'user_id': request.user.id,
                        'consent_type': request.consent.name,
                        'issue': 'Access approved but user consent revoked',
                    },
                    'recommendation': f'Revoke access request #{request.id} as user has revoked consent for {request.consent.name}',
                })
        
        return violations
    
    @staticmethod
    def check_purpose_limitation(organization: Org) -> list:
        """Check if data access purposes are clear and limited"""
        violations = []
        requests = AccessRequest.objects.filter(organization=organization)
        
        # Check for vague or missing purposes
        vague_purposes = ['general', 'testing', 'research', 'other', '']
        for request in requests:
            if request.purpose.lower() in vague_purposes or len(request.purpose.strip()) < 10:
                violations.append({
                    'rule': 'PURPOSE_LIMITATION',
                    'details': {
                        'access_request_id': request.id,
                        'purpose': request.purpose,
                        'issue': 'Purpose is too vague or insufficient',
                    },
                    'recommendation': 'Specify clear, specific purpose for data access (minimum 10 characters)',
                })
        
        return violations
    
    @staticmethod
    def check_data_minimization(organization: Org) -> list:
        """Check if organization requests excessive data types"""
        violations = []
        # Get unique users accessed
        unique_users = AccessRequest.objects.filter(
            organization=organization,
            status='APPROVED'
        ).values('user').distinct().count()
        
        # Get total consent types accessed
        consent_types = AccessRequest.objects.filter(
            organization=organization,
            status='APPROVED'
        ).values('consent').distinct().count()
        
        # Flag if accessing all 4 main consent types for same user (potential overreach)
        if unique_users > 0:
            avg_consents_per_user = consent_types / unique_users if unique_users > 0 else 0
            if avg_consents_per_user >= 3.5:  # Accessing 3.5+ consent types on average
                violations.append({
                    'rule': 'DATA_MINIMIZATION',
                    'details': {
                        'unique_users': unique_users,
                        'consent_types_accessed': consent_types,
                        'avg_consents_per_user': round(avg_consents_per_user, 2),
                        'issue': 'Accessing multiple data types per user may violate data minimization',
                    },
                    'recommendation': 'Review if all requested data types are necessary for stated purpose',
                })
        
        return violations
    
    @staticmethod
    def check_retention_policy(organization: Org) -> list:
        """Check for data retention policy violations"""
        violations = []
        # Check for old approved requests (assuming 1 year retention limit)
        one_year_ago = timezone.now() - timedelta(days=365)
        old_approved = AccessRequest.objects.filter(
            organization=organization,
            status='APPROVED',
            requested_at__lt=one_year_ago
        )
        
        if old_approved.exists():
            violations.append({
                'rule': 'RETENTION_POLICY',
                'details': {
                    'old_requests_count': old_approved.count(),
                    'oldest_request_date': old_approved.order_by('requested_at').first().requested_at.date().isoformat(),
                    'issue': f'{old_approved.count()} approved access requests older than 1 year',
                },
                'recommendation': 'Review and archive data access older than retention period (1 year)',
            })
        
        return violations
    
    @staticmethod
    def check_access_control(organization: Org) -> list:
        """Check for unauthorized access patterns"""
        violations = []
        # Check for revoked access that was previously approved
        revoked_after_approval = AccessRequest.objects.filter(
            organization=organization,
            status='REVOKED'
        )
        
        # Check if revoked access was used after revocation (would need access logs)
        # For now, flag if many revocations
        if revoked_after_approval.count() > 10:
            violations.append({
                'rule': 'ACCESS_CONTROL',
                'details': {
                    'revoked_count': revoked_after_approval.count(),
                    'issue': 'High number of revoked access requests may indicate access control issues',
                },
                'recommendation': 'Review access control policies and ensure revoked access is immediately enforced',
            })
        
        return violations
    
    @staticmethod
    def check_audit_trail(organization: Org) -> list:
        """Check audit trail completeness"""
        violations = []
        requests = AccessRequest.objects.filter(organization=organization)
        
        # Check for requests without proper purpose
        missing_purpose = requests.filter(purpose__isnull=True).count()
        if missing_purpose > 0:
            violations.append({
                'rule': 'AUDIT_TRAIL',
                'details': {
                    'missing_purpose_count': missing_purpose,
                    'issue': 'Some access requests lack purpose documentation',
                },
                'recommendation': 'Ensure all access requests have clear purpose documented',
            })
        
        return violations
    
    @staticmethod
    def check_revocation_handling(organization: Org) -> list:
        """Check if revoked consents are properly handled"""
        violations = []
        # Check for requests that are still APPROVED but user has revoked consent
        approved_requests = AccessRequest.objects.filter(
            organization=organization,
            status='APPROVED'
        )
        
        for request in approved_requests:
            user_consent = UserConsent.objects.filter(
                user=request.user,
                consent=request.consent
            ).first()
            
            # CRITICAL: If no consent record exists OR consent is revoked (access=False)
            if not user_consent or not user_consent.access:
                violations.append({
                    'rule': 'REVOCATION_HANDLING',
                    'details': {
                        'access_request_id': request.id,
                        'user_id': request.user.id,
                        'consent_type': request.consent.name,
                        'issue': 'CRITICAL: Access still approved but user consent is missing or revoked',
                    },
                    'recommendation': f'IMMEDIATELY revoke access request #{request.id} - user consent is missing or revoked',
                })
        
        return violations
    
    @staticmethod
    def check_excessive_requests(organization: Org) -> list:
        """Check for unusual patterns in data requests"""
        violations = []
        # Check requests in last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_requests = AccessRequest.objects.filter(
            organization=organization,
            requested_at__gte=thirty_days_ago
        )
        
        if recent_requests.count() > 100:  # Threshold: 100 requests in 30 days
            violations.append({
                'rule': 'EXCESSIVE_REQUESTS',
                'details': {
                    'requests_count': recent_requests.count(),
                    'period_days': 30,
                    'issue': 'Unusually high number of data access requests',
                },
                'recommendation': 'Review if all requests are necessary and legitimate',
            })
        
        return violations
    
    @classmethod
    def run_all_checks(cls, organization: Org) -> dict:
        """Run all compliance checks for an organization"""
        all_violations = []
        
        # Run all rule checks
        all_violations.extend(cls.check_consent_validity(organization))
        all_violations.extend(cls.check_purpose_limitation(organization))
        all_violations.extend(cls.check_data_minimization(organization))
        all_violations.extend(cls.check_retention_policy(organization))
        all_violations.extend(cls.check_access_control(organization))
        all_violations.extend(cls.check_audit_trail(organization))
        all_violations.extend(cls.check_revocation_handling(organization))
        all_violations.extend(cls.check_excessive_requests(organization))
        
        # Calculate risk score (0-100, higher = more risk)
        risk_score = cls.calculate_risk_score(all_violations)
        
        return {
            'violations': all_violations,
            'risk_score': risk_score,
            'total_violations': len(all_violations),
            'critical_count': len([v for v in all_violations if cls.RULES.get(v['rule'], {}).get('severity') == 'CRITICAL']),
            'high_count': len([v for v in all_violations if cls.RULES.get(v['rule'], {}).get('severity') == 'HIGH']),
            'medium_count': len([v for v in all_violations if cls.RULES.get(v['rule'], {}).get('severity') == 'MEDIUM']),
        }
    
    @staticmethod
    def calculate_risk_score(violations: list) -> int:
        """Calculate compliance risk score (0-100)"""
        if not violations:
            return 0
        
        score = 0
        for violation in violations:
            rule_info = NDPRRulesEngine.RULES.get(violation['rule'], {})
            severity = rule_info.get('severity', 'MEDIUM')
            
            if severity == 'CRITICAL':
                score += 20
            elif severity == 'HIGH':
                score += 15
            elif severity == 'MEDIUM':
                score += 10
            else:  # LOW
                score += 5
        
        # Cap at 100
        return min(score, 100)
    
    @classmethod
    def create_audit_records(cls, organization: Org, scan_result: dict) -> list:
        """Create ComplianceAudit records from scan results"""
        audit_records = []
        
        for violation in scan_result['violations']:
            rule_info = cls.RULES.get(violation['rule'], {})
            
            audit = ComplianceAudit.objects.create(
                organization=organization,
                rule_name=rule_info.get('name', violation['rule']),
                rule_description=rule_info.get('description', ''),
                severity=rule_info.get('severity', 'MEDIUM'),
                details=violation.get('details', {}),
                recommendation=violation.get('recommendation', ''),
                status='PENDING',
            )
            audit_records.append(audit)
            
            # Create violation report for critical/high severity
            if rule_info.get('severity') in ['CRITICAL', 'HIGH']:
                violation_type_map = {
                    'CONSENT_VALIDITY': 'CONSENT_VIOLATION',
                    'REVOCATION_HANDLING': 'CONSENT_VIOLATION',
                    'ACCESS_CONTROL': 'ACCESS_CONTROL',
                    'RETENTION_POLICY': 'DATA_RETENTION',
                    'PURPOSE_LIMITATION': 'PURPOSE_LIMITATION',
                }
                
                # Count affected users from details
                details = violation.get('details', {})
                affected_count = 1 if 'user_id' in details or 'access_request_id' in details else 0
                
                ViolationReport.objects.create(
                    organization=organization,
                    violation_type=violation_type_map.get(violation['rule'], 'PRIVACY_BREACH'),
                    description=violation.get('recommendation', rule_info.get('description', '')),
                    affected_users_count=affected_count,
                    related_audit=audit,
                    reported_to_dpo=rule_info.get('severity') == 'CRITICAL',
                )
        
        return audit_records

