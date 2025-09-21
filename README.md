# E-Shop - Django E-commerce Platform

A comprehensive e-commerce platform built with Django REST Framework, featuring user authentication, product management, search functionality, and a modern admin interface.

## 🚀 Features

### Core Features
- **User Authentication** - JWT-based authentication system
- **Product Management** - CRUD operations for products and categories
- **Advanced Search** - Elasticsearch-powered search with filtering
- **Admin Panel** - Enhanced admin interface with Django Jazzmin
- **API Documentation** - Swagger/ReDoc documentation
- **Frontend** - Responsive web interface with Bootstrap 5
- **Shopping Cart** - Full cart functionality
- **Image Management** - Product and category image uploads

### Technical Features
- **Django 5.2** - Latest Django framework
- **PostgreSQL** - Production-ready database
- **Elasticsearch** - Advanced search and indexing
- **Docker** - Containerized deployment
- **JWT Authentication** - Secure token-based auth
- **RESTful API** - Complete API with proper status codes
- **Comprehensive Testing** - Unit, integration, and API tests

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Git

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd django
```

### 2. Environment Setup
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,web
DB_NAME=eshop_db
DB_USER=eshop_user
DB_PASSWORD=eshop_password
DB_HOST=db
DB_PORT=5432
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
JWT_SECRET_KEY=your-jwt-secret-key
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200
```

### 3. Build and Run with Docker
```bash
# Build the containers
docker-compose build

# Start the services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Generate fake data
docker-compose exec web python manage.py create_fake_data

# Add images to products
docker-compose exec web python manage.py add_images
```

## 🎯 Usage

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://127.0.0.1:8001/ | Main website |
| **Admin Panel** | http://127.0.0.1:8001/admin/ | Django admin |
| **API Docs (Swagger)** | http://127.0.0.1:8001/swagger/ | Interactive API docs |
| **API Docs (ReDoc)** | http://127.0.0.1:8001/redoc/ | Alternative API docs |
| **Kibana** | http://127.0.0.1:5601/ | Elasticsearch dashboard |

### Default Credentials
- **Admin Username:** admin
- **Admin Password:** admin123
- **Test User Email:** admin@example.com
- **Test User Password:** admin123

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create category (Admin only)
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category (Admin only)
- `DELETE /api/categories/{id}/` - Delete category (Admin only)

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create product (Admin only)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product (Admin only)
- `DELETE /api/products/{id}/` - Delete product (Admin only)
- `GET /api/products/search/` - Search products

### Cart
- `POST /api/cart/add/` - Add item to cart
- `POST /api/cart/update/` - Update cart item
- `POST /api/cart/remove/` - Remove item from cart
- `GET /api/cart/` - Get cart data

## 🧪 Testing

### Run All Tests
```bash
# Run tests inside Docker container
docker-compose exec web python run_tests.py

# Or run specific test files
docker-compose exec web python manage.py test users
docker-compose exec web python manage.py test categories
docker-compose exec web python manage.py test products
```

### API Testing
```bash
# Run API tests
docker-compose exec web python test_api.py
```

### Elasticsearch Testing
```bash
# Test Elasticsearch functionality
docker-compose exec web python manage.py test_elasticsearch
```

## 📊 Management Commands

### Create Fake Data
```bash
# Create fake users, categories, and products
docker-compose exec web python manage.py create_fake_data

# Clear existing data and create new
docker-compose exec web python manage.py create_fake_data --clear
```

### Add Images
```bash
# Add placeholder images to products and categories
docker-compose exec web python manage.py add_images
```

### Elasticsearch Management
```bash
# Test Elasticsearch connection
docker-compose exec web python manage.py test_elasticsearch

# Create Elasticsearch index
docker-compose exec web python manage.py test_elasticsearch --create-index

# Populate Elasticsearch index
docker-compose exec web python manage.py test_elasticsearch --populate-index

# Test search functionality
docker-compose exec web python manage.py test_elasticsearch --test-search
```

## 🏗️ Project Structure

```
django/
├── apps/                    # Django apps
│   ├── users/              # User management
│   ├── categories/         # Category management
│   ├── products/           # Product management
│   ├── cart/               # Shopping cart
│   └── frontend/           # Frontend views
├── core/                   # Django settings
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker configuration
├── Dockerfile             # Docker image definition
└── README.md              # This file
```

## 🔐 Security Features

- **JWT Authentication** - Secure token-based authentication
- **CORS Configuration** - Proper cross-origin resource sharing
- **Input Validation** - Comprehensive data validation
- **SQL Injection Protection** - Django ORM protection
- **XSS Protection** - Template auto-escaping
- **CSRF Protection** - Cross-site request forgery protection

## 🚀 Deployment

### Production Deployment
1. Update `.env` file with production values
2. Set `DEBUG=False`
3. Configure proper `ALLOWED_HOSTS`
4. Use production database credentials
5. Set up proper media file storage
6. Configure Elasticsearch for production

### Docker Production
```bash
# Build production image
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

## 📈 Performance Features

- **Database Optimization** - Proper indexing and queries
- **Elasticsearch** - Fast search and filtering
- **Pagination** - Efficient data loading
- **Image Optimization** - Proper image handling
- **Caching** - Redis caching (configurable)

## 🛠️ Development

### Local Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Code Quality
- **PEP 8** - Python code style
- **Type Hints** - Type annotations
- **Docstrings** - Comprehensive documentation
- **Testing** - High test coverage

## 📝 API Documentation

### Swagger UI
Visit http://127.0.0.1:8001/swagger/ for interactive API documentation.

### ReDoc
Visit http://127.0.0.1:8001/redoc/ for alternative API documentation.

### JWT Token Usage
1. Get JWT token from `/api/auth/login/`
2. Use token in Authorization header: `Bearer <token>`
3. Token expires in 60 minutes (configurable)

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "8002:8000"  # Change 8001 to 8002
```

#### Database Connection Issues
```bash
# Restart database service
docker-compose restart db

# Check database logs
docker-compose logs db
```

#### Elasticsearch Issues
```bash
# Restart Elasticsearch
docker-compose restart elasticsearch

# Check Elasticsearch status
docker-compose exec web python manage.py test_elasticsearch
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django REST Framework
- Django Jazzmin
- Elasticsearch
- Bootstrap 5
- Font Awesome

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API documentation

---

**Happy Coding! 🚀**