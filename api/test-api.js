#!/usr/bin/env node

/**
 * Test script for QueimadAI API
 * Usage: node test-api.js
 */

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const API_BASE_URL = 'http://localhost:3000';

async function testHealthCheck() {
  console.log('🔍 Testing health check...');
  try {
    const response = await axios.get(`${API_BASE_URL}/api/health`);
    console.log('✅ Health check passed');
    console.log('Response:', JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.log('❌ Health check failed:', error.message);
  }
}

async function testImageUpload() {
  console.log('🔍 Testing image upload...');
  
  // Create a test image if it doesn't exist
  const testImagePath = path.join(__dirname, 'test-image.jpg');
  
  if (!fs.existsSync(testImagePath)) {
    console.log('⚠️  Test image not found. Please add a test image at:', testImagePath);
    return;
  }

  try {
    const form = new FormData();
    form.append('image', fs.createReadStream(testImagePath));

    const response = await axios.post(`${API_BASE_URL}/api/detect/image`, form, {
      headers: {
        ...form.getHeaders(),
      },
    });

    console.log('✅ Image upload test passed');
    console.log('Response:', JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.log('❌ Image upload test failed:', error.message);
    if (error.response) {
      console.log('Error response:', error.response.data);
    }
  }
}

async function testDetectionStatus() {
  console.log('🔍 Testing detection status...');
  try {
    const response = await axios.get(`${API_BASE_URL}/api/detect/status`);
    console.log('✅ Detection status test passed');
    console.log('Response:', JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.log('❌ Detection status test failed:', error.message);
  }
}

async function runAllTests() {
  console.log('🚀 Starting QueimadAI API Tests...\n');
  
  await testHealthCheck();
  console.log();
  
  await testDetectionStatus();
  console.log();
  
  await testImageUpload();
  console.log();
  
  console.log('🏁 All tests completed!');
}

// Run tests if this script is executed directly
if (require.main === module) {
  runAllTests().catch(console.error);
}

module.exports = {
  testHealthCheck,
  testImageUpload,
  testDetectionStatus,
  runAllTests
};
