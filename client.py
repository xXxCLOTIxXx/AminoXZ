from time import time as timestamp
from time import sleep
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

		self.sid = None
		self.auth = False
		self.profile = objects.UserProfile
		self.deviceId = deviceId if deviceId is not None else self.device["device_id"]

	def set_proxy(self, proxy):
		if type(proxy) == dict:self.proxies = proxy
		elif type(proxy) == str:
			self.proxies = {
				"http": proxy,
				"https": proxy
			}
		else:
			raise WrongType(type(proxy))


	def parse_headers(self, data = None, content_type = None, type: str = 'iphone', referer: str = None):
		headers = Headers(deviceId=self.deviceId, sid=self.sid)
		if type == 'iphone':return headers.iphone_headers(data, content_type)
		elif type == 'android':return headers.android_headers(data, content_type)
		elif type == 'web':return headers.web_headers(referer=referer)
		elif type == 'ios_web':return headers.iphoneWeb_headers()
		else: raise exceptions.WrongType(fileType)


	def join_voice_chat(self, comId: str, chatId: str, joinType: int = 1):


		data = {
			"o": {
				"ndcId": int(comId),
				"threadId": chatId,
				"joinRole": joinType,
				"id": "2154531"
			},
			"t": 112
		}
		data = json.dumps(data)
		self.send(data)

	def join_video_chat(self, comId: str, chatId: str, joinType: int = 1):

		data = {
			"o": {
				"ndcId": int(comId),
				"threadId": chatId,
				"joinRole": joinType,
				"channelType": 5,
				"id": "2154531"
			},
			"t": 108
		}
		data = json.dumps(data)
		self.send(data)

	def join_video_chat_as_viewer(self, comId: str, chatId: str):
		data = {
			"o":
				{
					"ndcId": int(comId),
					"threadId": chatId,
					"joinRole": 2,
					"id": "72446"
				},
			"t": 112
		}
		data = json.dumps(data)
		self.send(data)

	def run_vc(self, comId: str, chatId: str, joinType: str):
		while self.active:
			data = {
				"o": {
					"ndcId": comId,
					"threadId": chatId,
					"joinRole": joinType,
					"id": "2154531"
				},
				"t": 112
			}
			data = json.dumps(data)
			self.send(data)
			sleep(1)

	def start_vc(self, comId: str, chatId: str, joinType: int = 1):

		data = {
			"o": {
				"ndcId": comId,
				"threadId": chatId,
				"joinRole": joinType,
				"id": "2154531"
			},
			"t": 112
		}
		data = json.dumps(data)
		self.send(data)

		data = {
			"o": {
				"ndcId": comId,
				"threadId": chatId,
				"channelType": 1,
				"id": "2154531"
			},
			"t": 108
		}
		data = json.dumps(data)
		self.send(data)
		self.active = True
		threading.Thread(target=self.run_vc, args=[comId, chatId, joinType])

	def end_vc(self, comId: str, chatId: str, joinType: int = 2):

		self.active = False
		data = {
			"o": {
				"ndcId": comId,
				"threadId": chatId,
				"joinRole": joinType,
				"id": "2154531"
				},
			"t": 112
		}
		data = json.dumps(data)
		self.send(data)

	def start_video(self, comId: str, chatId: str, path: str, title: str, background: BinaryIO, duration: int):

		data = {
			"o": {
				"ndcId": int(comId),
				"threadId": chatId,
				"joinRole": 1,
				"id": "10335106"
			},
			"t": 112
		}
		self.send(data)
		data = {
			"o": {
				"ndcId": int(comId),
				"threadId": chatId,
				"channelType": 5,
				"id": "10335436"
			},
			"t": 108
		}
		self.send(data)
		data = {
			"o": {
				"ndcId": int(comId),
				"threadId": chatId,
				"playlist": {
					"currentItemIndex": 0,
					"currentItemStatus": 1,
					"items": [{
						"author": None,
						"duration": duration,
						"isDone": False,
						"mediaList": [[100, self.upload_media(background, "image"), None]],
						"title": title,
						"type": 1,
						"url": f"file://{path}"
					}]
				},
				"id": "3423239"
			},
			"t": 120
		}
		self.send(data)
		sleep(2)
		data["o"]["playlist"]["currentItemStatus"] = 2
		data["o"]["playlist"]["items"][0]["isDone"] = True
		self.send(data)




	def upload_media(self, file: BinaryIO, fileType: str):
		
		if fileType == "audio":
			t = "audio/aac"
		elif fileType == "image":
			t = "image/jpg"
		else: raise exceptions.WrongType(fileType)

		data = file.read()
		response = self.session.post(f"{self.api}/g/s/media/upload", data=data, headers=self.parse_headers(data=data, content_type=t), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return json.loads(response.text)["mediaValue"]

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
			self.auth = True
			self.profile = objects.UserProfile(json_response["userProfile"]).UserProfile
			self.profile.sid = self.sid
			if self.socket_enabled:
				self.run_amino_socket()
			return self.profile.userId

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
			self.auth = True
			self.profile = objects.UserProfile(json_response["userProfile"]).UserProfile
			self.profile.sid = self.sid
			if self.socket_enabled:
				self.run_amino_socket()
			return self.profile.userId
		elif sid:

			uId = generator.sid_to_uid(sid)
			self.authenticated = True
			self.sid = sid
			self.auth = True
			self.profile = objects.UserProfile({'uid': uId}).UserProfile
			self.profile.sid = self.sid
			if self.socket_enabled:
				self.run_amino_socket()
			return uId

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
		
		return {"sid": self.sid, "uid": self.profile.userId, "ip_by_sid": generator.sid_to_ip_address(self.sid), "created_time": generator.sid_created_time(self.sid), "client_type": generator.sid_to_client_type(self.sid)}

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

		data = {"url": image_link}
		response = self.session.post("https://captcha-solver-iukzq.run-eu-central1.goorm.app/predict", json=data)
		if response.status_code != 200:raise exceptions.CapchaNotRecognize(response)
		else: return response.json()


	def join_community(self, comId: str, invitationId: str = None):
		data = {"timestamp": int(timestamp() * 1000)}
		if invitationId: data["invitationId"] = invitationId

		data = json.dumps(data)
		response = self.session.post(f"{self.api}/x{comId}/s/community/join", data=data, headers=self.parse_headers(data=data), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: response.status_code

	def leave_community(self, comId: str):
		data = json.dumps ({"timestamp": int(timestamp() * 1000)})

		response = self.session.post(f"{self.api}/x{comId}/s/community/leave", data=data, headers=self.parse_headers(data=data), proxies=self.proxies, verify=self.certificatePath)
		return exceptions.checkExceptions(json.loads(response.text)) if response.status_code != 200 else response.status_code


	def get_all_users(self, start: int = 0, size: int = 25):

		response = self.session.get(f"{self.api}/g/s/user-profile?type=recent&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else:return objects.UserProfileCountList(json.loads(response.text)).UserProfileCountList



	def get_public_communities(self, language: str = "en", size: int = 25):

		response = requests.get(f"{self.api}/g/s/topic/0/feed/community?language={language}&type=web-explore&categoryKey=recommendation&size={size}&pagingType=t", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else:return objects.CommunityList(json.loads(response.text)["communityList"]).CommunityList

	def get_community_info(self, comId: str):

		response = self.session.get(f"{self.api}/g/s-x{comId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.Community(json.loads(response.text)["community"]).Community