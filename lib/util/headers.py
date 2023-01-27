from .generator import Generator

class Headers:
	def __init__(self, deviceId: str = None, sid: str = None):
		self.deviceId = deviceId
		self.sid=sid
		self.device = Generator().getDeviceId()
		self.User_Agent = self.device["user_agent"]

	def iphone_headers(self, data = None, content_type = None):

		headers = {
			"NDCDEVICEID": self.deviceId if self.deviceId is not None else self.device["device_id"],
			"NDCLANG": "ru",
			"Accept-Language": "ru-RU",
			"SMDEVICEID": "20230109055041eecd2b9dd8439235afe4522cb5dacd26011dba6bbfeeb752", 
			"User-Agent": self.User_Agent,
			"Content-Type": "application/json; charset=utf-8",
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Upgrade"
			}


		if data is not None:
			headers["Content-Length"] = str(len(data))
			headers["NDC-MSG-SIG"] = Generator().signature(data=data)

		if self.sid is not None:headers["NDCAUTH"] = f"sid={self.sid}"

		if content_type is not None:headers["Content-Type"] = content_type

		return headers



	def iphoneWeb_headers(self):
		return None