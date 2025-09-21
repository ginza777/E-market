# 🚀 Django DRF Project - Enhanced Setup & Testing Guide

## 🎯 Project Overview

This is a comprehensive Django REST Framework project with PostgreSQL, JWT authentication, Elasticsearch search, and Docker containerization. The project includes enhanced admin panel, comprehensive testing, fake data generation, and advanced search capabilities.

## ✨ Enhanced Features

### 🔧 **Enhanced Admin Panel**
- **Custom User Admin**: Advanced user management with full name display, verification status, and custom actions
- **Smart Category Admin**: Product count display, image previews, and bulk operations
- **Advanced Product Admin**: Stock status indicators, image previews, and Elasticsearch integration
- **Custom Actions**: Bulk operations for activating/deactivating products and updating search indexes

### 📚 **Comprehensive API Documentation**
- **Enhanced Swagger UI**: Detailed API documentation with examples and schemas
- **ReDoc Integration**: Alternative documentation interface
- **OpenAPI 3.0**: Complete API specification with authentication details
- **Interactive Testing**: Test endpoints directly from documentation

### 🧪 **Comprehensive Testing Suite**
- **Unit Tests**: Model validation, serializer testing, and business logic
- **API Tests**: Complete endpoint testing with authentication
- **Integration Tests**: End-to-end workflow testing
- **Elasticsearch Tests**: Search functionality and indexing performance
- **Mock Testing**: Isolated testing with mocked external dependencies

### 🎭 **Fake Data Generation**
- **Realistic Data**: Faker-based data generation for development and testing
- **Configurable**: Customizable number of users, categories, and products
- **Category-Specific**: Smart product generation based on category types
- **Bulk Operations**: Efficient data creation for large datasets

### 🔍 **Advanced Search & Indexing**
- **Elasticsearch Integration**: Full-text search across products
- **Performance Testing**: Indexing speed and search performance tests
- **Real-time Updates**: Automatic index updates on data changes
- **Advanced Filtering**: Price ranges, categories, and custom filters

## 🛠️ **Setup Instructions**

### **Prerequisites**
```bash
# Required software
- Docker & Docker Compose
- Python 3.12+
- PostgreSQL (for local development)
- Elasticsearch (for local development)
```

### **Quick Start with Docker**

1. **Clone and Setup**
```bash
git clone <repository-url>
cd django
```

2. **Start All Services**
```bash
docker-compose up -d
```

3. **Run Migrations**
```bash
docker-compose exec web python manage.py migrate
```

4. **Create Superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Generate Fake Data**
```bash
docker-compose exec web python manage.py create_fake_data --users 20 --categories 10 --products 100
```

6. **Setup Elasticsearch**
```bash
docker-compose exec web python manage.py test_elasticsearch --all
```

### **Local Development Setup**

1. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Database**
```bash
createdb django_db
python manage.py migrate
```

4. **Create Superuser**
```bash
python manage.py createsuperuser
```

5. **Generate Test Data**
```bash
python manage.py create_fake_data --users 10 --categories 5 --products 50
```

6. **Start Development Server**
```bash
python manage.py runserver
```

## 🧪 **Testing Guide**

### **Run All Tests**
```bash
# Using Docker
docker-compose exec web python run_tests.py

# Local development
python run_tests.py
```

### **Run Specific Test Modules**
```bash
# User tests
python manage.py test users.tests

# Category tests
python manage.py test categories.tests

# Product tests
python manage.py test products.tests
```

### **API Testing**
```bash
# Comprehensive API testing
python test_api.py

# Test with custom URL
python test_api.py --url http://localhost:8000
```

### **Elasticsearch Testing**
```bash
# Test Elasticsearch functionality
python manage.py test_elasticsearch --all

# Create and populate index
python manage.py test_elasticsearch --create-index --populate-index

# Test search functionality
python manage.py test_elasticsearch --test-search
```

## 📊 **Admin Panel Features**

### **User Management**
- **Enhanced Display**: Full name, verification status, last login
- **Custom Actions**: Bulk user operations
- **Advanced Filtering**: By verification status, staff status, creation date
- **Search**: By email, username, first name, last name

### **Category Management**
- **Product Count**: Shows number of products in each category
- **Image Preview**: Thumbnail preview of category images
- **Quick Actions**: Direct links to category products
- **Elasticsearch Integration**: Auto-updates search index

### **Product Management**
- **Stock Status**: Visual indicators for stock levels
- **Image Preview**: Thumbnail preview of product images
- **Bulk Operations**: Activate/deactivate multiple products
- **Search Integration**: Manual Elasticsearch index updates

## 🔍 **Search & Elasticsearch**

