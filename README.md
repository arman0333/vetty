# Cryptocurrency Market Updates API

A REST API application for fetching cryptocurrency market updates from CoinGecko API.

## Features

- List all coins with coin IDs
- List coin categories
- List specific coins by ID and/or category
- Market data in INR (Indian Rupee) and CAD (Canadian Dollar)
- Pagination support (page_num and per_page parameters)
- JWT-based authentication
- Comprehensive API documentation (Swagger/OpenAPI)
- Unit tests with >80% coverage

## Project Structure

```
vetty/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── auth.py              # JWT authentication
│   ├── models.py            # Pydantic models
│   ├── utils.py             # Shared utility functions
│   ├── services/
│   │   ├── __init__.py
│   │   └── coingecko.py     # CoinGecko API service
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── coins.py         # Coin endpoints
│       └── categories.py    # Category endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration
│   ├── test_auth.py
│   ├── test_coins.py
│   ├── test_categories.py
│   ├── test_main.py
│   ├── test_main_detailed.py
│   ├── test_services.py
│   └── test_utils.py
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── env.example
├── run.py
├── run.bat
├── run.ps1
├── run.sh
├── test-docker.ps1
├── README.md
├── HOW_TO_RUN.md
├── ENDPOINTS_GUIDE.md
├── API_ENDPOINTS.md
├── DOCKER.md
├── TEST_DOCKER.md
└── HEALTH_VERSION_ENDPOINTS.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vetty
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `env.example`:
```bash
# On Linux/Mac
cp env.example .env

# On Windows PowerShell
Copy-Item env.example .env
```

5. Update `.env` with your configuration (especially `SECRET_KEY`)

## Running the Application

### Option 1: Using Docker (Recommended for Production)
```bash
# Using Docker Compose
docker-compose up --build

# Or using Docker directly
docker build -t cryptocurrency-api .
docker run -p 8000:8000 cryptocurrency-api
```

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

### Option 2: Using the run script (Easiest)
```bash
# Windows (use 'py' command)
py run.py
# or double-click run.bat

# Linux/Mac
python3 run.py
# or
chmod +x run.sh && ./run.sh
```

### Option 3: Using uvicorn directly
```bash
uvicorn app.main:app --reload
```

### Option 4: Using uvicorn with custom port
```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at:
- **API**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`
- **Detailed Health**: `http://localhost:8000/health/detailed`
- **Version Info**: `http://localhost:8000/version`

## Authentication

The API uses JWT-based authentication. To get an access token:

1. Register a user (if registration endpoint exists) or use a default test user
2. Login to get a JWT token
3. Include the token in the Authorization header: `Authorization: Bearer <token>`

Example:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

## API Endpoints

### Authentication
- `POST /auth/login` - Login and get JWT token

### Coins
- `GET /coins` - List all coins with IDs (paginated)
- `GET /coins/market-data` - Get coins filtered by ID and/or category with INR/CAD market data (paginated)
- `GET /coins/{coin_id}` - Alternative endpoint to get coins by ID (paginated)

### Categories
- `GET /categories` - List all coin categories (paginated)
- `GET /categories/{category_id}/coins` - Get coins in a specific category with market data (paginated)

**For detailed documentation:**
- [API Endpoints Guide](ENDPOINTS_GUIDE.md) - Complete endpoint documentation
- [How to Run](HOW_TO_RUN.md) - Setup and running instructions
- [Docker Guide](DOCKER.md) - Docker setup and deployment
- [Health & Version Endpoints](HEALTH_VERSION_ENDPOINTS.md) - Health check documentation

## Testing

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

View coverage report:
```bash
# Open htmlcov/index.html in your browser
```

## Code Quality

This project follows:
- PEP-8 style guidelines
- Zen of Python principles
- KISS (Keep It Simple, Stupid)
- DRY (Don't Repeat Yourself)
- SOLID principles

## Security

- Sensitive data is stored in environment variables (`.env` file)
- JWT tokens are used for authentication
- Passwords are hashed using bcrypt
- API keys and secrets are never committed to the repository

## License

MIT License

