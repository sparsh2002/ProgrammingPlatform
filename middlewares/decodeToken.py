import jwt
import os
from dotenv import load_dotenv
load_dotenv()
# Secret key for JWT token decoding
secret_key = os.getenv('MY_SECRET')

# Function to decode JWT token
def decode_token(token):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Handle token expiration error
        print("Token has expired.")
    except jwt.InvalidTokenError:
        # Handle invalid token error
        print("Invalid token.")