# Bookstore API

A comprehensive RESTful API for managing a modern bookstore system built with Django REST Framework.

## 🌟 Features

### User Management
- User registration and authentication with JWT
- Role-based access control (User, Staff, Admin)
- Profile management
- Order history tracking
- Newsletter subscription system

### Product Management
- Comprehensive book catalog with multiple formats (Hardcover, Paperback, eBook, Audiobook)
- Author profiles and statistics
- Genre categorization
- Advanced search and filtering
- Rating and review system
- Bestseller tracking
- Similar book recommendations

### Shopping Features
- Shopping cart management
- Order processing and tracking
- Multiple shipping methods
- Secure checkout process
- Wishlist functionality

### Administrative Features
- Sales dashboard
- Order management
- Inventory tracking
- User management
- Content management

## 🔧 Technology Stack

- **Backend Framework**: Django 4.2
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL 15
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: drf-spectacular (OpenAPI 3.0)
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus & Grafana
- **Logging**: ELK Stack
- **Caching**: Redis

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose
- Kubernetes cluster (for production deployment)

## 🚀 Getting Started

### Local Development Setup

1. Clone the repository:
```bash
git clone repo-name
cd bookstore-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

### Docker Development Setup

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

3. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

### Production Deployment

1. Update Kubernetes configurations:
```bash
# Update the configurations in k8s/ directory with your values
```

2. Deploy to Kubernetes:
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/django.yaml
```

## 📚 API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## 🔒 Security Features

- SSL/TLS encryption
- CORS configuration
- JWT authentication
- Rate limiting
- Input validation
- XSS protection
- CSRF protection
- SQL injection protection

## 🔍 Monitoring & Logging

- Prometheus metrics
- Grafana dashboards
- ELK stack integration
- Error tracking with Sentry
- Automated health checks
- Performance monitoring

## 💾 Backup & Recovery

- Automated daily PostgreSQL backups
- Backup retention policy
- Point-in-time recovery capability
- Cloud storage integration (AWS S3)

## 🚦 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/me/` - Get current user profile
- `GET /api/users/{id}/order-history/` - Get user's order history
- `POST /api/users/{id}/toggle-active/` - Toggle user active status

### Books
- `GET /api/books/` - List all books
- `GET /api/books/bestsellers/` - Get bestselling books
- `GET /api/books/on-sale/` - Get books on sale
- `GET /api/books/{id}/similar-books/` - Get similar books
- `GET /api/books/top-rated/` - Get top rated books

### Authors
- `GET /api/authors/{id}/books/` - Get author's books
- `GET /api/authors/{id}/statistics/` - Get author statistics

### Genres
- `GET /api/genres/{id}/books/` - Get books in genre
- `GET /api/genres/{id}/popular-authors/` - Get popular authors in genre

### Shopping Cart
- `POST /api/shopping-carts/{id}/add-item/` - Add item to cart
- `POST /api/shopping-carts/{id}/remove-item/` - Remove item from cart
- `GET /api/shopping-carts/{id}/total/` - Get cart total

### Orders
- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/dashboard/` - Get order statistics
- `POST /api/orders/{id}/update-status/` - Update order status

### Newsletter
- `POST /api/newsletter/subscribe/` - Subscribe to newsletter
- `POST /api/newsletter/unsubscribe/` - Unsubscribe from newsletter