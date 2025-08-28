import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8080"

def test_app_health():
    """Test that the FastAPI app is running and accessible"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the FastAPI Fundamentals Project!"
    print("PASS: App health check passed")

def test_create_item():
    """Test creating a new item"""
    item_data = {
        "id": 1,
        "name": "Laptop",
        "description": "A powerful development laptop",
        "price": 1200.00
    }
    
    response = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["id"] == 1
    assert created_item["name"] == "Laptop"
    assert created_item["description"] == "A powerful development laptop"
    assert created_item["price"] == 1200.00
    
    print("PASS: Create item test passed")

def test_get_item_by_id():
    """Test retrieving a specific item by ID"""
    # First create an item
    item_data = {
        "id": 2,
        "name": "Mouse",
        "description": "Wireless gaming mouse",
        "price": 75.99
    }
    
    create_response = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert create_response.status_code == 201
    
    # Now get the item by ID
    get_response = requests.get(f"{BASE_URL}/items/2")
    assert get_response.status_code == 200
    retrieved_item = get_response.json()
    assert retrieved_item["id"] == 2
    assert retrieved_item["name"] == "Mouse"
    assert retrieved_item["price"] == 75.99
    
    print("PASS: Get item by ID test passed")

def test_get_all_items():
    """Test retrieving all items"""
    # Create multiple items first
    items = [
        {"id": 10, "name": "Keyboard", "description": "Mechanical keyboard", "price": 150.00},
        {"id": 11, "name": "Monitor", "description": "4K display", "price": 400.00},
        {"id": 12, "name": "Headphones", "price": 200.00}  # No description
    ]
    
    for item in items:
        response = requests.post(f"{BASE_URL}/items/", json=item)
        assert response.status_code == 201
    
    # Get all items
    response = requests.get(f"{BASE_URL}/items/")
    assert response.status_code == 200
    all_items = response.json()
    assert isinstance(all_items, list)
    assert len(all_items) >= 3  # At least the items we just created
    
    # Check if our items are in the list
    item_ids = [item["id"] for item in all_items]
    assert 10 in item_ids
    assert 11 in item_ids
    assert 12 in item_ids
    
    print("PASS: Get all items test passed")

def test_update_item():
    """Test updating an existing item"""
    # Create an item first
    original_item = {
        "id": 20,
        "name": "Original Item",
        "description": "Original description",
        "price": 100.00
    }
    
    create_response = requests.post(f"{BASE_URL}/items/", json=original_item)
    assert create_response.status_code == 201
    
    # Update the item
    updated_item = {
        "id": 20,
        "name": "Updated Item",
        "description": "Updated description with new features",
        "price": 150.00
    }
    
    update_response = requests.put(f"{BASE_URL}/items/20", json=updated_item)
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Item"
    assert updated_data["description"] == "Updated description with new features"
    assert updated_data["price"] == 150.00
    
    print("PASS: Update item test passed")

def test_delete_item():
    """Test deleting an item"""
    # Create an item first
    item_data = {
        "id": 30,
        "name": "Item to Delete",
        "description": "This item will be deleted",
        "price": 50.00
    }
    
    create_response = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert create_response.status_code == 201
    
    # Delete the item
    delete_response = requests.delete(f"{BASE_URL}/items/30")
    assert delete_response.status_code == 204
    
    # Verify item is deleted by trying to get it
    get_response = requests.get(f"{BASE_URL}/items/30")
    assert get_response.status_code == 404
    
    print("PASS: Delete item test passed")

def test_item_validation():
    """Test item validation errors"""
    # Test missing required fields
    invalid_item = {
        "name": "Invalid Item"
        # Missing id and price
    }
    
    response = requests.post(f"{BASE_URL}/items/", json=invalid_item)
    assert response.status_code == 422  # Validation error
    
    # Test invalid data types
    invalid_item2 = {
        "id": "not_a_number",  # Should be int
        "name": "Test Item",
        "price": "not_a_number"  # Should be float
    }
    
    response2 = requests.post(f"{BASE_URL}/items/", json=invalid_item2)
    assert response2.status_code == 422
    
    print("PASS: Item validation test passed")

def test_duplicate_id_handling():
    """Test handling of duplicate item IDs"""
    item_data = {
        "id": 40,
        "name": "First Item",
        "price": 100.00
    }
    
    # Create first item
    response1 = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert response1.status_code == 201
    
    # Try to create another item with same ID
    duplicate_item = {
        "id": 40,
        "name": "Duplicate Item",
        "price": 200.00
    }
    
    response2 = requests.post(f"{BASE_URL}/items/", json=duplicate_item)
    assert response2.status_code == 400  # Bad request for duplicate ID
    error_data = response2.json()
    assert "already exists" in error_data["detail"]
    
    print("PASS: Duplicate ID handling test passed")

def test_get_nonexistent_item():
    """Test getting an item that doesn't exist"""
    response = requests.get(f"{BASE_URL}/items/99999")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["detail"] == "Item not found"
    
    print("PASS: Get nonexistent item test passed")

