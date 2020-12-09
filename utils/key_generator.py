import binascii

from Crypto.PublicKey import RSA


def bin2hex(bin_str):
    return binascii.hexlify(bin_str)


key = RSA.generate(2048)
private_key = bin2hex(key.exportKey('DER'))
pub_key = bin2hex(key.publickey().exportKey('DER'))

print(private_key)
print()
print(pub_key)
