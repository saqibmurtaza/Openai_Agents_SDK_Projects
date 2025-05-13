from web_scraper_agent.load_env_var import (
    SHEET_ID,
    SHEET_NAME,
)
from google.oauth2.service_account import Credentials
import os, gspread

def test_google_sheets_access():
    """Test function to verify Google Sheets access"""
    try:
        # Path to credentials file
        creds_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "null"))
        print(f"Looking for credentials at: {creds_path}")
        
        if not os.path.exists(creds_path):
            print(f"❌ Credentials file not found at {creds_path}")
            return False
            
        # Define the scope
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Initialize credentials
        credentials = Credentials.from_service_account_file(creds_path, scopes=scope)
        
        # Get service account email from the credentials
        service_account_email = credentials.service_account_email
        print(f"Service account email: {service_account_email}")
        
        # Initialize the client
        client = gspread.authorize(credentials)
        print(f"✅ Successfully authenticated with service account")
        
        # Get the sheet ID from environment
        sheet_id = SHEET_ID
        if not sheet_id:
            print("❌ SHEET_ID environment variable not set")
            return False
            
        print(f"Attempting to open spreadsheet with ID: {sheet_id}")
        
        # Try to open the spreadsheet
        try:
            spreadsheet = client.open_by_key(sheet_id)
            print(f"✅ Successfully opened spreadsheet: {spreadsheet.title}")
            
            # List all worksheets
            print("Available worksheets:")
            for worksheet in spreadsheet.worksheets():
                print(f"- {worksheet.title}")
                
            return True
        except Exception as e:
            print(f"❌ Error opening spreadsheet: {str(e)}")
            print("Make sure:")
            print("1. The Sheet ID is correct")
            print(f"2. You've shared the sheet with {service_account_email}")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing Google Sheets client: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_google_sheets_access()
