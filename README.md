# Salesforce_refresh_token_IICS
This is a python script for easy generation of the salesforce refresh token for Oauth connectivity for IICS.

The following project was developed for creating salesforce refresh tokens for connectivity with IICS. Used gemini 3.0 pro for support and comments/readability.

This script is a direct automation of the functionality from following article: 
https://knowledge.informatica.com/s/article/000209105?language=en_US

Before running the script, make sure the connected app is configured in salesforce properly with all the settings (refer to the article)

Download this script and run it in your local machine. Make sure you have the following credentials ready beforehand:
1. Login URL
2. Client ID
3. Client Secret
4. Redirect URI
5. Username
6. Password

When browser opens a salesforce window:
1. Login using the credentials.
**** 2. Copy the entire url from the bar after logging in and paste in python.
   Make sure the url looks something like this : https://login.salesforce.com/?code=aPrxYXyxzkuBzbDGdwv67qekAQredtrsWqtxxxxxxx
3. The refresh token should be visible in terminal now. 
