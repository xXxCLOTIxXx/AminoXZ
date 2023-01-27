from .generator import Generator


def headers(data = None, content_type = None, deviceId: str = None, sid: str = None):

	device = Generator().getDeviceId()
	User_Agent = device["user_agent"]
	if deviceId is None:deviceId = device["device_id"]


	headers = {
		"NDCDEVICEID": deviceId,
		"NDCLANG": "ru",
		"Accept-Language": "ru-RU",
		"SMDEVICEID": "20230109055041eecd2b9dd8439235afe4522cb5dacd26011dba6bbfeeb752", 
		"User-Agent": User_Agent,
		"Content-Type": "application/json; charset=utf-8",
		"Host": "service.narvii.com",
		"Accept-Encoding": "gzip",
		"Connection": "Upgrade"
		}


	if data is not None:
		headers["Content-Length"] = str(len(data))
		headers["NDC-MSG-SIG"] = Generator().signature(data=data)

	if sid is not None:headers["NDCAUTH"] = f"sid={sid}"

	if content_type is not None:headers["Content-Type"] = content_type

	return headers



def web_headers():
	return None