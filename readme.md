# Crypto Management API

## Overview
API service for managing cryptocurrency prices across multiple organizations.

## Setup

### Prerequisites
- Python 3.10+
- Redis
- PostgreSQL
- Pipenv

### Installation
```bash
# Install pipenv if not installed
pip install pipenv

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Running Services
```bash
# Start Redis
redis-server

# Start Celery Worker
pipenv run celery -A crypto_management worker -l info

# Start Celery Beat (for scheduled tasks)
pipenv run celery -A crypto_management beat -l info

# Start Django Development Server
pipenv run python manage.py runserver
```

## API Endpoints

### Authentication

#### Register User
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepass123",
    "email": "user@example.com"
}

Response: 201 Created
{
    "id": "uuid",
    "username": "testuser",
    "email": "user@example.com"
}
```
#### Register User with Organizations
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepass123",
    "email": "user@example.com",
    "organization_ids": ["org_uuid1", "org_uuid2"]
}

Response: 201 Created
{
    "id": "uuid",
    "username": "testuser",
    "email": "user@example.com",
    "organizations": [
        {
            "id": "org_uuid1",
            "name": "First Organization"
        },
        {
            "id": "org_uuid2",
            "name": "Second Organization"
        }
    ]
}
```

#### Login
```http
POST /api/users/token/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepass123"
}

Response: 200 OK
{
    "access": "access_token",
    "refresh": "refresh_token"
}
```

### Organizations

#### Create Organization
```http
POST /api/orgs/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Test Organization"
}

Response: 201 Created
{
    "id": "uuid",
    "name": "Test Organization",
    "owner": {
        "id": "uuid",
        "username": "testuser"
    }
}
```

#### List Organizations
```http
GET /api/orgs/
Authorization: Bearer <token>

Response: 200 OK
[
    {
        "id": "uuid",
        "name": "Test Organization",
        "owner": {
            "id": "uuid",
            "username": "testuser"
        }
    }
]
```

#### Update Organization
```http
PATCH /api/orgs/{org_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Updated Name"
}

Response: 200 OK
{
    "id": "uuid",
    "name": "Updated Name",
    "owner": {
        "id": "uuid",
        "username": "testuser"
    }
}
```

### Crypto Prices

#### Create Price Entry
```http
POST /api/prices/
Authorization: Bearer <token>
Content-Type: application/json

{
    "symbol": "BTC",
    "price": "45000.00",
    "org_id": "org_uuid"
}

Response: 201 Created
{
    "id": "uuid",
    "symbol": "BTC",
    "price": "45000.00",
    "timestamp": "2025-03-17T12:00:00Z",
    "org_id": "org_uuid"
}
```

#### List Prices (Grouped by Organization)
```http
GET /api/prices/?price_page=1&prices_per_page=10
Authorization: Bearer <token>

Response: 200 OK
{
    "org_uuid": {
        "name": "Test Organization",
        "prices": [
            {
                "symbol": "BTC",
                "price": "45000.00",
                "timestamp": "2025-03-17T12:00:00Z"
            }
        ],
        "prices_pagination": {
            "count": 50,
            "next": true,
            "previous": false,
            "current_page": 1,
            "total_pages": 5
        }
    }
}
```

### Users & Organizations

#### Assign Organizations to User
```http
PATCH /api/users/{user_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "organization_ids": ["org_uuid1", "org_uuid2"]
}

Response: 200 OK
{
    "id": "uuid",
    "username": "testuser",
    "email": "user@example.com",
    "organizations": [
        {
            "id": "org_uuid1",
            "name": "First Organization",
            "owner": {
                "id": "uuid",
                "username": "owner1"
            }
        },
        {
            "id": "org_uuid2",
            "name": "Second Organization",
            "owner": {
                "id": "uuid",
                "username": "owner2"
            }
        }
    ]
}
```

#### Get User's Organizations
```http
GET /api/users/{user_id}/
Authorization: Bearer <token>

Response: 200 OK
{
    "id": "uuid",
    "username": "testuser",
    "email": "user@example.com",
    "organizations": [
        {
            "id": "org_uuid1",
            "name": "First Organization",
            "owner": {
                "id": "uuid",
                "username": "owner1"
            }
        },
        {
            "id": "org_uuid2",
            "name": "Second Organization",
            "owner": {
                "id": "uuid",
                "username": "owner2"
            }
        }
    ]
}
```

## Permissions

### Organizations
- Any authenticated user can view organizations
- Only organization owners can edit/delete their organizations
- Users can belong to multiple organizations

### Crypto Prices
- Authenticated users can view prices for organizations they belong to
- Only organization owners can create/edit/delete prices
- Prices are paginated within each organization group

## Testing

### Run Tests
```bash
# Run all tests
pipenv run python manage.py test

# Run specific app tests
pipenv run python manage.py test organizations
pipenv run python manage.py test users
pipenv run python manage.py test crypto

# Run with coverage
pipenv run coverage run manage.py test
pipenv run coverage report
pipenv run coverage html
```

