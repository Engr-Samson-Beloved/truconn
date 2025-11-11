/**
 * Simple test script to verify compliance API connection
 * Run with: node test_compliance_connection.js
 * 
 * This script tests the compliance API endpoints without requiring full server setup
 */

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000/api';
const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:3000';

console.log('🧪 Testing NDPR Compliance Engine Connection');
console.log('=' .repeat(60));
console.log(`Backend URL: ${API_BASE_URL}`);
console.log(`Frontend URL: ${FRONTEND_URL}`);
console.log('=' .repeat(60));

// Test 1: Check if backend health endpoint is accessible
async function testBackendHealth() {
  console.log('\n1️⃣ Testing Backend Health Endpoint...');
  try {
    const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health/`);
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Backend is running');
      console.log(`   Response: ${JSON.stringify(data)}`);
      return true;
    } else {
      console.log(`⚠️  Backend returned status: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.log('❌ Backend is not accessible');
    console.log(`   Error: ${error.message}`);
    console.log('   Make sure backend server is running: python manage.py runserver');
    return false;
  }
}

// Test 2: Check compliance endpoints exist (will fail without auth, but confirms endpoint exists)
async function testComplianceEndpoints() {
  console.log('\n2️⃣ Testing Compliance API Endpoints...');
  const endpoints = [
    { method: 'GET', path: '/compliance/scan/' },
    { method: 'POST', path: '/compliance/scan/' },
    { method: 'GET', path: '/compliance/reports/' },
  ];

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint.path}`, {
        method: endpoint.method,
        headers: { 'Content-Type': 'application/json' },
      });
      
      // 401 is expected without auth, 404 means endpoint doesn't exist
      if (response.status === 401) {
        console.log(`✅ ${endpoint.method} ${endpoint.path} - Endpoint exists (auth required)`);
      } else if (response.status === 404) {
        console.log(`❌ ${endpoint.method} ${endpoint.path} - Endpoint not found`);
      } else {
        console.log(`⚠️  ${endpoint.method} ${endpoint.path} - Status: ${response.status}`);
      }
    } catch (error) {
      console.log(`❌ ${endpoint.method} ${endpoint.path} - Error: ${error.message}`);
    }
  }
}

// Test 3: Check frontend compliance page
async function testFrontendPage() {
  console.log('\n3️⃣ Testing Frontend Compliance Page...');
  try {
    const response = await fetch(`${FRONTEND_URL}/admin/organization/compliance`);
    if (response.ok || response.status === 401) {
      console.log('✅ Frontend page is accessible');
      console.log(`   Status: ${response.status}`);
      return true;
    } else {
      console.log(`⚠️  Frontend returned status: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.log('❌ Frontend is not accessible');
    console.log(`   Error: ${error.message}`);
    console.log('   Make sure frontend server is running: npm run dev');
    return false;
  }
}

// Main test function
async function runTests() {
  const backendOk = await testBackendHealth();
  if (backendOk) {
    await testComplianceEndpoints();
  }
  await testFrontendPage();

  console.log('\n' + '='.repeat(60));
  console.log('📋 Test Summary:');
  console.log('='.repeat(60));
  console.log('\nTo fully test the compliance engine:');
  console.log('1. Start backend: cd backend && python manage.py runserver');
  console.log('2. Start frontend: npm run dev');
  console.log('3. Login as organization user');
  console.log('4. Navigate to: http://localhost:3000/admin/organization/compliance');
  console.log('5. Click "Run Full Compliance Scan"');
  console.log('\nSee TEST_COMPLIANCE_ENGINE.md for detailed instructions.');
}

// Run tests
runTests().catch(console.error);

