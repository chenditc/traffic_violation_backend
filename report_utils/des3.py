from Crypto.Cipher import DES3
import base64

DEFAULT_KEY = "shjjappshjjappshjjappdic"
DEFAULT_SALT = "shjjapp0"

def r_pad(payload, block_size=8):
    length = block_size - (len(payload) % block_size)
    return payload + (chr(length) * length).encode("ascii")

def decrypt_message(message, key=None, iv=None):
	if key is None:
		key = DEFAULT_KEY
	if iv is None:
		iv = DEFAULT_SALT
	cipher = DES3.new(key.encode("utf-8"), DES3.MODE_CBC, iv.encode("utf-8"))
	byte_message = cipher.decrypt(base64.b64decode(message))
	return byte_message.decode("utf-8")

def encrypt_message(message, key=None, iv=None):
	if key is None:
		key = DEFAULT_KEY
	if iv is None:
		iv = DEFAULT_SALT
	cipher = DES3.new(key.encode("utf-8"), DES3.MODE_CBC, iv.encode("utf-8"))
	byte_message = base64.b64encode(cipher.encrypt(r_pad(message.encode('utf-8'))))
	return byte_message.decode('utf-8')