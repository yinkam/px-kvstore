# px-kvstore by Yinka Makanjuola

A simple in-memory key-value store with a RESTful API.

## Features

- **Create/Update:** Add or modify key-value pairs.
- **Read:** Retrieve values by key.
- **Delete:** Remove key-value pairs.
- **Thread-safe:** Operations are protected by locks to ensure data consistency in a multi-threaded environment.
- **RESTful API:** Easy-to-use HTTP interface for interacting with the store.
- **Dockerized:** Comes with a Dockerfile for easy containerization and deployment.

## API Usage

The server listens on port `8000` by default.

### Create or Update a Key-Value Pair

- **Method:** `POST`
- **Endpoint:** `/`
- **Body (JSON):**
  ```json
  {
    "key": "your-key",
    "value": "your-value"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "message": "Key created/updated successfully."
  }
  ```

### Read a Value by Key

- **Method:** `GET`
- **Endpoint:** `/?key=your-key`
- **Success Response (200 OK):**
  ```json
  {
    "key": "your-key",
    "value": "your-value"
  }
  ```
- **Error Response (404 Not Found):**
  ```json
  {
    "error": "Key 'your-key' not found."
  }
  ```

### Delete a Key-Value Pair

- **Method:** `DELETE`
- **Endpoint:** `/?key=your-key`
- **Success Response (200 OK):**
  ```json
  {
    "message": "Key deleted successfully."
  }
  ```
- **Error Response (404 Not Found):**
  ```json
  {
    "error": "Key 'your-key' not found."
  }
  ```

## Installation and Running

### Prerequisites

- Python 3.7+

### Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/px-kvstore.git
    cd px-kvstore
    ```

2.  **Run the server:**
    ```bash
    python3 server.py
    ```
    The server will start on `http://localhost:8000`.

## Testing

To run the unit tests for the key-value store and the server, execute the following commands:

```bash
python3 test_key_value_store.py
python3 test_server.py
```

## Docker

### Build the Docker Image

```bash
docker build -t px-kvstore .
```

### Run the Docker Container

```bash
docker run -p 8000:8000 px-kvstore
```

The server will be accessible at `http://localhost:8000`.