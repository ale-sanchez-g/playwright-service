# playwright-service
A web automation service powered by Playwright that enables programmatic execution of browser-based test flows.
    
## Key Features
- **Test Execution**: Run structured test plans against any website with detailed results
- **Element Interaction**: Click, hover, type, scroll, and check element visibility
- **Navigation**: Visit URLs and inspect page structure and elements
- **Recording**: Capture screenshots and videos during test execution
- **Wait Conditions**: Support for timeouts and page load states
    
This service provides a RESTful API to automate browser interactions for testing, monitoring, and data extraction purposes without requiring direct browser access or Playwright installation.
    
Use cases include:
- Automated UI testing
- Website monitoring
- Content verification
- Data extraction
- Visual regression testing

## Status

[![CI](https://github.com/ale-sanchez-g/playwright-service/actions/workflows/test.yml/badge.svg)](https://github.com/ale-sanchez-g/playwright-service/actions/workflows/test.yml)

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

### How to contribute

Refer to [Contribution](/contribution.md) 

### Sponsors


- [Devops1 Australia](https://devops1.com.au/): Helps your organisation design systems that anticipate risks, adapt to change, and deliver continuous quality.
