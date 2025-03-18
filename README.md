# playwright-service
This is a playwright service to support simple test execution of test flows

## FastAPI Setup and Usage

This project includes a simple Python API using FastAPI.

### Requirements

- Python 3.7+
- FastAPI
- Uvicorn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ale-sanchez-g/playwright-service.git
   cd playwright-service
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the FastAPI Server

To run the FastAPI server, use the following command:
```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

### Endpoints

- **Root Endpoint**: Returns a welcome message.
  ```http
  GET /
  ```

- **Sample Endpoint**: Returns a sample JSON response.
  ```http
  GET /sample
  ```
