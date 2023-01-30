from typing import Union
from hmac import new
from hashlib import sha1
from base64 import b64encode, urlsafe_b64decode
import json
from typing import Union
from os import urandom



class Generator:
	def __init__(self):
		self.PREFIX = bytes.fromhex("19")
		self.SIG_KEY = bytes.fromhex("DFA5ED192DDA6E88A12FE12130DC6206B1251E44")
		self.DEVICE_KEY = bytes.fromhex("E7309ECC0953C6FA60005B2765F99DBBC965C8E9")


	def signature(self, data: Union[str, bytes]):
		data = data if isinstance(data, bytes) else data.encode("utf-8")
		return b64encode(self.PREFIX + new(self.SIG_KEY, data, sha1).digest()).decode("utf-8")


	def generateDeviceId(self):
		ur = self.PREFIX + (urandom(20))
		mac = new(self.DEVICE_KEY, ur, sha1)
		return f"{ur.hex()}{mac.hexdigest()}".upper()



	def generate_device_info(self):
		return {
			"device_id": self.generateDeviceId(),
			"iphone_user_agent": "Apple iPhone12,1 iOS v15.5 Main/3.12.2",
			'android_user_agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/star2ltexx-user 7.1.; com.narvii.amino.master/3.4.33602)'
		}


	def getDeviceId(self):
		try:
			with open("device.json", "r") as stream:
				data = json.load(stream)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			device = self.generate_device_info()
			with open("device.json", "w") as stream:
				json.dump(device, stream, indent=4)
			with open("device.json", "r") as stream:
				data = json.load(stream)
		return data

	#from amino.py
	def decode_sid(self, SID: str) -> dict:return json.loads(urlsafe_b64decode(SID + "=" * (4 - len(SID) % 4))[1:-20])

	def sid_to_uid(self, SID: str) -> str: return self.decode_sid(SID)["2"]

	def sid_to_ip_address(self, SID: str) -> str: return self.decode_sid(SID)["4"]

	def sid_created_time(self, SID: str) -> str: return self.decode_sid(SID)["5"]

	def sid_to_client_type(self, SID: str) -> str: return self.decode_sid(SID)["6"]