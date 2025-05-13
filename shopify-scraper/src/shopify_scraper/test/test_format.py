import json
import re

def extract_and_show_json_from_string(input_string: str):
    """
    Extracts a JSON object from a string enclosed in triple backticks (```json ... ```)
    and prints the extracted data.

    Args:
        input_string: The input string potentially containing a JSON block.

    Returns:
        The extracted Python object (usually a dictionary or list), or None if no
        valid JSON block is found.
    """
    print(f"--- Processing Input String ---")
    # Print only a portion for clarity in case of very long inputs
    print(input_string[:500] + "..." if len(input_string) > 500 else input_string)
    print("-------------------------------")

    # Use regex to find the JSON block enclosed in ```json and ```
    # Corrected regex to handle newline after ```json  
    match = re.search(r"```json\s*\n?(.*?)\s*```", input_string, re.DOTALL)  

    extracted_json_string = None  
    if match:  
        # Group 1 (.*?) captures the content between the backticks (after ```json and optional newline)
        extracted_json_string = match.group(1).strip()
        print(f"Found potential JSON block:\n{extracted_json_string[:500] + '...' if len(extracted_json_string) > 500 else extracted_json_string}") # Print portion
    else:
        print("No ```json ... ``` block found in the string.")
        return None

    if extracted_json_string:
        try:
            # Attempt to parse the extracted string as JSON
            extracted_object = json.loads(extracted_json_string)
            print("\n--- Successfully Parsed JSON Object ---")
            print(json.dumps(extracted_object, indent=2)) # Print with indentation for readability
            print("---------------------------------------")
            return extracted_object
        except json.JSONDecodeError as e:
            print(f"\nError decoding JSON: {e}")
            print("-----------------------")
            return None
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("-------------------------------")
            return None
    else:
        # This case should be covered by the `if match:` check, but good practice
        print("Extracted string was empty after stripping whitespace.")
        return None

# --- Example Usage (using your exact output format for dummy_input_1) ---

dummy_input_1_corrected = """
Some introductory text.
Here is the data:
```json  
[  
  {  
    "Title": "Simone White Trainer",  
    "Price": "240.00",  
    "Description": "Handmade in Houjie, China . Vintage-inspired, but you'll wear these for days to come. With its sleek silhouette and signat"  
  },  
  {  
    "Title": "Another Shoe",  
    "Price": "150.00",  
    "Description": "A comfortable everyday shoe."  
  }  
]
```  
"""

extract_and_show_json_from_string(dummy_input_1_corrected)

# dummy_input_2 = """ Data with an error:
# [  
#   {  
#     "Title": "Mismatched Quotes",  
#     "Price": "100.00  
#   }  
# ]  
# """
# extract_and_show_json_from_string(dummy_input_2)

# dummy_input_3 = """ Just some plain text. No structured data here. """
# extract_and_show_json_from_string(dummy_input_3)

# dummy_input_4 = """ Empty data:"""
# extract_and_show_json_from_string(dummy_input_4)