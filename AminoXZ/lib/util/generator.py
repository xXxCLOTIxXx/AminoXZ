from typing import Union
from hmac import new
from hashlib import sha1
from base64 import b64encode, urlsafe_b64decode
import json
from typing import Union
from os import urandom
from time import time as timestamp
from time import strftime, gmtime

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
			with open("Device.json", "r") as stream:
				data = json.load(stream)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			device = self.generate_device_info()
			with open("Device.json", "w") as stream:
				json.dump(device, stream, indent=4)
			with open("Device.json", "r") as stream:
				data = json.load(stream)
		return data

	def timezone(self):
		localhour = strftime("%H", gmtime())
		localminute = strftime("%M", gmtime())
		UTC = {"GMT0": '+0', "GMT1": '+60', "GMT2": '+120', "GMT3": '+180', "GMT4": '+240', "GMT5": '+300', "GMT6": '+360',
				"GMT7": '+420', "GMT8": '+480', "GMT9": '+540', "GMT10": '+600', "GMT11": '+660', "GMT12": '+720',
				"GMT13": '+780', "GMT-1": '-60', "GMT-2": '-120', "GMT-3": '-180', "GMT-4": '-240', "GMT-5": '-300',
				"GMT-6": '-360', "GMT-7": '-420', "GMT-8": '-480', "GMT-9": '-540', "GMT-10": '-600', "GMT-11": '-660'};
		hour = [localhour, localminute]
		if hour[0] == "00": tz = UTC["GMT-1"];return int(tz)
		if hour[0] == "01": tz = UTC["GMT-2"];return int(tz)
		if hour[0] == "02": tz = UTC["GMT-3"];return int(tz)
		if hour[0] == "03": tz = UTC["GMT-4"];return int(tz)
		if hour[0] == "04": tz = UTC["GMT-5"];return int(tz)
		if hour[0] == "05": tz = UTC["GMT-6"];return int(tz)
		if hour[0] == "06": tz = UTC["GMT-7"];return int(tz)
		if hour[0] == "07": tz = UTC["GMT-8"];return int(tz)
		if hour[0] == "08": tz = UTC["GMT-9"];return int(tz)
		if hour[0] == "09": tz = UTC["GMT-10"];return int(tz)
		if hour[0] == "10": tz = UTC["GMT13"];return int(tz)
		if hour[0] == "11": tz = UTC["GMT12"];return int(tz)
		if hour[0] == "12": tz = UTC["GMT11"];return int(tz)
		if hour[0] == "13": tz = UTC["GMT10"];return int(tz)
		if hour[0] == "14": tz = UTC["GMT9"];return int(tz)
		if hour[0] == "15": tz = UTC["GMT8"];return int(tz)
		if hour[0] == "16": tz = UTC["GMT7"];return int(tz)
		if hour[0] == "17": tz = UTC["GMT6"];return int(tz)
		if hour[0] == "18": tz = UTC["GMT5"];return int(tz)
		if hour[0] == "19": tz = UTC["GMT4"];return int(tz)
		if hour[0] == "20": tz = UTC["GMT3"];return int(tz)
		if hour[0] == "21": tz = UTC["GMT2"];return int(tz)
		if hour[0] == "22": tz = UTC["GMT1"];return int(tz)
		if hour[0] == "23": tz = UTC["GMT0"];return int(tz)



	def timers(self):
		return [
				{
					'start': int(timestamp()), 'end': int(timestamp()) + 300
				} for _ in range(50)
			]



	#from amino.py
	def decode_sid(self, SID: str) -> dict:return json.loads(urlsafe_b64decode(SID + "=" * (4 - len(SID) % 4))[1:-20])

	def sid_to_uid(self, SID: str) -> str: return self.decode_sid(SID)["2"]

	def sid_to_ip_address(self, SID: str) -> str: return self.decode_sid(SID)["4"]

	def sid_created_time(self, SID: str) -> str: return self.decode_sid(SID)["5"]

	def sid_to_client_type(self, SID: str) -> str: return self.decode_sid(SID)["6"]