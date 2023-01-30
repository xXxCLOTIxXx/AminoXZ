from time import time as timestamp
import json

from .lib.util.generator import Generator

from .lib.util import exceptions, objects

from .lib.util.headers import Headers

from .socket import Callbacks, SocketHandler

import requests
from typing import BinaryIO
from threading import Thread

generator = Generator()

class Client(Callbacks, SocketHandler):
	def __init__(self, deviceId: str=None, proxies: dict = None, sock_trace: bool = False, sock_debug: bool = False, socket_enabled: bool = True, autoDevice: bool = False, certificatePath = None):
		self.proxies=proxies
		self.session = requests.Session()
		self.api = "https://service.narvii.com/api/v1"
		self.web_api = "https://aminoapps.com/api"
		self.certificatePath = certificatePath

		self.device = generator.getDeviceId()

		self.socket_enabled = socket_enabled
		self.autoDevice = autoDevice
		SocketHandler.__init__(self, self, sock_trace=sock_trace, debug=sock_debug)
		Callbacks.__init__(self, self)

		self.uid = None
		self.sid = None
		self.auth = False
		self.profile = objects.UserProfile
		self.deviceId = deviceId if deviceId is not None else self.device["device_id"]


	def parse_headers(self, data = None, content_type = None, type: str = 'iphone'):
		headers = Headers(deviceId=self.deviceId, sid=self.sid)
		if type == 'iphone':return headers.iphone_headers(data, content_type)
		elif type == 'android':return headers.android_headers(data, content_type)
		else: raise exceptions.WrongType(fileType)


	def upload_media(self, file: BinaryIO, fileType: str):

		if fileType == "audio":
			t = "audio/aac"
		elif fileType == "image":
			t = "image/jpg"
		else: raise exceptions.WrongType(fileType)

		data = file.read()
		response = self.session.post(f"{self.api}/g/s/media/upload", data=data, headers=headers.Headers(type=t, data=data, deviceId=self.device_id).headers, proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.CheckException(json.loads(response.text))
		else: return json.loads(response.text)["mediaValue"]


	def Online(self):
		#don't work
		Thread(target=self._online_loop).start()

	def login(self, password: str, email: str = None, number: str = None, sid: str = None, secret: str = None):

		if email:
			data = json.dumps({
				"email": email,
				"v": 2,
				"secret": f"0 {password}" if secret is None else secret,
				"deviceID": self.deviceId,
				"clientType": 100,
				"action": "normal",
				"timestamp": int(timestamp() * 1000)
			})
			with self.session.post(f"{self.api}/g/s/auth/login", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath) as response:
				if response.status_code != 200: exceptions.checkExceptions(response.text)
				else:json_response = json.loads(response.text)
			self.sid = json_response["sid"]
			self.uid = json_response["account"]["uid"]
			self.auth = True
			self.profile = objects.UserProfile(json_response["userProfile"])
			self.profile.sid = self.sid
			if self.socket_enabled:
				self.run_amino_socket()
			return self.uid

		elif number:

			data = json.dumps({
				"phoneNumber": number,
				"v": 2,
				"secret": f"0 {password}",
				"deviceID": self.deviceId,
				"clientType": 100,
				"action": "normal",
				"timestamp": int(timestamp() * 1000)
			})

			response = self.session.post(f"{self.api}/g/s/auth/login", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath)
			if response.status_code != 200: return exceptions.checkExceptions(response.text)
			else: json_response = json.loads(response.text)
			self.sid = self.json_response["sid"]
			self.uid = self.json_response["account"]["uid"]
			self.auth = True
			self.profile = objects.UserProfile(json_response["userProfile"])
			self.profile.sid = self.sid
			if self.socket_enabled:
				self.run_amino_socket()
			return self.uid
		elif sid:

			uId = generator.sid_to_uid(sid)
			self.authenticated = True
			self.sid = sid
			self.uid = uId
			self.auth = True
			self.profile = objects.UserProfile(json_response["userProfile"])
			self.profile.sid = self.sid
			if self.socket_enabled:
				self.run_amino_socket()

		else:exceptions.checkExceptions(response.text)



	def logout(self):

		data = json.dumps({
		"deviceID": self.deviceId,
		"clientType": 100,
		"timestamp": int(timestamp() * 1000)
		})
		response = self.session.post(f"{self.api}/g/s/auth/logout", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200:exceptions.checkExceptions(response.text)
		else:
			self.sid = None
			self.uid = None
			self.auth = False
			self.profile = None
			if self.socket_enabled:
				self.close()
		return response.status_code


	def register(self, nickname: str, email: str, password: str, verificationCode: str, deviceId: str):

		data = json.dumps({
			"secret": f"0 {password}",
			"deviceID": deviceId,
			"email": email,
			"clientType": 100,
			"nickname": nickname,
			"latitude": 0,
			"longitude": 0,
			"address": None,
			"clientCallbackURL": "narviiapp://relogin",
			"validationContext": {
				"data": {"code": verificationCode},
				"type": 1,
				"identity": email
			},
			"type": 1,
			"identity": email,
			"timestamp": int(timestamp() * 1000)
		})

		response = self.session.post(f"{self.api}/g/s/auth/register", data=data, headers=self.parse_headers(data=data), proxies=self.proxies, verify=self.certificatePath)
		return exceptions.checkExceptions(response.text) if response.status_code != 200 else response.status_code



	def request_verify_code(self, email: str, resetPassword: bool = False):
		
		data = {
			"identity": email,
			"type": 1,
			"deviceID": self.deviceId
		}

		if resetPassword is True:
			data["level"] = 2
			data["purpose"] = "reset-password"

		data = json.dumps(data)
		response = self.session.post(f"{self.api}/g/s/auth/request-security-validation", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath)
		return exceptions.checkExceptions(response.text) if response.status_code != 200 else response.status_code





	def get_my_communities(self, start: int = 0, size: int = 10):

		if not self.auth: exceptions.checkExceptions(local={'code': 1, 'text': 'You are not logged in.'})
		response = self.session.get(f"{self.api}/g/s/community/joined?v=1&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.CheckException(response.text)
		else: return objects.CommunityList(json.loads(response.text)["communityList"])


	def get_account_info(self):

		if not self.auth: exceptions.checkExceptions(local={'code': 1, 'text': 'You are not logged in.'})
		response = self.session.get(f"{self.api}/g/s/account", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.UserProfile(json.loads(response.text)["account"]).UserProfile


	def get_sid_info(self, sid: str):
		
		return {"sid": self.sid, "uid": self.uid, "ip_by_sid": generator.sid_to_ip_address(self.sid), "created_time": generator.sid_created_time(self.sid), "client_type": generator.sid_to_client_type(self.sid)}

	def get_from_deviceid(self, deviceId: str):

		response = self.session.get(f"{self.api}/g/s/auid?deviceId={deviceId}")
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return json.loads(response.text)["auid"]

	def get_from_link(self, link: str):

		response = self.session.get(f"{self.api}/g/s/link-resolution?q={link}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.FromCode(json.loads(response.text)["linkInfoV2"]).FromCode

	def get_from_id(self, objectId: str, objectType: int, comId: str = None):

		data = json.dumps({
			"objectId": objectId,
			"targetCode": 1,
			"objectType": objectType,
			"timestamp": int(timestamp() * 1000)
		})

		if comId: response = self.session.post(f"{self.api}/g/s-x{comId}/link-resolution", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath)
		else: response = self.session.post(f"{self.api}/g/s/link-resolution", headers=self.parse_headers(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.FromCode(json.loads(response.text)["linkInfoV2"]).FromCode


	def auto_capcha(self, image_link: str):

		data = json.dumps({'link': image_link})
		response = self.session.post(f'https://amino-tools.herokuapp.com/getCapcha-apiV1', data=data).json()
		if response['api-code'] != 200:raise exceptions.CapchaNotRecognize(response)
		else: return response


	def join_community(self, comId: str, invitationId: str = None):
		data = {"timestamp": int(timestamp() * 1000)}
		if invitationId: data["invitationId"] = invitationId

		data = json.dumps(data)
		response = self.session.post(f"{self.api}/x{comId}/s/community/join", data=data, headers=self.parse_headers(data=data), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: response.status_code