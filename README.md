# Parcels Management API

Django-based API for managing land parcels and offers with background job monitoring and unit testing.

## Prerequisites
- Docker
- Docker Compose

## Quick Start with Docker

### 1. Clone Repository
```bash
git clone <repository-url>
cd parcels-management-api
```

### 2. Environment Configuration
Create a `.env` file in the `/docker` directory:

```env
# Database configuration
POSTGRES_USER=parcel_user
POSTGRES_PASSWORD=securepassword123
POSTGRES_DB=parcel_db
DB_HOST=db
DB_PORT=5432

# RabbitMQ configuration
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# Celery configuration
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672
```

### 3. Build and Run Project
```bash
cd docker
docker-compose up --build
```

### 4. Running Tests
```bash
# Run tests in the web service container
docker-compose exec web python manage.py test
```

### 5. Authentication
### Access Token Generation
To generate an access token for a user and authenticate request against, use the `jwt_token_generator` module in the
`api/authentication` package.
```bash
#Run Python interactive shell
docker-compose exec web python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from api.authentication import jwt_token_generator

# retrieve already created user
user = get_user_model().objects.get(username="testuser")
# Generate tokens
tokens = jwt_token_generator.make_tokens(user)
print("Access Token:", tokens.access)
```

## API Testing

### Postman Collection
Import the `parcels_api_collection.json` located in the project root for comprehensive API endpoint documentation.

### Accessing API Endpoints
- Base URL: `http://localhost:8000/api/v1/`


## Project Services
- Web Application: `http://localhost:8000`
- PostgreSQL Database: `localhost:5432`
- RabbitMQ: `localhost:5672`

## Troubleshooting
- Check container logs: `docker-compose logs <service_name>`
- Verify environment variables in `.env` file within the `/docker` directory
- Ensure Docker and Docker Compose are up to date
```