import secrets

# Generate a secure 32-byte key (256 bits)
jwt_secret_key = secrets.token_hex(32)

print("JWT Secret Key:", jwt_secret_key)
print("Length:", len(jwt_secret_key))
