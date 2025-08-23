from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Define a Pydantic model for handling JSON data
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# Initialize FastAPI app
app = FastAPI(title="FastAPI Fundamentals Project")

# In-memory storage for items (for demonstration purposes)
items_db = []

# --- HTTP Methods Examples ---

# GET - Retrieve all items
@app.get("/items/", response_model=List[Item])
def get_items():
    """
    Retrieve a list of all items.
    """
    return items_db

# GET - Retrieve a single item by ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """
    Retrieve a specific item by its ID.
    """
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# POST - Create a new item
@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    """
    Create a new item.
    Expects a JSON body matching the Item model.
    """
    # Basic check to prevent duplicate IDs for this demo
    for existing_item in items_db:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db.append(item)
    return item

# PUT - Update an existing item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: Item):
    """
    Update an existing item by its ID.
    Expects a JSON body with the fields to update.
    """
    for index, item in enumerate(items_db):
        if item.id == item_id:
            # For simplicity, replace the whole item. In practice, you might update specific fields.
            items_db[index] = item_update
            return item_update
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE - Delete an item
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """
    Delete an item by its ID.
    """
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return # 204 No Content

# --- Root endpoint ---
@app.get("/")
def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the FastAPI Fundamentals Project!"}

# --- Run the application ---
# This block ensures the app runs when the script is executed directly
if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    # Host is set to "0.0.0.0" to make it accessible on the network
    # Port is set to 8080 as requested
    # To enable reload, pass the app as an import string
    # Assuming this file is named 'main.py' and the app instance is named 'app'
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
