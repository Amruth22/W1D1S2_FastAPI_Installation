import unittest
import asyncio
import aiohttp
import sys

# Base URL for the running API server
BASE_URL = ""
# eg::-BASE_URL = "https://ide-bbfeeedbcaf332013968deeebdeeafecbone.premiumproject.examly.io/proxy/8080/"

class TestMainApp(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Set up test environment before each test method."""
        # Quick connection check only
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{BASE_URL}/", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        self.fail("API server not responding correctly on port 8080.")
            except aiohttp.ClientConnectorError:
                self.fail("Cannot connect to API server. Make sure the server is running on port 8080.")

    async def asyncTearDown(self):
        """Clean up test environment after each test method."""
        # Fast cleanup - delete all items concurrently
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{BASE_URL}/items/", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        items = await response.json()
                        # Delete items concurrently for speed
                        delete_tasks = [
                            session.delete(f"{BASE_URL}/items/{item['id']}", timeout=aiohttp.ClientTimeout(total=5))
                            for item in items
                        ]
                        if delete_tasks:
                            await asyncio.gather(*delete_tasks, return_exceptions=True)
            except aiohttp.ClientConnectorError:
                pass

    async def test_read_root(self):
        """Test the root endpoint."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/", timeout=aiohttp.ClientTimeout(total=3)) as response:
                self.assertEqual(response.status, 200)
                data = await response.json()
                expected_data = {"message": "Welcome to the FastAPI Fundamentals Project!"}
                self.assertEqual(data, expected_data)

    async def test_create_item_success(self):
        """Test creating a new item successfully."""
        sample_item = {
            "id": 101,
            "name": "Laptop",
            "description": "A powerful laptop for development.",
            "price": 1200.00
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BASE_URL}/items/", json=sample_item, timeout=aiohttp.ClientTimeout(total=3)) as response:
                self.assertEqual(response.status, 201)
                data = await response.json()
                self.assertEqual(data, sample_item)

    async def test_get_all_items(self):
        """Test getting all items after adding multiple items."""
        item_a = {"id": 10, "name": "Item A", "price": 100.0}
        item_b = {"id": 20, "name": "Item B", "description": "Desc B", "price": 200.0}
        
        async with aiohttp.ClientSession() as session:
            # Add items concurrently
            await asyncio.gather(
                session.post(f"{BASE_URL}/items/", json=item_a, timeout=aiohttp.ClientTimeout(total=3)),
                session.post(f"{BASE_URL}/items/", json=item_b, timeout=aiohttp.ClientTimeout(total=3))
            )
            
            # Get all items
            async with session.get(f"{BASE_URL}/items/", timeout=aiohttp.ClientTimeout(total=3)) as response:
                self.assertEqual(response.status, 200)
                items_list = await response.json()
                self.assertEqual(len(items_list), 2)

    async def test_update_item_success(self):
        """Test updating an existing item successfully."""
        original_item = {"id": 77, "name": "Original Gadget", "price": 150.0}
        updated_item_data = {"id": 77, "name": "Updated Gadget", "description": "New features.", "price": 175.50}

        async with aiohttp.ClientSession() as session:
            # Add then update the item
            await session.post(f"{BASE_URL}/items/", json=original_item, timeout=aiohttp.ClientTimeout(total=3))
            async with session.put(f"{BASE_URL}/items/{original_item['id']}", json=updated_item_data, timeout=aiohttp.ClientTimeout(total=3)) as response:
                self.assertEqual(response.status, 200)
                data = await response.json()
                self.assertEqual(data, updated_item_data)

    async def test_delete_item_success(self):
        """Test deleting an item successfully."""
        item_to_delete = {"id": 99, "name": "Item to Remove", "price": 25.0}

        async with aiohttp.ClientSession() as session:
            # Add then delete the item
            await session.post(f"{BASE_URL}/items/", json=item_to_delete, timeout=aiohttp.ClientTimeout(total=3))
            async with session.delete(f"{BASE_URL}/items/{item_to_delete['id']}", timeout=aiohttp.ClientTimeout(total=3)) as response:
                self.assertEqual(response.status, 204)

if __name__ == '__main__':
    # Create a test suite and runner for detailed results
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMainApp)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print custom summary
    print(f"\n--- Test Results Summary ---")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("Overall result: SUCCESSFUL")
        sys.exit(0) # Exit with success code
    else:
        print("Overall result: FAILED")
        # Optionally print failure details
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  {test}: {traceback}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  {test}: {traceback}")
        sys.exit(1) # Exit with failure code