### **Search Features**
- **Full-Text Search**: Search across product titles and descriptions
- **Category Search**: Filter by product categories
- **Price Filtering**: Range-based price filtering
- **Advanced Sorting**: By price, title, creation date

### **Indexing Performance**
- **Bulk Indexing**: Efficient bulk operations
- **Real-time Updates**: Automatic index updates
- **Performance Monitoring**: Indexing speed tests
- **Statistics**: Document count and index size

### **Search API Endpoints**
```bash
# Basic search
GET /api/products/search/?search=iPhone

# Category filter
GET /api/products/search/?category=1

# Price range
GET /api/products/search/?price__gte=100&price__lte=500

# Combined filters
GET /api/products/search/?search=phone&category=1&price__gte=500
```

## 📚 **API Documentation**

### **Access Points**
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI JSON**: http://localhost:8000/swagger.json
- **OpenAPI YAML**: http://localhost:8000/swagger.yaml

### **Authentication**
All protected endpoints require JWT authentication:
```bash
Authorization: Bearer <your_access_token>
```

### **API Endpoints**

#### **Authentication**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh
- `GET /api/auth/profile/` - User profile

#### **Categories**
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category
- `GET /api/categories/{id}/` - Get category
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

#### **Products**
- `GET /api/products/` - List products
- `POST /api/products/` - Create product
- `GET /api/products/{id}/` - Get product
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `GET /api/products/by_category/` - Products by category

#### **Search**
- `GET /api/products/search/` - Elasticsearch search

## 🐳 **Docker Services**

### **Services Overview**
- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **elasticsearch**: Elasticsearch search engine (port 9200)
- **kibana**: Elasticsearch visualization (port 5601)

### **Docker Commands**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Execute commands
docker-compose exec web python manage.py <command>

# Stop services
docker-compose down

# Rebuild services
docker-compose up --build
```

## 🔧 **Management Commands**

### **Fake Data Generation**
```bash
# Create default data
python manage.py create_fake_data

# Custom amounts
python manage.py create_fake_data --users 50 --categories 15 --products 200

# Clear existing data first
python manage.py create_fake_data --clear --users 10 --categories 5 --products 50
```

### **Elasticsearch Management**
```bash
# Create index
python manage.py test_elasticsearch --create-index

# Populate index
python manage.py test_elasticsearch --populate-index

# Test search
python manage.py test_elasticsearch --test-search

# Test indexing performance
python manage.py test_elasticsearch --test-indexing

# Run all tests
python manage.py test_elasticsearch --all
```

## 📈 **Performance & Monitoring**

### **Database Optimization**
- **Select Related**: Optimized queries with select_related
- **Indexing**: Proper database indexes
- **Pagination**: Efficient pagination for large datasets

### **Elasticsearch Performance**
- **Bulk Operations**: Efficient bulk indexing
- **Index Optimization**: Proper index settings
- **Query Optimization**: Optimized search queries

### **API Performance**
- **Caching**: Response caching where appropriate
- **Rate Limiting**: Built-in rate limiting
- **Compression**: Response compression

## 🚀 **Production Deployment**

### **Environment Variables**
```env
# Production settings
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=secure_password
DB_HOST=your-db-host

# Elasticsearch
ELASTICSEARCH_HOST=your-elasticsearch-host
ELASTICSEARCH_PORT=9200
```

### **Security Considerations**
- **HTTPS**: Use HTTPS in production
- **Secret Keys**: Use strong, unique secret keys
- **Database**: Use production-grade database
- **Monitoring**: Implement proper monitoring and logging

## 🆘 **Troubleshooting**

### **Common Issues**

1. **Elasticsearch Connection Error**
```bash
# Check Elasticsearch status
docker-compose logs elasticsearch

# Restart Elasticsearch
docker-compose restart elasticsearch
```

2. **Database Connection Error**
```bash
# Check database status
docker-compose logs db

# Run migrations
docker-compose exec web python manage.py migrate
```

3. **Permission Errors**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### **Debug Mode**
```bash
# Enable debug logging
export DJANGO_LOG_LEVEL=DEBUG
python manage.py runserver
```

## 📞 **Support**

For support and questions:
- **Email**: support@example.com
- **Documentation**: http://localhost:8000/swagger/
- **Issues**: Create GitHub issues for bugs and feature requests

## 🎉 **Success!**

Your Django DRF project is now fully set up with:
- ✅ Enhanced admin panel
- ✅ Comprehensive API documentation
- ✅ Complete testing suite
- ✅ Fake data generation
- ✅ Advanced search capabilities
- ✅ Docker containerization
- ✅ Performance optimization

Happy coding! 🚀
