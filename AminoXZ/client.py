from time import time as timestamp
import json
from .lib.util import generator as gen
from .lib.util import exceptions
import requests

"""
	Made by Xsarz (@DXsarz)
	GitHub: https://github.com/xXxCLOTIxXx
	Telegram channel: https://t.me/DxsarzUnion
	YouTube: https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q]

"""



class Client():
	def __init__(self):
		requests.Session()
		self.logged = False
		self.sid = None
		self.session = requests.Session()
		self.community_id = None
		self.api = "https://service.narvii.com/api/v1"
		self.web_api = "https://aminoapps.com/api"
		self.uid = None
		self.generator = gen.Generator()
		self.device = self.generator.deviceId()
		self.User_Agent = self.device["user_agent"]
		self.device_id = self.device["device_id"]

	def headers(self, data=None, content_type=None):
		headers = {
			"NDCDEVICEID": self.device_id,
			"Accept-Language": "ru-RU",
			"Content-Type": "application/json; charset=utf-8",
			"User-Agent": self.User_Agent,
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Upgrade"
		}

		if data is not None:
			headers["Content-Length"] = str(len(data))
			headers["NDC-MSG-SIG"] = self.generator.signature(data=data)
		if self.sid is not None:
			headers["NDCAUTH"] = f"sid={self.sid}"
		if content_type is not None:
			headers["Content-Type"] = content_type
		return headers

	def web_headers(self, referer):
		headers = {
			"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36",
			"content-type": "application/json",
			"x-requested-with": "xmlhttprequest",
			"cookie": f"sid={self.sid}",
			"referer": referer
		}
		return headers



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
		with self.session.post(f"{self.api}/g/s/auth/login", headers=self.headers(data=data), data=data) as response:
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else:json_response = json.loads(response.text)
		self.sid = json_response["sid"]
		self.uid = json_response["account"]["uid"]
		self.logged = True
		return self.uid

	def get_my_chats(self, start: int = 0, size: int = 25, comId: str = None):

		"""

		Get chats on account


		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.
		-*comId*: Community id (if you want to get a list of chats from a community, otherwise you will get a list of chats in the global amino menu)


		"""
		if self.logged == False: return exceptions.checkExceptionsLocal('1')
		if comId!=None:
			response = self.session.get(f"{self.api}/x{comId}/s/chat/thread?type=joined-me&start={start}&size={size}", headers=self.headers())
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["threadList"]
		else:
			response = self.session.get(f"{self.api}/g/s/chat/thread?type=joined-me&start={start}&size={size}", headers=self.headers())
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["threadList"]

	def get_my_communities(self, start: int = 0, size: int = 25):

		"""

		Get communities on account


		** options **

		- *start* : Where to start the list.
		- *size* : The size of the list.

		"""
		if self.logged == False: return exceptions.checkExceptionsLocal('1')
		response = self.session.get(f"{self.api}/g/s/community/joined?v=1&start={start}&size={size}", headers=self.headers())
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["communityList"]

	def join_community(self, comId):


		"""

		join the community

		** options **
		-*comId*: Community id

		"""

		if self.logged == False: return exceptions.checkExceptionsLocal('1')
		data = json.dumps({"timestamp": int(timestamp() * 1000)})
		response = self.session.post(f"{self.api}/x{comId}/s/community/join", headers=self.headers(data=data), data=data)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code




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
			response = self.session.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}", headers=self.headers())
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)["thread"]
		else:
			response = self.session.get(f"{self.api}/g/s/chat/thread/{chatId}", headers=self.headers())
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
			response = self.session.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}", headers=self.headers())
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)['messageList']
		else:
			response = self.session.get(f"{self.api}/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}", headers=self.headers())
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return json.loads(response.text)['messageList']


	def get_from_link(self, link: str):
		"""
		Get the information from the Amino URL.
		** options **
		- *link* : link.

		"""
		response = self.session.get(f"{self.api}/g/s/link-resolution?q={link}", headers=self.headers())
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return json.loads(response.text)["linkInfoV2"]




	"""


														░██╗░░░░░░░██╗███████╗██████╗░      ███████╗██╗░░░██╗███╗░░██╗░█████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
														░██║░░██╗░░██║██╔════╝██╔══██╗      ██╔════╝██║░░░██║████╗░██║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
														░╚██╗████╗██╔╝█████╗░░██████╦╝      █████╗░░██║░░░██║██╔██╗██║██║░░╚═╝░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
														░░████╔═████║░██╔══╝░░██╔══██╗      ██╔══╝░░██║░░░██║██║╚████║██║░░██╗░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
														░░╚██╔╝░╚██╔╝░███████╗██████╦╝      ██║░░░░░╚██████╔╝██║░╚███║╚█████╔╝░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
														░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░      ╚═╝░░░░░░╚═════╝░╚═╝░░╚══╝░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░


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
		if self.logged == False: return exceptions.checkExceptionsLocal('1')
		data = json.dumps(data)
		response = self.session.post(f"https://aminoapps.com/api/add-chat-message",headers=self.web_headers(referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={comId}"),data=data)
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
		if self.logged == False: return exceptions.checkExceptionsLocal('1')
		data = json.dumps(data)
		response = self.session.post(f"https://aminoapps.com/api/join-thread", headers=self.web_headers(referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={comId}"), data=data)
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
		if self.logged == False: return exceptions.checkExceptionsLocal('1')
		data = json.dumps(data)
		response = self.session.post(f"https://aminoapps.com/api/leave-thread", headers=self.web_headers(referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={comId}"), data=data)
		if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
		else: return response.status_code	


	"""

												███╗░░██╗░█████╗░████████╗  ░██╗░░░░░░░██╗░█████╗░██████╗░██╗░░██╗██╗███╗░░██╗░██████╗░
												████╗░██║██╔══██╗╚══██╔══╝  ░██║░░██╗░░██║██╔══██╗██╔══██╗██║░██╔╝██║████╗░██║██╔════╝░
												██╔██╗██║██║░░██║░░░██║░░░  ░╚██╗████╗██╔╝██║░░██║██████╔╝█████═╝░██║██╔██╗██║██║░░██╗░
												██║╚████║██║░░██║░░░██║░░░  ░░████╔═████║░██║░░██║██╔══██╗██╔═██╗░██║██║╚████║██║░░╚██╗
												██║░╚███║╚█████╔╝░░░██║░░░  ░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██║░╚██╗██║██║░╚███║╚██████╔╝
												╚═╝░░╚══╝░╚════╝░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░╚═════╝░

												███████╗██╗░░░██╗███╗░░██╗░█████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
												██╔════╝██║░░░██║████╗░██║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
												█████╗░░██║░░░██║██╔██╗██║██║░░╚═╝░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
												██╔══╝░░██║░░░██║██║╚████║██║░░██╗░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
												██║░░░░░╚██████╔╝██║░╚███║╚█████╔╝░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
												╚═╝░░░░░░╚═════╝░╚═╝░░╚══╝░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░


	"""



	def send_message(self, chatId: str, message: str, messageType: int = 0, replyTo: str = None, comId: str = None):
		"""

		Send message


		** options **

		*chatId*: Chat ID
		*message*: message to send
		*messageType*: message type (normal - 0)
		*replyTo*: id of the message you want to reply to
		*comId*: community id (if the chat is in a community)

		"""

		data = {
				"type": messageType,
				"content": message,
				"clientRefId": int(timestamp() / 10 % 1000000000),
				"timestamp": int(timestamp() * 1000)
			}
		if comId!=None:
			if self.logged == False: return exceptions.checkExceptionsLocal('1')
			data = json.dumps(data)
			if replyTo != None: data["replyMessageId"] = replyTo
			response = self.session.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/message", headers=self.headers(data=data))
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return response.status_code
		else:
			data = json.dumps(data)
			if replyTo != None: data["replyMessageId"] = replyTo
			response = self.session.post(f"{self.api}/g/s/chat/thread/{chatId}/message", headers=self.headers(data=data), data=data)
			if response.status_code != 200: return exceptions.checkExceptions(json.loads(response.text))
			else: return response.status_code