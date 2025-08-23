# FastAPI Fundamentals Project

This project demonstrates the installation of FastAPI and the implementation of basic HTTP methods (GET, POST, PUT, DELETE) along with JSON handling.

## Prerequisites

- Python 3.7+
- `pip` (Python package installer)

## Installation

1.  **Clone or Download the Project:**
    Place the `main.py` and `requirements.txt` files in a directory on your local machine.

2.  **Create a Virtual Environment (Recommended):**
    It's good practice to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv .venv
    # Activate the virtual environment
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    # source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    Use `pip` to install the required packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    This command installs FastAPI and all its optional dependencies, including Uvicorn, which is a fast ASGI server used to run the application.

## Running the Application

Navigate to the project directory (where `main.py` is located) and execute the following command:
```bash
python main.py
```
This will start the FastAPI development server using Uvicorn. The application will be available at `http://0.0.0.0:8080`. This host and port configuration makes the API accessible from other machines on the same network, not just locally.

## Exploring the API

FastAPI automatically generates interactive API documentation:
-   **Swagger UI:** Accessible at `http://127.0.0.1:8000/docs`. This provides a user-friendly interface to test the API endpoints.
-   **ReDoc:** Accessible at `http://127.0.0.1:8000/redoc`. This offers an alternative documentation view.

### Available Endpoints

-   `GET /`: Welcome message.
-   `GET /items/`: Retrieve a list of all items (JSON array).
-   `GET /items/{id}`: Retrieve a specific item by its ID (JSON object).
-   `POST /items/`: Create a new item. Send a JSON object in the request body matching the `Item` structure.
-   `PUT /items/{id}`: Update an existing item by its ID. Send a JSON object with the updated data in the request body.
-   `DELETE /items/{id}`: Delete an item by its ID.

### Example `Item` JSON structure:
```json
{
  "id": 1,
  "name": "Sample Item",
  "description": "A sample item for demonstration.",
  "price": 19.99
}
```
The `description` field is optional.

## Key Concepts Demonstrated

-   **FastAPI Installation:** Using `pip install fastapi[all]`.
-   **HTTP Methods:**
    -   `@app.get()`: Defines routes for GET requests.
    -   `@app.post()`: Defines routes for POST requests.
    -   `@app.put()`: Defines routes for PUT requests.
-   `@app.delete()`: Defines routes for DELETE requests.
-   **JSON Handling:**
    -   Using Pydantic models (`Item`) to define data structures for request bodies and response bodies, enabling automatic data validation and (de)serialization.
    -   Receiving JSON data in `POST` and `PUT` requests.
    -   Returning JSON data in `GET` responses.
-   **Path Parameters:** Using `{item_id}` in route paths to capture dynamic values.
-   **Status Codes:** Returning appropriate HTTP status codes (e.g., 201 for created, 204 for no content, 404 for not found).
-   **Error Handling:** Using `HTTPException` to return standard HTTP error responses.
-   **Automatic Documentation:** Leveraging FastAPI's built-in generation of interactive API docs (Swagger UI and ReDoc).
