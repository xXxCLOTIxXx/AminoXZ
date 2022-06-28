from typing import Union
from hmac import new
from hashlib import sha1
from base64 import b64encode
import json

from .helpers import generate_device_info

class Generator():
	PREFIX = bytes.fromhex("42")
	SIG_KEY = bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93")
	DEVICE_KEY = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
	def deviceId(self):
		try:
			with open("device.json", "r") as stream:
				data = json.load(stream)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			device = generate_device_info()
			with open("device.json", "w") as stream:
				json.dump(device, stream, indent=4)
			with open("device.json", "r") as stream:
				data = json.load(stream)
		return data


	def signature(self, data) -> str:
		try: dt = data.encode("utf-8")
		except Exception: dt = data
		mac = new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), dt, sha1)
		return b64encode(bytes.fromhex("42") + mac.digest()).decode("utf-8")