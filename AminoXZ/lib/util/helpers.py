import hmac
from os import urandom
from hashlib import sha1


def generate_device_info():
	identifier = urandom(20)
	key = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
	mac = hmac.new(key, bytes.fromhex("42") + identifier, sha1)
	device = f"42{identifier.hex()}{mac.hexdigest()}".upper()
	return {
		"device_id": device,
		"user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.5.33562)"
	}