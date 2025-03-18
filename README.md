# playwright-service
This is a playwright service to support simple test execution of test flows

## FastAPI Setup and Usage

This project includes a simple Python API using FastAPI.

### Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Docker

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ale-sanchez-g/playwright-service.git
   cd playwright-service
   ```
2. Create Python virtual env
   ```bash
      python3 -m venv pwservice
      source pwservice/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the FastAPI Server locally

To run the FastAPI server, use the following command:
```bash
python service.py
```

The server will be available at `http://127.0.0.1:8000`.

### Running the FastAPI Server in docker

To run the FastAPI server, use the following command:
```bash
docker-compose up
```

### Endpoints

- **Root Endpoint**: Returns a welcome message.
  ```http
  GET /
  ```

- **Execute Test Plan**: Executes a test plan on a specified URL.
  ```http
  POST /execute
  ```
  **Request Body**:
  ```json
  {
    "test_plan": {
      "steps": [
        {
          "action": "click",
          "selector": "#button",
          "description": "Click the button",
          "critical": true
        }
        // ... other steps ...
      ]
    },
    "url": "http://example.com",
    "record_video": true
  }
  ```

- **Navigate to URL**: Navigates to a URL and returns a map of all elements.
  ```http
  POST /navigate
  ```
  **Request Body**:
  ```json
  {
    "url": "http://example.com"
  }
  ```
