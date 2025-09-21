#!/usr/bin/env python
"""
Comprehensive test runner for Django DRF project
Tests all components including models, APIs, Elasticsearch, and integration tests
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests():
    """Run all tests for the project"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Define test modules to run
    test_modules = [
        'users.tests',
        'categories.tests', 
        'products.tests',
    ]
    
    print("🧪 Running Comprehensive Test Suite")
    print("=" * 50)
    
    failures = test_runner.run_tests(test_modules)
    
    if failures:
        print(f"\n❌ {failures} test(s) failed")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)

if __name__ == '__main__':
    run_tests()
