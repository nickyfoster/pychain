from Crypto.PublicKey import RSA

private_key = RSA.generate(1024)  # -> convert to hex
pub_key = private_key.publickey()  # -> convert to hex

print(f"Private key: {private_key}")
print(f"Public key: {pub_key}")
