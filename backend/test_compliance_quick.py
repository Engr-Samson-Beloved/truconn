"""
Quick validation script for compliance engine
This checks code structure without requiring Django to be running
Run: python test_compliance_quick.py
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_file_content(filepath, search_string, description):
    """Check if file contains specific content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description} - '{search_string}' not found")
                return False
    except Exception as e:
        print(f"⚠️  Could not check {filepath}: {e}")
        return False

def main():
    """Run all validation checks"""
    print("=" * 70)
    print("NDPR Compliance Engine - Quick Validation")
    print("=" * 70)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results = []
    
    # Check 1: Models file exists
    print("\n1️⃣ Checking Models...")
    models_path = os.path.join(base_dir, 'compliance', 'models.py')
    results.append(check_file_exists(models_path, "Compliance models file"))
    results.append(check_file_content(models_path, 'class ComplianceAudit', "ComplianceAudit model"))
    results.append(check_file_content(models_path, 'class ViolationReport', "ViolationReport model"))
    
    # Check 2: Rules engine exists
    print("\n2️⃣ Checking Rules Engine...")
    rules_path = os.path.join(base_dir, 'compliance', 'rules_engine.py')
    results.append(check_file_exists(rules_path, "Rules engine file"))
    results.append(check_file_content(rules_path, 'class NDPRRulesEngine', "NDPRRulesEngine class"))
    results.append(check_file_content(rules_path, 'CONSENT_VALIDITY', "CONSENT_VALIDITY rule"))
    results.append(check_file_content(rules_path, 'REVOCATION_HANDLING', "REVOCATION_HANDLING rule"))
    results.append(check_file_content(rules_path, 'run_all_checks', "run_all_checks method"))
    
    # Check 3: Views exist
    print("\n3️⃣ Checking Views...")
    views_path = os.path.join(base_dir, 'compliance', 'views.py')
    results.append(check_file_exists(views_path, "Views file"))
    results.append(check_file_content(views_path, 'class ComplianceScanView', "ComplianceScanView"))
    results.append(check_file_content(views_path, 'class ComplianceReportsView', "ComplianceReportsView"))
    
    # Check 4: Serializers exist
    print("\n4️⃣ Checking Serializers...")
    serializers_path = os.path.join(base_dir, 'compliance', 'serializers.py')
    results.append(check_file_exists(serializers_path, "Serializers file"))
    results.append(check_file_content(serializers_path, 'ComplianceAuditSerializer', "ComplianceAuditSerializer"))
    results.append(check_file_content(serializers_path, 'ViolationReportSerializer', "ViolationReportSerializer"))
    
    # Check 5: URLs configured
    print("\n5️⃣ Checking URLs...")
    urls_path = os.path.join(base_dir, 'compliance', 'urls.py')
    results.append(check_file_exists(urls_path, "URLs file"))
    results.append(check_file_content(urls_path, 'compliance-scan', "Compliance scan URL"))
    
    # Check main URLs
    main_urls_path = os.path.join(base_dir, 'truconn', 'urls.py')
    results.append(check_file_content(main_urls_path, "api/compliance/", "Compliance URLs in main urls.py"))
    
    # Check 6: Migrations exist
    print("\n6️⃣ Checking Migrations...")
    migrations_dir = os.path.join(base_dir, 'compliance', 'migrations')
    results.append(check_file_exists(migrations_dir, "Migrations directory"))
    
    migration_file = os.path.join(migrations_dir, '0001_initial.py')
    results.append(check_file_exists(migration_file, "Initial migration file"))
    results.append(check_file_content(migration_file, 'ComplianceAudit', "ComplianceAudit in migration"))
    results.append(check_file_content(migration_file, 'ViolationReport', "ViolationReport in migration"))
    
    # Check 7: Settings
    print("\n7️⃣ Checking Settings...")
    settings_path = os.path.join(base_dir, 'truconn', 'settings.py')
    results.append(check_file_content(settings_path, "'compliance'", "Compliance app in INSTALLED_APPS"))
    
    # Check 8: Frontend API client
    print("\n8️⃣ Checking Frontend Integration...")
    frontend_base = os.path.join(base_dir, '..')
    api_client_path = os.path.join(frontend_base, 'lib', 'compliance', 'api.ts')
    if os.path.exists(api_client_path):
        results.append(check_file_exists(api_client_path, "Frontend API client"))
        results.append(check_file_content(api_client_path, 'runScan', "runScan method"))
        results.append(check_file_content(api_client_path, 'getScanResults', "getScanResults method"))
        results.append(check_file_content(api_client_path, 'updateAuditStatus', "updateAuditStatus method"))
    else:
        print(f"⚠️  Frontend API client not found (expected at: {api_client_path})")
    
    # Check 9: Frontend page
    frontend_page = os.path.join(frontend_base, 'app', 'admin', 'organization', 'compliance', 'page.tsx')
    if os.path.exists(frontend_page):
        results.append(check_file_exists(frontend_page, "Frontend compliance page"))
        results.append(check_file_content(frontend_page, 'ComplianceAPI', "ComplianceAPI usage"))
        results.append(check_file_content(frontend_page, 'handleRunScan', "Run scan handler"))
    else:
        print(f"⚠️  Frontend page not found (expected at: {frontend_page})")
    
    # Summary
    print("\n" + "=" * 70)
    passed = sum([1 for r in results if r])
    total = len(results)
    print(f"📊 Results: {passed}/{total} checks passed ({int(passed/total*100)}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n✅ ALL CODE CHECKS PASSED!")
        print("\nNext steps to test:")
        print("1. Activate virtual environment:")
        print("   cd backend")
        print("   .\\venv\\Scripts\\Activate.ps1  # Windows PowerShell")
        print("   source venv/bin/activate      # Linux/Mac")
        print("\n2. Run migrations:")
        print("   python manage.py migrate compliance")
        print("\n3. Start backend server:")
        print("   python manage.py runserver")
        print("\n4. In another terminal, start frontend:")
        print("   npm run dev")
        print("\n5. Test the compliance scanner:")
        print("   Navigate to: http://localhost:3000/admin/organization/compliance")
        print("   Login as organization user")
        print("   Click 'Run Full Compliance Scan'")
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please review the errors above.")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()

