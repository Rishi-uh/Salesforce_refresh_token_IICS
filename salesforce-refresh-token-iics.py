import requests
import urllib.parse
import webbrowser

def get_salesforce_tokens_browser():
    print("--- Salesforce OAuth Token Generator (Browser Flow) ---\n")
    
    # 1. Gather Inputs
    base_url = input("Enter Salesforce Base URL (Press Enter for 'https://login.salesforce.com'): ").strip()
    if not base_url:
        base_url = "https://login.salesforce.com"
    
    # Remove trailing slash if present
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    client_id = input("Enter Consumer Key (Client ID): ").strip()
    client_secret = input("Enter Consumer Secret (Client Secret): ").strip()
    
    # NEW: Input for Redirect URI
    redirect_uri = input("Enter Redirect URI (Callback URL): ").strip()
    
    # 2. Construct Authorization URL
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri
    }
    
    # Create the URL string
    auth_url = f"{base_url}/services/oauth2/authorize?{urllib.parse.urlencode(auth_params)}"
    
    print("-" * 60)
    print("Step 1: Authorization")
    print("I will now open your browser. Please log in and allow access.")
    print(f"Auth URL: {auth_url}")
    print("-" * 60)
    
    # Open the default web browser
    webbrowser.open(auth_url)
    
    # 3. Capture the Code
    print("\nAFTER you allow access, you will be redirected to your Callback URL.")
    print(f"The URL will look like: {redirect_uri}?code=aPrxYXyx... (long string)")
    print("\n>>> COPY that entire URL from your browser address bar and paste it below.")
    
    redirected_url = input("Paste the full redirected URL here: ").strip()
    
    try:
        # Extract the 'code' parameter from the URL
        parsed_url = urllib.parse.urlparse(redirected_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        # Get the first code found
        auth_code = query_params.get('code', [None])[0]
        
        if not auth_code:
            print("Error: Could not find 'code' in the URL provided.")
            return
            
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return

    # 4. Exchange Code for Tokens
    print("\nStep 2: Exchanging Code for Tokens...")
    
    token_url = f"{base_url}/services/oauth2/token"
    
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }
    
    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status() # Check for HTTP errors
        
        tokens = response.json()
        
        print("\n" + "=" * 60)
        print("SUCCESS! Credentials for Informatica:")
        print("=" * 60)
        print(f"Access Token  : {tokens.get('access_token')}")
        print(f"Refresh Token : {tokens.get('refresh_token')}")
        print(f"Instance URL  : {tokens.get('instance_url')}")
        print("=" * 60)
        print("\nNote: Use the 'Refresh Token' and 'Instance URL' for your IICS Connection.")

    except requests.exceptions.HTTPError as err:
        print("\nRequest Failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_salesforce_tokens_browser()