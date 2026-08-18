#  Cologne Store — Architecture & Full-Stack System

A scalable, production-oriented e-commerce system for fragrance cataloging and discovery. The system couples a robust, high-performance **FastAPI** backend with a lightweight, reactive **React (Vite)** client.

---

##  Backend Architecture (FastAPI & SQLModel)

The backend is built around a domain-driven, layered architecture designed for strict data validation, secure authentication, and resilient database transactions.

### 1. Architectural Principles & Patterns

* **Layered Separation of Concerns:** Route handlers remain decoupled from business logic and database access, ensuring isolated testing and long-term maintainability.
* **SQLModel & Async Database Sessions:** Unifies Pydantic data validation schemas with SQLAlchemy ORM models, eliminating schema redundancy while supporting full asynchronous operations.
* **Stateless OAuth2 & JWT Flow:** Issues signed JSON Web Tokens (`HS256`/`RS256`) carrying user identity claims and expiration timestamps (`exp`).
* **Granular Dependency Injection:** Reusable FastAPI `Depends` fixtures handle session lifecycle management, request validation, and route-level role-based authorization.
* **Centralized Custom Exception Handlers:** Normalizes error payloads into standardized JSON error responses across the API.

---

## 🛠️ Backend Features & Technical Specifications

### Authentication & User Management
* **Registration (`POST /auth/register`):** Creates new customer accounts with input sanitization and password hashing powered by **Passlib (Bcrypt)**.
* **Token Issuance (`POST /auth/token`):** Fully compliant OAuth2 password flow accepting `application/x-www-form-urlencoded` payloads and returning scoped JWT access tokens.
* **Current User Dependency (`get_current_user`):** Extracts bearer tokens from authorization headers, verifies signatures, and fetches authenticated user instances from the session.

### Cologne Catalog & Inventory Engine
* **Catalog Querying & Search (`GET /colognes`):** Dynamic querying supporting filtering by brand, olfactory family, concentration, and price ranges with pagination support (`limit` & `offset`).
* **Identifier/Slug Lookups (`GET /colognes/{uid_or_slug}`):** High-efficiency single-item retrieval with explicit `404 Not Found` handling.
* **Inventory Control & Mutations (`POST`, `PUT`, `DELETE`):** Administrative endpoints enforcing data constraints, field-level validations, and inventory consistency.

---

## 🔌 API Reference & Data Contracts

| Method | Endpoint | Access | Description | Request Body / Params | Status Codes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Public | Registers a new user account | `UserCreate` (JSON) | `201`, `400`, `409` |
| `POST` | `/auth/token` | Public | Generates JWT access token | Form Data (`username`, `password`) | `200`, `401` |
| `GET` | `/users/me` | Authenticated | Returns current authenticated profile | Header: `Bearer <token>` | `200`, `401` |
| `GET` | `/colognes` | Public | Lists and filters the catalog | Query: `search`, `brand`, `skip`, `limit` | `200` |
| `GET` | `/colognes/{id}`| Public | Fetches detailed cologne data | Path: `id` (UUID / int) | `200`, `404` |
| `POST` | `/colognes` | Admin | Creates a new cologne entry | `CologneCreate` (JSON) | `201`, `401`, `403` |

### Sample JSON Error Response Contract

All exceptions follow a consistent error structure for deterministic client handling:

```json
{
  "code": "EMPTY_INVENTORY",
  "message": "No colognes were found matching the specified query criteria.",
  "variant": "NOT_FOUND",
  "detail": "Query returned 0 records."
}
```
## 🎨 Frontend Architecture & Client-Side Flow (React + Vite)

 A clean three-tier architecture (**Service Layer**, **Hook/State Layer**, and **UI Presentation Layer**) to provide a seamless fragrance discovery and shopping experience. It features centralized data fetching, robust error isolation, and secure JWT authentication.

---

## ✨ Key Features

* **Three-Tier Architecture:** Complete separation of concerns between API communication (services), asynchronous React state management (hooks), and view components (UI).
* **Centralized Data Fetching (`useService` / `useFetch`):**
  * Custom generic hook handling `loading`, `error`, and `data` states.
  * Dependency-tracking re-fetches for reactive queries and search parameters.
  * Built-in request cancellation via native `AbortController` to prevent memory leaks and race conditions.
* **Component-Level Error Isolation (Fault Isolation):**
  * Failure in the catalog/grid displays contextual UI components (`<ErrorUI/>`, `<EmptyState/>`) without breaking navigation or layout elements like the `<Header/>`.
  * Dedicated loading states with animated skeleton cards (`<SkeletonCard/>`).
* **JWT Authentication & Session Management:**
  * Global state management powered by React Context (`AuthContext`).
  * Support for **Login**, **Sign Up** (with automatic authentication), and **Logout**.
  * Persistent user sessions synced with `localStorage`.
* **Axios Interceptors:**
  * **Request Interceptor:** Automatically injects the `Authorization: Bearer <token>` header on authenticated outgoing requests.
  * **Response Interceptor:** Intercepts `401 Unauthorized` responses, cleans up stored session tokens, and redirects users to `/login`.
* **Dynamic Search & Routing:**
  * Declarative client-side routing using `react-router`.
  * Search integration supporting both reactive updates and URL parameter synchronization.

---

## ⚡ Vite Setup & Local Environment

### 1. Prerequisites

* **Python:** `3.10+`
* **Node.js:** `v18.x` or higher
* **Database:** PostgreSQL or SQLite

---

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start FastAPI server
uvicorn main:app --reload --port 8000
```
### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Set: VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
```
