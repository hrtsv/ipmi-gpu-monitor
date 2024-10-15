import secrets
import json
import os

def generate_secret_keys():
    secret_key = secrets.token_hex(32)
    jwt_secret_key = secrets.token_hex(32)
    
    secrets_dict = {
        "SECRET_KEY": secret_key,
        "JWT_SECRET_KEY": jwt_secret_key
    }
    
    secrets_file = '/app/secrets.json'
    with open(secrets_file, 'w') as f:
        json.dump(secrets_dict, f)
    
    print("Secret keys generated and saved to secrets.json")

if __name__ == "__main__":
    generate_secret_keys()