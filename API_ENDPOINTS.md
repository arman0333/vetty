# API Endpoints Documentation

## Version 1.0 Endpoints

### 1. List All Coins (including coin id)
**Endpoint:** `GET /coins`

**Description:** Lists all coins with their IDs, symbols, and names.

**Query Parameters:**
- `page_num` (int, default: 1): Page number
- `per_page` (int, default: 10): Items per page

**Example:**
```
GET /coins?page_num=1&per_page=10
```

**Response:** Paginated list of coins with `id`, `symbol`, and `name`

---

### 2. List Coin Categories
**Endpoint:** `GET /categories`

**Description:** Lists all coin categories.

**Query Parameters:**
- `page_num` (int, default: 1): Page number
- `per_page` (int, default: 10): Items per page

**Example:**
```
GET /categories?page_num=1&per_page=10
```

**Response:** Paginated list of categories with `category_id` and `name`

---

### 3. List Specific Coins (by ID and/or Category)
**Endpoint:** `GET /coins/market-data`

**Description:** Lists specific coins filtered by coin ID from the listing endpoint and/or category from the categories endpoint. Shows market data in INR (Indian Rupee) and CAD (Canadian Dollar).

**Query Parameters:**
- `coin_id` (string, optional): Coin ID(s) from `/coins` endpoint (comma-separated for multiple: `bitcoin,ethereum`)
- `category` (string, optional): Category ID from `/categories` endpoint
- `page_num` (int, default: 1): Page number
- `per_page` (int, default: 10): Items per page

**Note:** At least one of `coin_id` or `category` must be provided.

**Examples:**

1. **Filter by coin ID only:**
   ```
   GET /coins/market-data?coin_id=bitcoin,ethereum&page_num=1&per_page=10
   ```

2. **Filter by category only:**
   ```
   GET /coins/market-data?category=defi&page_num=1&per_page=10
   ```

3. **Filter by both coin ID AND category:**
   ```
   GET /coins/market-data?coin_id=bitcoin&category=defi&page_num=1&per_page=10
   ```

**Response:** Paginated list of coins with market data:
- `id`: Coin ID
- `symbol`: Coin symbol
- `name`: Coin name
- `current_price_inr`: Current price in Indian Rupee
- `current_price_cad`: Current price in Canadian Dollar
- `market_cap_inr`: Market cap in Indian Rupee
- `market_cap_cad`: Market cap in Canadian Dollar
- `price_change_percentage_24h`: 24h price change percentage

---

## Alternative Endpoint

### Get Coin by ID (Path Parameter)
**Endpoint:** `GET /coins/{coin_id}`

**Description:** Alternative way to get coins by ID using path parameter. Can also filter by category.

**Path Parameters:**
- `coin_id` (string): Coin ID (comma-separated for multiple: `bitcoin,ethereum`)

**Query Parameters:**
- `category` (string, optional): Category ID to filter
- `page_num` (int, default: 1): Page number
- `per_page` (int, default: 10): Items per page

**Example:**
```
GET /coins/bitcoin,ethereum?category=defi&page_num=1&per_page=10
```

---

## Pagination

All endpoints support pagination with:
- `page_num`: Page number (starts at 1)
- `per_page`: Items per page (default: 10, max: 250)

**Pagination Response Format:**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 100,
  "total_pages": 10,
  "data": [...]
}
```

---

## Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Get a token from: `POST /auth/login`

