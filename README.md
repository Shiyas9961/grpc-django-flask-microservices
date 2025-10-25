# Django gRPC Product Service with Flask Client

This project demonstrates a **full-stack Python application** with:

- **Django REST Framework** backend with a gRPC server
- **Flask client** consuming gRPC services
- **CRUD operations** for products
- **Swagger API documentation**
- **Dockerized setup**
- **Automated tests** for server and client

---

## **Project Structure**

```
├── client
│   ├── apis                # Flask API endpoints
│   ├── config              # Flask & gRPC configuration
│   ├── grpc_client         # gRPC client services
│   ├── swagger             # Swagger YAML definitions
│   ├── tests               # Client API and gRPC tests
│   └── app.py
├── server
│   ├── apps
│   │   ├── core
│   │   └── products        # Django app for products
│   ├── grpc_server         # gRPC server and proto files
│   ├── tests               # Server tests (models, serializers, views, gRPC)
│   └── settings.py
├── docker-compose.yml
├── README.md
└── requirements-dev.txt / requirements.txt
```

---

## **Setup & Installation**

### 1. Clone the repository

```bash
git clone <repo-url>
cd <project-folder>
```

### 2. Create virtual environments

```bash
# Server
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Client
cd ../client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in `client/`:

```
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key
GRPC_SERVER_HOST=localhost
GRPC_SERVER_PORT=50051
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

---

## **Running the Application**

### 1. Migrate Django database

```bash
cd server
python manage.py makemigrations
python manage.py migrate
```

### 2. Start gRPC server

```bash
python grpc_server/server.py
```

### 3. Start Flask client

```bash
cd client
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

---

## **Docker Setup**

You can also run the entire system using Docker:

```bash
docker-compose up --build
```

This will start:

- Django gRPC server
- Flask client
- Database (if included in Docker Compose)

---

## **API Endpoints (Flask Client)**

- **List Products:** `GET /products`
- **Create Product:** `POST /products`
  ```json
  {
    "name": "Product 1",
    "description": "Sample description",
    "price": 99.99
  }
  ```
- **Get Product:** `GET /products/<product_id>`
- **Update Product:** `PUT /products/<product_id>`
  ```json
  {
    "name": "Updated Product",
    "description": "Updated description",
    "price": 120.00
  }
  ```
- **Delete Product:** `DELETE /products/<product_id>`

### Swagger Documentation

Access Swagger UI:

```
client/swagger/product_swagger.yml
```

---

## **gRPC Service**

The server implements the following methods:

- `ListProducts(Empty) -> ProductList`
- `CreateProduct(ProductRequest) -> ProductResponse`
- `GetProduct(ProductId) -> ProductResponse`
- `UpdateProduct(ProductUpdateRequest) -> ProductResponse`
- `DeleteProduct(ProductId) -> DeleteResponse`

Proto file: `server/grpc_server/product.proto`

---

## **Testing**

### Server Tests

- Models: `server/tests/products/test_models.py`
- Serializers: `server/tests/products/test_serializers.py`
- Views: `server/tests/products/test_views.py`
- gRPC Services: `server/tests/products/test_grpc_service.py`

Run server tests:

```bash
cd server
pytest
```

### Client Tests

- API: `client/tests/test_api.py`
- gRPC client: `client/tests/test_grpc_service.py`

Run client tests:

```bash
cd client
pytest
```

---

## **Admin Interface**

Django admin is available to manage products:

```
/admin
```

- Model: `Product`
- Display fields: `name`, `description`, `price`
- Search: `name`, `description`
- Filters: `name`, `description`, `price`

---

## **Environment Configurations**

- Flask client: `client/config/settings.py`
- gRPC server: `server/grpc_server/server.py`
- Environment variables are used for ports, host, and debug mode.

---

## **Commit Message Guidelines**

Use conventional commits for future development:

```
feat: add new feature
fix: fix a bug
docs: update documentation
test: add or update tests
chore: maintenance tasks
```

---

## **License**

This project is licensed under MIT License.
