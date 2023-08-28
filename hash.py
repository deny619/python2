import bcrypt

# Generate a salt and hash a password
password = "Password@1234".encode('utf-8')  # Convert the password to bytes
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password, salt)

# Store `hashed_password` in your storage or database
print(hashed_password)

stored_hashed_password = b'$2b$12$QkH5EWddnMECUTrGdd1H.OHOelGE0.wVJjsIF86D8egS7nQ8XMgWS'

# User input password
user_password = "Password@1234".encode('utf-8')

# Verify the password
if bcrypt.checkpw(user_password, stored_hashed_password):
    print("Password is correct")
else:
    print("Password is incorrect")