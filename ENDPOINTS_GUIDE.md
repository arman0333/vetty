# 📋 Complete API Endpoints Guide

## 🔐 Authentication Required

**All endpoints require JWT authentication.** Get your token first:

### Step 1: Login to Get Token
```http
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpass"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 2: Use Token in Requests
Include the token in the Authorization header:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

---

## 📍 Endpoint List

### 1. List All Coins (with coin IDs)

**Endpoint:** `GET /coins`

**Description:** Get a paginated list of all coins with their IDs, symbols, and names.

**Query Parameters:**
- `page_num` (int, optional, default: 1): Page number
- `per_page` (int, optional, default: 10): Items per page (max: 250)

**How to Access:**
```http
GET http://localhost:8000/coins?page_num=1&per_page=10
Authorization: Bearer YOUR_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/coins?page_num=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 15000,
  "total_pages": 1500,
  "data": [
    {
      "id": "bitcoin",
      "symbol": "btc",
      "name": "Bitcoin"
    },
    {
      "id": "ethereum",
      "symbol": "eth",
      "name": "Ethereum"
    },
    ...
  ]
}
```

---

### 2. List Coin Categories

**Endpoint:** `GET /categories`

**Description:** Get a paginated list of all coin categories.

**Query Parameters:**
- `page_num` (int, optional, default: 1): Page number
- `per_page` (int, optional, default: 10): Items per page (max: 250)

**How to Access:**
```http
GET http://localhost:8000/categories?page_num=1&per_page=10
Authorization: Bearer YOUR_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/categories?page_num=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 50,
  "total_pages": 5,
  "data": [
    {
      "category_id": "defi",
      "name": "DeFi"
    },
    {
      "category_id": "nft",
      "name": "NFT"
    },
    {
      "category_id": "layer-1",
      "name": "Layer 1"
    },
    ...
  ]
}
```

---

### 3. List Specific Coins by ID and/or Category (Market Data)

**Endpoint:** `GET /coins/market-data`

**Description:** Get coins filtered by coin ID(s) from the listing endpoint and/or category from the categories endpoint. Shows market data in INR (Indian Rupee) and CAD (Canadian Dollar).

**Query Parameters:**
- `coin_id` (string, optional): Coin ID(s) from `/coins` endpoint (comma-separated: `bitcoin,ethereum`)
- `category` (string, optional): Category ID from `/categories` endpoint
- `page_num` (int, optional, default: 1): Page number
- `per_page` (int, optional, default: 10): Items per page (max: 250)

**Note:** At least one of `coin_id` or `category` must be provided.

#### Example 3a: Filter by Coin ID Only

**How to Access:**
```http
GET http://localhost:8000/coins/market-data?coin_id=bitcoin,ethereum&page_num=1&per_page=10
Authorization: Bearer YOUR_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/coins/market-data?coin_id=bitcoin,ethereum&page_num=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 2,
  "total_pages": 1,
  "data": [
    {
      "id": "bitcoin",
      "symbol": "btc",
      "name": "Bitcoin",
      "current_price_inr": 5000000.0,
      "current_price_cad": 85000.0,
      "market_cap_inr": 1000000000000,
      "market_cap_cad": 1700000000000,
      "price_change_percentage_24h": 2.5
    },
    {
      "id": "ethereum",
      "symbol": "eth",
      "name": "Ethereum",
      "current_price_inr": 300000.0,
      "current_price_cad": 5100.0,
      "market_cap_inr": 500000000000,
      "market_cap_cad": 850000000000,
      "price_change_percentage_24h": 1.5
    }
  ]
}
```

#### Example 3b: Filter by Category Only

**How to Access:**
```http
GET http://localhost:8000/coins/market-data?category=defi&page_num=1&per_page=10
Authorization: Bearer YOUR_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/coins/market-data?category=defi&page_num=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 150,
  "total_pages": 15,
  "data": [
    {
      "id": "uniswap",
      "symbol": "uni",
      "name": "Uniswap",
      "current_price_inr": 500.0,
      "current_price_cad": 8.5,
      "market_cap_inr": 50000000000,
      "market_cap_cad": 85000000000,
      "price_change_percentage_24h": 3.2
    },
    {
      "id": "aave",
      "symbol": "aave",
      "name": "Aave",
      "current_price_inr": 8000.0,
      "current_price_cad": 136.0,
      "market_cap_inr": 120000000000,
      "market_cap_cad": 204000000000,
      "price_change_percentage_24h": -1.5
    },
    ...
  ]
}
```

#### Example 3c: Filter by Both Coin ID AND Category

**How to Access:**
```http
GET http://localhost:8000/coins/market-data?coin_id=bitcoin&category=defi&page_num=1&per_page=10
Authorization: Bearer YOUR_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/coins/market-data?coin_id=bitcoin&category=defi&page_num=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:** Returns coins that match BOTH the coin_id AND category filter.

