#!/usr/bin/env python
"""
API Testing Script for Django DRF Project
Tests all API endpoints including authentication, CRUD operations, and search
"""

import requests
import json
import time
from typing import Dict, Any


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.category_id = None
        self.product_id = None

    def test_authentication(self) -> bool:
        """Test user registration and login"""
        print("🔐 Testing Authentication...")
        
        # Test user registration
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/auth/register/", json=register_data)
            if response.status_code == 201:
                print("✅ User registration successful")
                self.token = response.json()["tokens"]["access"]
                self.user_id = response.json()["user"]["id"]
            else:
                print(f"❌ User registration failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
        
        # Test user login
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/auth/login/", json=login_data)
            if response.status_code == 200:
                print("✅ User login successful")
                self.token = response.json()["tokens"]["access"]
            else:
                print(f"❌ User login failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
        
        # Test profile access
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = self.session.get(f"{self.base_url}/api/auth/profile/", headers=headers)
            if response.status_code == 200:
                print("✅ Profile access successful")
            else:
                print(f"❌ Profile access failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Profile access error: {e}")
            return False
        
        return True

    def test_categories(self) -> bool:
        """Test category CRUD operations"""
        print("\n📁 Testing Categories...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test category creation
        category_data = {
            "title": "Test Electronics",
            "description": "Test electronic devices",
            "is_active": True
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/categories/", json=category_data, headers=headers)
            if response.status_code == 201:
                print("✅ Category creation successful")
                self.category_id = response.json()["id"]
            else:
                print(f"❌ Category creation failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Category creation error: {e}")
            return False
        
        # Test category listing
        try:
            response = self.session.get(f"{self.base_url}/api/categories/")
            if response.status_code == 200:
                print("✅ Category listing successful")
            else:
                print(f"❌ Category listing failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Category listing error: {e}")
            return False
        
        # Test category retrieval
        try:
            response = self.session.get(f"{self.base_url}/api/categories/{self.category_id}/")
            if response.status_code == 200:
                print("✅ Category retrieval successful")
            else:
                print(f"❌ Category retrieval failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Category retrieval error: {e}")
            return False
        
        # Test category update
        update_data = {
            "title": "Updated Electronics",
            "description": "Updated electronic devices",
            "is_active": True
        }
        
        try:
            response = self.session.put(f"{self.base_url}/api/categories/{self.category_id}/", json=update_data, headers=headers)
            if response.status_code == 200:
                print("✅ Category update successful")
            else:
                print(f"❌ Category update failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Category update error: {e}")
            return False
        
        return True

    def test_products(self) -> bool:
        """Test product CRUD operations"""
        print("\n📦 Testing Products...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test product creation
        product_data = {
            "title": "Test iPhone 15",
            "description": "Test iPhone model",
            "price": "999.99",
            "category": self.category_id,
            "stock_quantity": 50,
            "is_active": True
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/products/", json=product_data, headers=headers)
            if response.status_code == 201:
                print("✅ Product creation successful")
                self.product_id = response.json()["id"]
            else:
                print(f"❌ Product creation failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Product creation error: {e}")
            return False
        
        # Test product listing
        try:
            response = self.session.get(f"{self.base_url}/api/products/")
            if response.status_code == 200:
                print("✅ Product listing successful")
            else:
                print(f"❌ Product listing failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Product listing error: {e}")
            return False
        
        # Test product retrieval
        try:
            response = self.session.get(f"{self.base_url}/api/products/{self.product_id}/")
            if response.status_code == 200:
                print("✅ Product retrieval successful")
            else:
                print(f"❌ Product retrieval failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Product retrieval error: {e}")
            return False
        
        # Test product update
        update_data = {
            "title": "Updated iPhone 15",
            "description": "Updated iPhone model",
            "price": "1099.99",
            "category": self.category_id,
            "stock_quantity": 25,
            "is_active": True
        }
        
        try:
            response = self.session.put(f"{self.base_url}/api/products/{self.product_id}/", json=update_data, headers=headers)
            if response.status_code == 200:
                print("✅ Product update successful")
            else:
                print(f"❌ Product update failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Product update error: {e}")
            return False
        
        return True

    def test_search(self) -> bool:
        """Test Elasticsearch search functionality"""
        print("\n🔍 Testing Search...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test basic search
        try:
            response = self.session.get(f"{self.base_url}/api/products/search/", headers=headers, params={"search": "iPhone"})
            if response.status_code == 200:
                print("✅ Basic search successful")
            else:
                print(f"❌ Basic search failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Basic search error: {e}")
            return False
        
        # Test category search
        try:
            response = self.session.get(f"{self.base_url}/api/products/search/", headers=headers, params={"category": self.category_id})
            if response.status_code == 200:
                print("✅ Category search successful")
            else:
                print(f"❌ Category search failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Category search error: {e}")
            return False
        
        # Test price range search
        try:
            response = self.session.get(f"{self.base_url}/api/products/search/", headers=headers, params={"price__gte": "500"})
            if response.status_code == 200:
                print("✅ Price range search successful")
            else:
                print(f"❌ Price range search failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Price range search error: {e}")
            return False
        
        return True

    def test_documentation(self) -> bool:
        """Test API documentation endpoints"""
        print("\n📚 Testing Documentation...")
        
        # Test Swagger UI
        try:
            response = self.session.get(f"{self.base_url}/swagger/")
            if response.status_code == 200:
                print("✅ Swagger UI accessible")
            else:
                print(f"❌ Swagger UI failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Swagger UI error: {e}")
            return False
        
        # Test ReDoc
        try:
            response = self.session.get(f"{self.base_url}/redoc/")
            if response.status_code == 200:
                print("✅ ReDoc accessible")
            else:
                print(f"❌ ReDoc failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ ReDoc error: {e}")
            return False
        
        return True

    def cleanup(self):
        """Clean up test data"""
        print("\n🧹 Cleaning up test data...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Delete product
        if self.product_id:
            try:
                response = self.session.delete(f"{self.base_url}/api/products/{self.product_id}/", headers=headers)
                if response.status_code == 204:
                    print("✅ Product deleted")
            except Exception as e:
                print(f"❌ Product deletion error: {e}")
        
        # Delete category
        if self.category_id:
            try:
                response = self.session.delete(f"{self.base_url}/api/categories/{self.category_id}/", headers=headers)
                if response.status_code == 204:
                    print("✅ Category deleted")
            except Exception as e:
                print(f"❌ Category deletion error: {e}")

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Tests")
        print("=" * 50)
        
        tests = [
            ("Authentication", self.test_authentication),
            ("Categories", self.test_categories),
            ("Products", self.test_products),
            ("Search", self.test_search),
            ("Documentation", self.test_documentation),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ {test_name} test crashed: {e}")
                failed += 1
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All API tests passed!")
        else:
            print("💥 Some API tests failed!")
        
        # Cleanup
        self.cleanup()
        
        return failed == 0


def main():
    """Main function to run API tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Django DRF API endpoints')
    parser.add_argument('--url', default='http://localhost:8000', help='Base URL for the API')
    parser.add_argument('--no-cleanup', action='store_true', help='Skip cleanup after tests')
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        if not args.no_cleanup:
            tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test runner crashed: {e}")
        if not args.no_cleanup:
            tester.cleanup()
        sys.exit(1)


if __name__ == '__main__':
    import sys
    main()
