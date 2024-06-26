# Master Data Service

This project is a Django-based web application with gRPC support for managing a product catalog. It includes models for categories, brands, products, product variants, product images, and product attributes. The application supports CRUD operations via gRPC and provides an admin interface for managing the data.

## Table of Contents

- Features
- Technologies
- Setup
  - Prerequisites
  - Installation
  - Docker Setup
- Usage
  - Running the Application
  - Running the gRPC Client test
- API
- Contributing
- License

## Features

- Django admin interface for managing product catalog
- gRPC API for CRUD operations on products
- Support for nested data structures including product variants, images, and attributes

## Technologies

- Python 3.11
- Django 5.0.6
- Django REST framework 3.15.2
- django-grpc-framework 0.2.1
- gRPC
- Docker

## Setup

### Prerequisites

- Python 3.11
- Docker (optional, for containerization)
- Docker Compose (optional, for containerization)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

### Docker Setup

1. Build the Docker image:

```bash
docker build -t my-django-app .
```

2. Run the Docker container:

```bash
docker run -p 8000:8000 -p 50051:50051 my-django-app
```

Alternatively, use Docker Compose:

1. Build the Docker images:

```bash
docker-compose build
```

2. Run the Docker containers:

```bash
docker-compose up
```

## Usage

### Running the Application

1. Start the Django development server:

```bash
python manage.py runserver
```

2. Start the gRPC server:

```bash
python server.py
```

3. Access the Django admin interface:

Open your browser and go to <http://localhost:8000/admin>. Log in with the superuser credentials you created earlier.

### Running the gRPC Client test

Use the provided `grpc_client.py` script to interact with the gRPC server:

```bash
python grpc_client.py
```

This script will create, retrieve, update, and delete a product, as well as list all products.

## API

### gRPC API

The gRPC API provides the following methods:

- GetProduct(GetProductRequest): Retrieve a product by ID
- CreateProduct(CreateProductRequest): Create a new product
- UpdateProduct(UpdateProductRequest): Update an existing product
- DeleteProduct(DeleteProductRequest): Delete a product by ID
- ListProducts(Empty): List all products

### Protobuf Definitions
Refer to the `master_data.proto` file for the full protobuf definitions.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any features, bug fixes, or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
