import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Salesforce Token Gen", layout="centered")

st.title("Salesforce OAuth Generator")
st.markdown("Use this tool to generate Refresh Tokens for Informatica IICS.")

# --- Inputs ---
st.header("1. Configuration")
base_url = st.text_input("Base URL", value="https://login.salesforce.com")
client_id = st.text_input("Consumer Key (Client ID)")
client_secret = st.text_input("Consumer Secret", type="password")
redirect_uri = st.text_input("Redirect URI", value="https://login.salesforce.com")

# --- Logic ---
if client_id and redirect_uri:
    # Construct the Auth URL
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri
    }
    auth_url = f"{base_url}/services/oauth2/authorize?{urllib.parse.urlencode(params)}"

    st.header("2. Authorization")
    st.info("Click the link below to log in. After logging in, you will be redirected to a URL. Copy that entire URL.")
    
    # Display the link as a button-like object
    st.markdown(f"[**👉 Click here to Login to Salesforce**]({auth_url})", unsafe_allow_html=True)

    # --- Exchange ---
    st.header("3. Get Tokens")
    pasted_url = st.text_input("Paste the full redirected URL here:")

    if st.button("Generate Tokens"):
        if not pasted_url:
            st.error("Please paste the URL first.")
        else:
            try:
                # Extract code from URL
                parsed = urllib.parse.urlparse(pasted_url)
                qs = urllib.parse.parse_qs(parsed.query)
                code = qs.get("code", [None])[0]

                if not code:
                    st.error("Could not find 'code' in the URL.")
                else:
                    # Request Tokens (Server-Side request, so NO CORS)
                    token_url = f"{base_url}/services/oauth2/token"
                    payload = {
                        "grant_type": "authorization_code",
                        "code": code,
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "redirect_uri": redirect_uri
                    }
                    
                    with st.spinner("Exchanging code for tokens..."):
                        response = requests.post(token_url, data=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Success!")
                        
                        st.subheader("Access Token")
                        st.code(data.get("access_token"), language="text")
                        
                        st.subheader("Refresh Token (Use in Informatica)")
                        st.code(data.get("refresh_token"), language="text")
                        
                        st.subheader("Instance URL")
                        st.code(data.get("instance_url"), language="text")
                    else:
                        st.error(f"Error: {response.status_code}")
                        st.json(response.json())

            except Exception as e:
                st.error(f"Error: {str(e)}")