---

### 4. Alternative: Get Coin by ID (Path Parameter)

**Endpoint:** `GET /coins/{coin_id}`

**Description:** Alternative way to get coins by ID using path parameter. Can also filter by category.

**Path Parameters:**
- `coin_id` (string): Coin ID (comma-separated for multiple: `bitcoin,ethereum`)

**Query Parameters:**
- `category` (string, optional): Category ID to filter
- `page_num` (int, optional, default: 1): Page number
- `per_page` (int, optional, default: 10): Items per page

**How to Access:**
```http
GET http://localhost:8000/coins/bitcoin,ethereum?category=defi&page_num=1&per_page=10
Authorization: Bearer YOUR_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/coins/bitcoin,ethereum?category=defi&page_num=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:** Same format as `/coins/market-data` endpoint.

---

### 5. Get Coins by Category (Alternative Endpoint)

**Endpoint:** `GET /categories/{category_id}/coins`

**Description:** Get all coins in a specific category with market data in INR and CAD.

**Path Parameters:**
- `category_id` (string): Category ID from `/categories` endpoint

**Query Parameters:**
- `page_num` (int, optional, default: 1): Page number
- `per_page` (int, optional, default: 10): Items per page

**How to Access:**
```http
GET http://localhost:8000/categories/defi/coins?page_num=1&per_page=10
Authorization: Bearer YOUR_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/categories/defi/coins?page_num=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:** Same format as `/coins/market-data` endpoint.

---

## 🔍 Using Swagger UI (Easiest Method)

1. Start the server: `python run.py`
2. Open browser: http://localhost:8000/docs
3. Click "Authorize" button (top right)
4. Enter: `Bearer YOUR_TOKEN` (replace YOUR_TOKEN with actual token)
5. Click "Authorize"
6. Now you can test all endpoints interactively!

---

## 📊 Response Format

All endpoints return paginated responses with this structure:

```json
{
  "page": 1,              // Current page number
  "per_page": 10,         // Items per page
  "total": 100,           // Total number of items
  "total_pages": 10,      // Total number of pages
  "data": [...]           // Array of items
}
```

---

## 🧪 Quick Test Script (PowerShell)

```powershell
# 1. Login and get token
$body = @{
    username = "testuser"
    password = "testpass"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
  -Method Post -Body $body -ContentType "application/json"
$token = $response.access_token

# 2. Set headers
$headers = @{
    Authorization = "Bearer $token"
}

# 3. Test endpoints
Write-Host "`n1. List all coins:"
Invoke-RestMethod -Uri "http://localhost:8000/coins?page_num=1&per_page=5" -Headers $headers

Write-Host "`n2. List categories:"
Invoke-RestMethod -Uri "http://localhost:8000/categories?page_num=1&per_page=5" -Headers $headers

Write-Host "`n3. Get market data by coin ID:"
Invoke-RestMethod -Uri "http://localhost:8000/coins/market-data?coin_id=bitcoin&page_num=1&per_page=5" -Headers $headers

Write-Host "`n4. Get market data by category:"
Invoke-RestMethod -Uri "http://localhost:8000/coins/market-data?category=defi&page_num=1&per_page=5" -Headers $headers
```

---

## ⚠️ Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```
**Solution:** Make sure you're including a valid JWT token in the Authorization header.

### 400 Bad Request
```json
{
  "detail": "At least one of 'coin_id' or 'category' must be provided"
}
```
**Solution:** Provide at least one filter parameter.

### 404 Not Found
```json
{
  "detail": "Coin or category not found"
}
```
**Solution:** Check that the coin_id or category_id exists.

---

## 📝 Summary Table

| Endpoint | Method | Purpose | Required Params | Optional Params |
|----------|--------|---------|----------------|-----------------|
| `/auth/login` | POST | Get JWT token | username, password | - |
| `/coins` | GET | List all coins | - | page_num, per_page |
| `/categories` | GET | List categories | - | page_num, per_page |
| `/coins/market-data` | GET | Get coins by ID/category | coin_id OR category | page_num, per_page |
| `/coins/{coin_id}` | GET | Get coin by ID | coin_id (path) | category, page_num, per_page |
| `/categories/{category_id}/coins` | GET | Get coins in category | category_id (path) | page_num, per_page |

