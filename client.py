from time import time as timestamp
import json
from .lib.util.generator import Generator
from .lib.util import exceptions, helpers, headers
import requests
from typing import BinaryIO


"""
	Made by Xsarz (@DXsarz)
	GitHub: https://github.com/xXxCLOTIxXx
	Telegram channel: https://t.me/DxsarzUnion
	YouTube: https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q]

"""



class Client():
	def __init__(self, deviceId: str=None, proxies: dict = None):
		requests.Session()
		self.sid = None
		self.proxies=proxies
		self.session = requests.Session()
		self.api = "https://service.narvii.com/api/v1"
		self.web_api = "https://aminoapps.com/api"
		self.uid = None
		self.device = Generator().deviceId()
		self.User_Agent = self.device["user_agent"]
		if deviceId!=None:self.device_id = deviceId
		else:self.device_id = self.device["device_id"]

	def parser(self, header_type: str = "app", data = None, content_type: str = None, referer: str = None):
		if header_type == 'app':return headers.headers(data=data, content_type=content_type, deviceId=self.device_id, sid=self.sid).headers
		elif header_type == 'web':return headers.web_headers(referer=referer, sid=self.sid).headers
		else:return headers.headers(data=data, content_type=content_type, deviceId=self.device_id, sid=self.sid).headers


	def upload_media(self, file: BinaryIO, fileType: str):
		"""
		Not tested

		Upload file to the amino servers

		** options **

		- *file* : upload file
		- *fileType*: type of file
		"""
		if fileType == "audio":t = "audio/aac"
		elif fileType == "image":t = "image/jpg"
		else: raise exceptions.SpecifyType(fileType)
		data = file.read()
		response = self.session.post(f"{self.api}/g/s/media/upload", data=data, headers=headers(data=data), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else:return json.loads(response.text)["mediaValue"]


	def login_phone(number: str, password: str):

		"""
		Login with phone number

		** options **
		- *number* : Phone number
		- *password* : Password


		"""

		data = json.dumps({
			"phoneNumber": number,
			"v": 2,
			"secret": f"0 {password}",
			"deviceID": self.device_id,
			"clientType": 100,
			"action": "normal",
			"timestamp": int(timestamp() * 1000)
		})

		response = self.session.post(f"{self.api}/g/s/auth/login", headers=self.parser(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: json_response = json.loads(response.text)
		self.sid = self.json_response["sid"]
		self.uid = self.json_response["account"]["uid"]
		return self.uid


	def sid_login(self, sid: str):
		"""

		Sign in with sid

		** options **
		- *sid* : sid of the account

		"""
		self.sid = sid
		self.uid = helpers.sid_to_uid(self.sid)
		return self.uid




	def login(self, email: str, password: str):
		"""
		Account login 

		** options **

		- *email*: email
		- *password*: password

		"""


		data = json.dumps({
			"email": email,
			"v": 2,
			"secret": f"0 {password}",
			"deviceID": self.device_id,
			"clientType": 100,
			"action": "normal",
			"timestamp": int(timestamp() * 1000)
		})
		with self.session.post(f"{self.api}/g/s/auth/login", headers=self.parser(data=data), data=data, proxies=self.proxies) as response:
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else:json_response = json.loads(response.text)
		self.sid = json_response["sid"]
		self.uid = json_response["account"]["uid"]
		return self.uid

	def logout(self):
		"""
		Logout from account
		"""
		data = json.dumps({
		"deviceID": self.device_id,
		"clientType": 100,
		"timestamp": int(timestamp() * 1000)
		})
		response = self.session.post(f"{self.api}/g/s/auth/logout", headers=self.parser(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200:return exceptions.CheckException(json.loads(response.text))
		else:
			self.sid = None
			self.uid = None
		return response.status_code




	def register_account(self, name: str, email: str, password: str, сode: str, deviceId: str = None):
		"""
		Register account.

		** options **
		- *name* : name of the account
		- *email* : email of the account
		- *password* : password of the account
		- *сode* : confirmation code
		- *deviceId* : device for account (you can not write)

		"""

		if deviceId==None: deviceId = self.device_id
		data = json.dumps({
			"secret": f"0 {password}",
			"deviceID": deviceId,
			"email": email,
			"clientType": 100,
			"nickname": name,
			"latitude": 0,
			"longitude": 0,
			"address": None,
			"clientCallbackURL": "narviiapp://relogin",
			"validationContext": {
				"data": {
						"code": сode
						},
				"type": 1,
				"identity": email
				},
				"type": 1,
				"identity": email,
				"timestamp": int(timestamp() * 1000)
				})        

		response = self.session.post(f"{self.api}/g/s/auth/register", data=data, headers=self.parser(data=data), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)

	def request_verify_code(self, email: str, resetPassword: bool = False, timeout: int = None):
		"""

		Request an verification code

		** options **
		- *email* : email
		- *resetPassword * : if code should be for password reset

		"""
		data = {"identity": email,"type": 1,"deviceID": self.device_id}
		if resetPassword is True:
			data["level"] = 2
			data["purpose"] = "reset-password"

		data = json.dumps(data)
		response = self.session.post(f"{self.api}/g/s/auth/request-security-validation", headers=self.parser(data=data), data=data, timeout=timeout, proxies=self.proxies)
		if response.status_code != 200:return exceptions.checkExceptions(json.loads(response.text))
		else:return response.status_code


	def get_account_info(self):
		"""

		Get account info

		"""

		response = self.session.get(f"{self.api}/g/s/account", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: information_from_the_server = json.loads(response.text)["account"]


		info = {
			"sid": self.sid,
			"uid": self.uid,
			"ip_by_sid": helpers.sid_to_ip_address(self.sid),
			"created_time": helpers.sid_to_created_time(self.sid),
			"client_type": helpers.sid_to_client_type(self.sid),
			"other": information_from_the_server

		}
		return info


	def get_from_link(self, link: str):
		"""
		Get the information from the Amino URL.
		** options **
		- *link* : link.

		"""
		response = self.session.get(f"{self.api}/g/s/link-resolution?q={link}", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["linkInfoV2"]


	def change_global_profile(self, name: str = None, content: str = None, icon: BinaryIO = None, backgroundColor: str = None, backgroundImage: str = None, bubbleId: str = None):

		"""
		change global account's profile

		** options **
		- *name* : Profile name
		- *content* : Bio of the Profile.
		- *icon* : Profile icon
		- *backgroundImage* : Url of the background picture
		- *backgroundColor* : Hexadecimal background color
		- *bubbleId* : Bubble ID.

		"""
		data = {
			"address": None,
			"latitude": 0,
			"longitude": 0,
			"mediaList": None,
			"eventSource": "UserProfileView",
			"timestamp": int(timestamp() * 1000)
		}

		if name!=None: data["nickname"] = name
		if icon!=None: data["icon"] = self.upload_media(icon, "image")
		if content!=None: data["content"] = content
		if backgroundColor!=None: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
		if backgroundImage!=None: data["extensions"] = {"style": {"backgroundMediaList": [[100, backgroundImage, None, None, None]]}}
		if bubbleId!=None: data["extensions"] = {"defaultBubbleId": bubbleId}

		data = json.dumps(data)
		response = self.session.post(f"{self.api}/g/s/user-profile/{self.uid}", headers=self.parser(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else:return response.status_code


	def change_profile(self, comId: str, name: str = None, content: str = None):

		"""
		change account's in community profile

		** options **

		- *name* : Profile name
		- *content* : Bio of the Profile.
		"""

		data = {"timestamp": int(timestamp() * 1000)}
		if name!=None: data["nickname"] = name
		if content!=None: data["content"] = content
		data = json.dumps(data)
		response = self.session.post(f"{self.api}/x{comId}/s/user-profile/{self.uid}", headers=self.parser(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else:return response.status_code








	"""

		█▀▀ █░█ ▄▀█ ▀█▀   █▀▀ █░█ █▄░█ █▀▀ ▀█▀ █ █▀█ █▄░█ █▀
		█▄▄ █▀█ █▀█ ░█░   █▀░ █▄█ █░▀█ █▄▄ ░█░ █ █▄█ █░▀█ ▄█

	"""


	def send_message_web(self, chatId: str, comId: str, message: str, messageType: int = 0):

		"""

		Send message via the web


		** options **

		*chatId*: Chat ID
		*message*: message to send
		*messageType*: message type (normal - 0)
		*comId*: community id (if the chat is in a community)

		"""


		data = {
			"ndcId": f"x{comId}",
			"threadId": chatId,
			"message": {
				"content": message,
				"mediaType": 0,
				"type": messageType,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		data = json.dumps(data)
		response = self.session.post(f"https://aminoapps.com/api/add-chat-message",headers=self.parser(referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={comId}", header_type='web'),data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code	



	def join_chat_web(self, chatId: str, comId: str):


		"""

		enter chat via web

		** options **

		-*comId*: Community id
		- *chatId*: Chat Id

		"""


		data = {
			"ndcId": f"x{comId}",
			"threadId": chatId
		}
		data = json.dumps(data)
		response = self.session.post(f"https://aminoapps.com/api/join-thread", headers=self.parser(referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={comId}", header_type='web'), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code


	def leave_chat_web(self, chatId: str, comId: str):


		"""

		leave chat via web

		** options **

		-*comId*: Community id
		- *chatId*: Chat Id

		"""

		data = {
			"ndcId": f"x{comId}",
			"threadId": chatId
		}
		data = json.dumps(data)
		response = self.session.post(f"https://aminoapps.com/api/leave-thread", headers=self.parser(referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={comId}", header_type='web'), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code


	def join_chat(self, chatId: str, comId: str = None):
		"""
		Join chat

		** options **
		- *chatId* : Chat id
		- *comId*: community id (if the chat is in a community)

		"""
		if comId!=None:
			response = self.session.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member/{self.uid}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return response.status_code


		response = self.session.post(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.uid}", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: response.status_code

	def leave_chat(self, chatId: str, comId: str = None):
		"""
		Leave chat

		** options **
		- **chatId** : Chat id
		- *comId*: community id (if the chat is in a community)

		"""
		if comId!=None:
			response = self.session.delete(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member/{self.uid}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return response.status_code

		response = self.session.delete(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.uid}", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code






	def get_my_chats(self, start: int = 0, size: int = 25, comId: str = None):

		"""

		Get chats on account


		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.
		-*comId*: Community id (if you want to get a list of chats from a community, otherwise you will get a list of chats in the global amino menu)


		"""
		if comId!=None:
			response = self.session.get(f"{self.api}/x{comId}/s/chat/thread?type=joined-me&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["threadList"]
		else:
			response = self.session.get(f"{self.api}/g/s/chat/thread?type=joined-me&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["threadList"]


	def get_chat_thread(self, chatId: str, start: int = 0, size: int = 25, comId: str = None):
		"""

		Get the Chat Object


		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.
		-*comId*: Community id (if the chat is in a community)
		- *chatId*: Chat Id

		"""

		if comId!=None:
			response = self.session.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["thread"]
		else:
			response = self.session.get(f"{self.api}/g/s/chat/thread/{chatId}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["thread"]

	def get_chat_messages(self, chatId: str, start: int = 0, size: int = 25, comId: str = None):

		"""

		Get the Chat messages


		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.
		-*comId*: Community id (if the chat is in a community)
		- *chatId*: Chat Id

		"""
		if comId!=None:
			response = self.session.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)['messageList']
		else:
			response = self.session.get(f"{self.api}/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)['messageList']

	def get_public_chat_threads(self, comId: str, type: str = "recommended", start: int = 0, size: int = 25):
		"""

		Get public chats


		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.
		-*comId*: Community id (if the chat is in a community)

		"""
		response = self.session.get(f"{self.api}/x{comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}", headers=self.parser())
		if response.status_code != 200: raise Exception(json.loads(response.text))
		else: return json.loads(response.text)["threadList"]



	def get_chat_members(self, chatId: str, comId: str, start: int = 0, size: int = 25):
		"""
		Get chat members
		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.
		- *chatId* : chat id
		- *comId*: community id
		"""


		if comId !=None:
			response = self.session.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["memberList"]	

		response = self.session.get(f"{self.api}/g/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["memberList"]




	def get_community_members(self, comId: str,  type: str = "recent", start: int = 0, size: int = 25):

		"""
		Get chat members
		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.
		- *comId*: community id (if chat in community)
		- *type*: type of participants 
		
		=-types-=
		recent - recent members
		online - online users 
		banned - banned users
		featured - featured members
		leaders - leaders
		curators - curators

		"""
		if type == "recent": response = self.session.get(f"{self.api}/x{comId}/s/user-profile?type=recent&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
		elif type == 'online': response = self.session.get(f"{self.api}/x{comId}/s/live-layer?topic=ndtopic:x{comId}:online-members&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
		elif type == "banned": response = self.session.get(f"{self.api}/x{comId}/s/user-profile?type=banned&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
		elif type == "featured": response = self.session.get(f"{self.api}/x{comId}/s/user-profile?type=featured&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
		elif type == "leaders": response = self.session.get(f"{self.api}/x{comId}/s/user-profile?type=leaders&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
		elif type == "curators": response = self.session.get(f"{self.api}/x{comId}/s/user-profile?type=curators&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)


	def get_message_info(self, chatId: str, messageId: str): #do
		"""
		Message Information
		** options **

		- **chatId** : Chat id
		- **messageId** : Message id

		"""
		response = self.session.get(f"{self.api}/g/s/chat/thread/{chatId}/message/{messageId}", headers=self.parser(data=data), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["message"]




	"""
				█▀▀ █▀█ █▀▄▀█ █▀▄▀█ █░█ █▄░█ █ ▀█▀ █▄█   █▀▀ █░█ █▄░█ █▀▀ ▀█▀ █ █▀█ █▄░█ █▀
				█▄▄ █▄█ █░▀░█ █░▀░█ █▄█ █░▀█ █ ░█░ ░█░   █▀░ █▄█ █░▀█ █▄▄ ░█░ █ █▄█ █░▀█ ▄█

	"""


	def get_community_info(self, comId: str):
		"""
		Community information

		** options **
		- *comId* : Community id
		"""

		response = self.session.get(f"{self.api}/g/s-x{comId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["community"]

	def get_my_communities(self, start: int = 0, size: int = 25):

		"""

		Get communities on account


		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.

		"""
		response = self.session.get(f"{self.api}/g/s/community/joined?v=1&start={start}&size={size}", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["communityList"]

	def join_community(self, comId):


		"""

		join the community

		** options **
		-*comId*: Community id

		"""

		data = json.dumps({"timestamp": int(timestamp() * 1000)})
		response = self.session.post(f"{self.api}/x{comId}/s/community/join", headers=self.parser(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code





	#user functions



	def get_user_info(self, userId: str, comId: str = None):
		"""
		get user information


		** options **

		- *userId* : user id
		- *comId*: community id (if you want to get a profile from a community)

		"""
		if comId!=None:
			response = self.session.get(f"{self.api}/x{comId}/s/user-profile/{userId}", headers=self.parser(), proxies=self.proxies)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["userProfile"]

		response = self.session.get(f"{self.api}/g/s/user-profile/{userId}", headers=self.parser(), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["userProfile"]




	"""

				█░█░█ █ █▄▀ █   ▄▀█ █▄░█ █▀▄   █▄▄ █░░ █▀█ █▀▀   █▀█ █▀█ █▀ ▀█▀ █▀
				▀▄▀▄▀ █ █░█ █   █▀█ █░▀█ █▄▀   █▄█ █▄▄ █▄█ █▄█   █▀▀ █▄█ ▄█ ░█░ ▄█
	"""

	def post_wiki(self, comId: str, title: str, content: str, icon: str = None, imageList: list = None, keywords: str = None, backgroundColor: str = None, fansOnly: bool = False):
		mediaList = []
		if imageList!=None:
			for image in imageList:
				mediaList.append([100, self.upload_media(image, "image"), None])

		data = {
			"label": title,
			"content": content,
			"mediaList": mediaList,
			"eventSource": "GlobalComposeMenu",
			"timestamp": int(timestamp() * 1000)
		}

		if icon: data["icon"] = icon
		if keywords: data["keywords"] = keywords
		if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
		if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
		data = json.dumps(data)

		response = self.session.post(f"{self.api}/x{comId}/s/item", headers=self.parser(data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code