def test_update_nonexistent_item():
    """Test updating an item that doesn't exist"""
    update_data = {
        "id": 99998,
        "name": "Nonexistent Item",
        "price": 100.00
    }
    
    response = requests.put(f"{BASE_URL}/items/99998", json=update_data)
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["detail"] == "Item not found"
    
    print("PASS: Update nonexistent item test passed")

def test_item_without_description():
    """Test creating item without optional description field"""
    item_data = {
        "id": 50,
        "name": "Item Without Description",
        "price": 25.99
    }
    
    response = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["id"] == 50
    assert created_item["name"] == "Item Without Description"
    assert created_item["price"] == 25.99
    assert created_item["description"] is None
    
    print("PASS: Item without description test passed")

def test_price_validation():
    """Test price field validation"""
    # Test negative price
    item_with_negative_price = {
        "id": 60,
        "name": "Negative Price Item",
        "price": -10.00
    }
    
    response = requests.post(f"{BASE_URL}/items/", json=item_with_negative_price)
    # Note: The current API doesn't validate negative prices, but this test documents the behavior
    # In a real application, you might want to add validation for positive prices
    assert response.status_code in [201, 422]  # Either accepts or validates
    
    # Test zero price
    item_with_zero_price = {
        "id": 61,
        "name": "Zero Price Item",
        "price": 0.00
    }
    
    response2 = requests.post(f"{BASE_URL}/items/", json=item_with_zero_price)
    assert response2.status_code == 201  # Zero price is typically valid
    
    print("PASS: Price validation test passed")

def test_large_item_list():
    """Test handling of multiple items"""
    # Create multiple items to test list handling
    base_id = 100
    items_to_create = 5
    
    for i in range(items_to_create):
        item_data = {
            "id": base_id + i,
            "name": f"Bulk Item {i+1}",
            "description": f"Description for bulk item {i+1}",
            "price": 10.00 * (i + 1)
        }
        
        response = requests.post(f"{BASE_URL}/items/", json=item_data)
        assert response.status_code == 201
    
    # Get all items and verify count
    response = requests.get(f"{BASE_URL}/items/")
    assert response.status_code == 200
    all_items = response.json()
    
    # Check that our bulk items are present
    bulk_item_ids = [base_id + i for i in range(items_to_create)]
    existing_ids = [item["id"] for item in all_items]
    
    for bulk_id in bulk_item_ids:
        assert bulk_id in existing_ids
    
    print("PASS: Large item list test passed")

def test_json_response_format():
    """Test that responses are properly formatted JSON"""
    # Test root endpoint JSON format
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    
    # Test items list JSON format
    response2 = requests.get(f"{BASE_URL}/items/")
    assert response2.status_code == 200
    assert response2.headers.get("content-type", "").startswith("application/json")
    data = response2.json()
    assert isinstance(data, list)
    
    print("PASS: JSON response format test passed")

def run_all_tests():
    """Run all tests and provide summary"""
    print("Running synchronous API tests for FastAPI Installation project...")
    print("Server should be running at: http://localhost:8080")
    print("=" * 70)
    
    # List of all test functions
    test_functions = [
        test_app_health,
        test_create_item,
        test_get_item_by_id,
        test_get_all_items,
        test_update_item,
        test_delete_item,
        test_item_validation,
        test_duplicate_id_handling,
        test_get_nonexistent_item,
        test_update_nonexistent_item,
        test_item_without_description,
        test_price_validation,
        test_large_item_list,
        test_json_response_format
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"FAIL: {test_func.__name__} - {e}")
            failed += 1
    
    print("=" * 70)
    print(f"📊 Test Results Summary:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total: {passed + failed}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        print("✅ FastAPI Installation project is working correctly")
        return True
    else:
        print(f"⚠️  {failed} test(s) failed")
        return False

if __name__ == "__main__":
    print("🚀 Starting FastAPI Installation Project Sync Tests")
    print("📋 Make sure the API server is running: python main.py")
    print("🔧 Server should be accessible at http://localhost:8080")
    print()
    
    # Run the tests
    success = run_all_tests()
    exit(0 if success else 1)