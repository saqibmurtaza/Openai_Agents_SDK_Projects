# test_googlesheet.py

import gspread
import logging
import os
# from google.oauth2.service_account import Credentials # Not needed if using service_account directly

# Import the function you want to test
from tools.save_to_google import save_to_sheet # Import only the function

# Configure basic logging for the test script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- gspread Authentication Setup ---
GOOGLE_CREDENTIALS_FILE = os.path.join(os.getcwd(), "gc.json")

try:
    test_client = gspread.service_account(filename=GOOGLE_CREDENTIALS_FILE)
    logging.info("gspread client authenticated successfully in test script.")
except Exception as e:
    logging.error(f"Failed to authenticate gspread client in test script: {e}")
    logging.error("Please check your credentials file path and contents.")
    exit() # Exit if authentication fails

# --- Test Data and Parameters ---
TEST_SHEET_URL = "https://docs.google.com/spreadsheets/d/1q5SSZstyJozocO97giC4gFCFB8MEnU5cj6_ZKEle0OQ/edit?gid=0#gid=0"

# Test data simulating products from different URLs
TEST_PRODUCTS_HEELS = [
    {"name": "Elegant Stiletto", "price": "75.00", "color": "Black"},
    {"name": "Comfortable Wedge", "price": "55.50", "color": "Brown"},
]
TEST_URL_HEELS = "https://maguireshoes.com/collections/heels"

TEST_PRODUCTS_SNEAKERS = [
    {"name": "Running Sneaker", "price": "90.00", "size": "10", "brand": "Nike"},
    {"name": "Casual Sneaker", "price": "60.00", "size": "8", "brand": "Adidas"},
    {"name": "High-Top Sneaker", "price": "120.00", "size": "9", "brand": "Converse"},
]
TEST_URL_SNEAKERS = "https://maguireshoes.com/collections/sneakers"

# Add another test case with slightly different product keys
TEST_PRODUCTS_SANDALS = [
    {"product_name": "Summer Sandal", "cost": "30.00", "material": "Leather"},
    {"product_name": "Beach Flip Flop", "cost": "15.00", "material": "Rubber"},
]
TEST_URL_SANDALS = "https://maguireshoes.com/collections/sandals"


# --- Run the Test ---
if __name__ == "__main__":
    if TEST_SHEET_URL == "YOUR_TEST_GOOGLE_SHEET_URL_HERE":
        print("-----------------------------------------------------------")
        print("ERROR: Please replace 'YOUR_TEST_GOOGLE_SHEET_URL_HERE' with")
        print("the actual URL of your test Google Sheet.")
        print("-----------------------------------------------------------")
    else:
        print(f"Starting test for save_to_sheet function with dynamic tab names...")

        # Test Case 1: Heels
        print(f"\nTesting with URL: {TEST_URL_HEELS}")
        test_result_heels = save_to_sheet(test_client, TEST_SHEET_URL, TEST_PRODUCTS_HEELS, TEST_URL_HEELS)
        print(f"Result for {TEST_URL_HEELS}: {test_result_heels}")

        # Test Case 2: Sneakers
        print(f"\nTesting with URL: {TEST_URL_SNEAKERS}")
        test_result_sneakers = save_to_sheet(test_client, TEST_SHEET_URL, TEST_PRODUCTS_SNEAKERS, TEST_URL_SNEAKERS)
        print(f"Result for {TEST_URL_SNEAKERS}: {test_result_sneakers}")

        # Test Case 3: Sandals (with different keys)
        print(f"\nTesting with URL: {TEST_URL_SANDALS}")
        test_result_sandals = save_to_sheet(test_client, TEST_SHEET_URL, TEST_PRODUCTS_SANDALS, TEST_URL_SANDALS)
        print(f"Result for {TEST_URL_SANDALS}: {test_result_sandals}")


        print("\n--- Overall Test Summary ---")
        if "Successfully saved" in test_result_heels and \
           "Successfully saved" in test_result_sneakers and \
           "Successfully saved" in test_result_sandals:
            print("All dynamic tab tests PASSED!")
            print(f"Check your Google Sheet at {TEST_SHEET_URL} to verify the data in the dynamically created tabs ('Heels', 'Sneakers', 'Sandals').")
        else:
            print("Some dynamic tab tests FAILED.")
            print("Please review the output above for details.")
