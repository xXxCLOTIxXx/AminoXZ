from .generator import Generator

class Headers:
	def __init__(self, deviceId: str = None, sid: str = None):
		self.deviceId = deviceId
		self.sid=sid
		self.device = Generator().getDeviceId()
		self.User_Agent_Iphone, self.User_Agent_Android = self.device["iphone_user_agent"], self.device["android_user_agent"]

	def iphone_headers(self, data = None, content_type = None):

		headers = {
			"NDCDEVICEID": self.deviceId if self.deviceId is not None else self.device["device_id"],
			"NDCLANG": "ru",
			"Accept-Language": "ru-RU",
			"SMDEVICEID": "20230109055041eecd2b9dd8439235afe4522cb5dacd26011dba6bbfeeb752", 
			"User-Agent": self.User_Agent_Iphone,
			"Content-Type": "application/json; charset=utf-8",
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Upgrade"
			}


		if data is not None:
			headers["Content-Length"] = str(len(data))
			headers["NDC-MSG-SIG"] = Generator().signature(data=data)

		if self.sid:headers["NDCAUTH"] = f"sid={self.sid}"

		if content_type:headers["Content-Type"] = content_type

		return headers

	def android_headers(self, data = None, content_type = None):

		headers = {
			"NDCDEVICEID": self.deviceId if self.deviceId is not None else self.device["device_id"],
			"Accept-Language": "en-US",
			"Content-Type": "application/json; charset=utf-8",
			"User-Agent": self.User_Agent_Android,
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Upgrade"
		}

		if data:
			headers["Content-Length"] = str(len(data))
			headers["NDC-MSG-SIG"] = Generator().signature(data=data)

		if self.sid: headers["NDCAUTH"] = f"sid={self.sid}"
		if content_type: headers["Content-Type"] = type


		return headers



	def iphoneWeb_headers(self):
		return None

	def web_headers(self):
		return None