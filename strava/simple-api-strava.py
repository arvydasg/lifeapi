from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

load_dotenv()

# Get the client ID and client secret from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Set the redirect URL for the OAuth flow
redirect_url = "https://arvydas.dev/lifeapi/"

# Create an OAuth2 session with the client ID and redirect URL
session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url)

# Set the authorization URL and scope
auth_base_url = "https://www.strava.com/oauth/authorize"
session.scope = ["profile:read_all"]

# Generate the authorization link
auth_link = session.authorization_url(auth_base_url)

# Print the authorization link and prompt the user to enter the redirect URL
print(f"Click Here: {auth_link[0]}")
redirect_response = input(f"Paste redirect URL here: ")

# Exchange the authorization code for an access token
token_url = "https://www.strava.com/api/v3/oauth/token"
session.fetch_token(
    token_url=token_url,
    client_id=client_id,
    client_secret=client_secret,
    authorization_response=redirect_response,
    include_client_id=True
)

# Make a request to the athlete's profile
response = session.get("https://www.strava.com/api/v3/athlete")

# Print the response information
print("\n\n\n")
print(f"Response Status: {response.status_code}")
print(f"Response Reason: {response.reason}")
print(f"Time Elapsed: {response.elapsed}")
print(f"Response Text: \n{'-'*15}\n{response.text}")