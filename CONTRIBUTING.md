# Contributing to Django E-Shop

Thank you for your interest in contributing to Django E-Shop! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Git
- PostgreSQL (for local development)
- Elasticsearch (for search functionality)

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/django-eshop.git
   cd django-eshop
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Docker Setup**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. **Database Setup**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   docker-compose exec web python manage.py create_fake_data
   ```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Write comprehensive docstrings
- Use meaningful variable and function names

### Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run tests before submitting PRs:
  ```bash
  docker-compose exec web python manage.py test
  ```

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(auth): add JWT token refresh endpoint
fix(products): resolve image upload validation issue
docs(api): update Swagger documentation
```

## 📋 Pull Request Process

### Before Submitting

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test Your Changes**
   ```bash
   # Run all tests
   docker-compose exec web python manage.py test
   
   # Run specific app tests
   docker-compose exec web python manage.py test users
   
   # Check code style
   docker-compose exec web flake8 .
   ```

4. **Update Documentation**
   - Update README.md if needed
   - Add/update API documentation
   - Update CHANGELOG.md

### Submitting PR

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Use clear, descriptive title
   - Provide detailed description
   - Link related issues
   - Add screenshots for UI changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes
   ```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - OS and version
   - Python version
   - Docker version
   - Browser (for frontend issues)

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Screenshots if applicable

3. **Error Messages**
   - Full error traceback
   - Log files if relevant

## ✨ Feature Requests

When requesting features:

1. **Describe the Feature**
   - What problem does it solve?
   - How should it work?
   - Any specific requirements?

2. **Provide Context**
   - Use cases
   - Expected benefits
   - Potential implementation ideas

## 🏗️ Project Structure

```
django-eshop/
├── apps/                    # Django applications
│   ├── users/              # User management
│   ├── categories/         # Category management
│   ├── products/           # Product management
│   ├── cart/               # Shopping cart
│   └── frontend/           # Frontend views
├── core/                   # Django settings
├── templates/              # HTML templates
├── static/                 # Static files
├── media/                  # User uploaded files
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker configuration
├── Dockerfile             # Docker image definition
└── README.md              # Project documentation
```

## 🔧 Development Tools

### Recommended VS Code Extensions

- Python
- Django
- Docker
- GitLens
- REST Client
- Thunder Client

### Useful Commands

```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f web

# Access Django shell
docker-compose exec web python manage.py shell

# Create migrations
docker-compose exec web python manage.py makemigrations

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Generate fake data
docker-compose exec web python manage.py create_fake_data

# Test Elasticsearch
docker-compose exec web python manage.py test_elasticsearch
```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8001/swagger/
- **ReDoc**: http://localhost:8001/redoc/
- **API Endpoints**: See README.md for complete list

## 🧪 Testing

### Running Tests

```bash
# All tests
docker-compose exec web python manage.py test

# Specific app
docker-compose exec web python manage.py test users

# With coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

### Test Categories

- **Unit Tests**: Individual components
- **Integration Tests**: Component interactions
- **API Tests**: Endpoint functionality
- **Model Tests**: Database operations

## 🚀 Deployment

### Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] SSL certificates configured
- [ ] Security headers enabled
- [ ] Monitoring setup
- [ ] Backup strategy implemented

## 📞 Getting Help

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: README.md and inline docs
- **Code Review**: Pull request comments

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Django E-Shop! 🎉
