from time import time as timestamp
import json

from .lib.util.generator import Generator

from .lib.util import exceptions, objects

from .lib.util.headers import headers, web_headers

from .socket import Callbacks, SocketHandler

import requests
from typing import BinaryIO, Union

generator = Generator()

class Client(Callbacks, SocketHandler):
	def __init__(self, deviceId: str=None, proxies: dict = None, sock_trace: bool = False, sock_debug: bool = False, socket_enabled: bool = True, autoDevice: bool = False):
		self.proxies=proxies
		self.session = requests.Session()
		self.api = "https://service.narvii.com/api/v1"
		self.web_api = "https://aminoapps.com/api"

		self.device = generator.getDeviceId()

		self.socket_enabled = socket_enabled
		self.autoDevice = autoDevice
		SocketHandler.__init__(self, self, sock_trace=sock_trace, debug=sock_debug)
		Callbacks.__init__(self, self)

		self.uid = None
		self.sid = None
		self.auth = False
		self.profile = objects.UserProfile

		if deviceId!=None:self.deviceId = deviceId
		else:self.deviceId = self.device["device_id"]


	def login(self, password: str, email: str = None, number: str = None, sid: str = None, secret: str = None):
		"""
		Account login 

		** options **

		- *email*: email
		- *password*: password
		- *number* : Phone number
		- * sid *: sid of the account
		- * secret *: secret of the account

		use or email or number or sid or secret

		"""
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
			with self.session.post(f"{self.api}/g/s/auth/login", headers=headers(data=data, deviceId=self.deviceId, sid=self.sid), data=data, proxies=self.proxies) as response:
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

			response = self.session.post(f"{self.api}/g/s/auth/login", headers=headers(data=data, deviceId=self.deviceId, sid=self.sid), data=data, proxies=self.proxies)
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

		else:exceptions.checkExceptions(local={'code': 1, 'text': 'Incorrect login type.'})



	def logout(self):
		"""

		Logout from account.

		"""
		data = json.dumps({
		"deviceID": self.deviceId,
		"clientType": 100,
		"timestamp": int(timestamp() * 1000)
		})
		response = self.session.post(f"{self.api}/g/s/auth/logout", headers=headers(data=data, deviceId=self.deviceId, sid=self.sid), data=data, proxies=self.proxies)
		if response.status_code != 200:exceptions.CheckException(response.text)
		else:
			self.sid = None
			self.uid = None
			self.auth = False
			self.profile = None
			if self.socket_enabled:
				self.close()
		return response.status_code


	def get_my_communities(self, start: int = 0, size: int = 10):
		"""
		List of Communities in the account.

		** options **
			- *start* : Where to start the list
			- *size* : Size of the list
		"""

		if not self.auth: exceptions.checkExceptions(local={'code': 1, 'text': 'You are not logged in.'})
		response = self.session.get(f"{self.api}/g/s/community/joined?v=1&start={start}&size={size}", headers=headers(deviceId=self.deviceId, sid=self.sid), proxies=self.proxies)
		if response.status_code != 200: return exceptions.CheckException(response.text)
		else: return objects.CommunityList(json.loads(response.text)["communityList"])




	def get_account_info(self):
		"""
		Get info about account
		"""
		if not self.auth: exceptions.checkExceptions(local={'code': 1, 'text': 'You are not logged in.'})
		response = self.session.get(f"{self.api}/g/s/account", headers=headers(deviceId=self.deviceId, sid=self.sid), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: information_from_the_server = json.loads(response.text)["account"]
		return objects.UserProfile({"sid": self.sid, "uid": self.uid, "ip_by_sid": generator.sid_to_ip_address(self.sid), "created_time": generator.sid_created_time(self.sid), "client_type": generator.sid_to_client_type(self.sid), "other": information_from_the_server})


	def get_from_deviceid(self, deviceId: str):
		"""
		Get the User id from device id

		** options **
			- ** deviceID ** : device id
		"""
		response = self.session.get(f"{self.api}/g/s/auid?deviceId={deviceId}")
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return json.loads(response.text)["auid"]

	def get_from_link(self, link: str):
		"""
		Get the Object Information from the Amino URL
		** options **
			- * code * : amino link
				= example = : https://aminoapps.com/p/zalupa/hui

		"""
		response = self.session.get(f"{self.api}/g/s/link-resolution?q={link}", headers=headers(deviceId=self.deviceId, sid=self.sid), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.FromCode(json.loads(response.text)["linkInfoV2"]).FromCode

	def get_from_id(self, objectId: str, objectType: int, comId: str = None):
		"""
		Get the Object Information from the Object ID and Type.
		** options **
			- * objectId * : user Id, Blog Id, etc.
			- * objectType * : Type of the Object.
			- * comId * : ID of the Community. Use if the Object is in a Community.

		"""
		data = json.dumps({
			"objectId": objectId,
			"targetCode": 1,
			"objectType": objectType,
			"timestamp": int(timestamp() * 1000)
		})

		if comId: response = self.session.post(f"{self.api}/g/s-x{comId}/link-resolution", headers=headers(deviceId=self.deviceId, sid=self.sid), data=data, proxies=self.proxies)
		else: response = self.session.post(f"{self.api}/g/s/link-resolution", headers=self.parse_headers(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.FromCode(json.loads(response.text)["linkInfoV2"]).FromCode


	def auto_capcha(self, image_link: str):
		data = json.dumps({'link': image_link})
		response = self.session.post(f'https://amino-tools.herokuapp.com/getCapcha-apiV1', data=data).json()
		if response['api-code'] != 200:raise exceptions.CapchaNotRecognize(response)
		else: return response