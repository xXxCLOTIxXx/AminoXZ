import hmac
from os import urandom
from hashlib import sha1
import json
from base64 import urlsafe_b64decode


def generate_device_info():
	identifier = urandom(20)
	key = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
	mac = hmac.new(key, bytes.fromhex("42") + identifier, sha1)
	device = f"42{identifier.hex()}{mac.hexdigest()}".upper()
	return {
		"device_id": device,
		"user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.5.33562)"
	}



def sid_to_uid(sid: str) -> str: return json.loads(urlsafe_b64decode(sid + "=" * (4 - len(sid) % 4))[1:-20])["2"]
def sid_to_ip_address(sid: str) -> str: return json.loads(urlsafe_b64decode(sid + "=" * (4 - len(sid) % 4))[1:-20])["4"]
def sid_to_created_time(sid: str) -> str: return json.loads(urlsafe_b64decode(sid + "=" * (4 - len(sid) % 4))[1:-20])["5"]
def sid_to_client_type(sid: str) -> str: return json.loads(urlsafe_b64decode(sid + "=" * (4 - len(sid) % 4))[1:-20])["6"]