from cryptography.fernet import Fernet
# Generate a key and print it (save it securely)
key = Fernet.generate_key()
print("Generated Key:", key.decode())
