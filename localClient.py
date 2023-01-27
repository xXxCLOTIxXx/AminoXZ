from . import client

from .lib.util.generator import Generator

from .lib.util import exceptions, objects

from .lib.util.headers import headers, web_headers

import requests
import json
from typing import BinaryIO
from time import time as timestamp


class LocalClient(client.Client):
	def __init__(self, comId: str, profile: objects.UserProfile, deviceId: str = None):
		client.Client.__init__(self, deviceId=deviceId)
		self.comId = comId
		self.profile = profile
		self.sid = profile.sid


	def get_chats(self, start: int = 0, size: int = 10):
		"""
		List of Chats in account.
		** options **
			- *start* : Where to start the list.
			- *size* : Size of the list.
		"""
		response = self.session.get(f"{self.api}/x{self.comId}/s/chat/thread?type=joined-me&start={start}&size={size}", headers=headers(deviceId=self.deviceId, sid=self.sid), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.ThreadList(json.loads(response.text)["threadList"])


	def send_message(self, chatId: str, message: str, messageType: int = 0, file: BinaryIO = None, fileType: str = None, replyTo: str = None, mentionUserIds: list = None, stickerId: str = None, embedId: str = None, embedType: int = None, embedLink: str = None, embedTitle: str = None, embedContent: str = None, embedImage: BinaryIO = None):
		"""
		Send a Message to a Chat.

		** options **
			- *message* : Message to be sent
			- *chatId* : ID of the Chat.
			- *messageType* : Type of the Message.
		"""
		mentions = []
		data = {
			"type": messageType,
			"content": message,
			"clientRefId": int(timestamp() / 10 % 1000000000),
			"attachedObject": {
				"objectId": embedId,
				"objectType": embedType,
				"link": embedLink,
				"title": embedTitle,
				"content": embedContent,
				"mediaList": embedImage
			},
			"extensions": {"mentionedArray": mentions},
			"timestamp": int(timestamp() * 1000)
		}
		data = json.dumps(data)

		response = self.session.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message", headers=headers(deviceId=self.deviceId, sid=self.sid), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code

	def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None):
		"""
		delete message from chat
		* options *
			- * messageId * : ID of the Message.
			- * chatId * : ID of the Chat.
			- * asStaff * : If execute as a Staff member (Leader or Curator).
			- * reason * : Reason of the action to show on the Moderation History.
		"""
		data = {
			"adminOpName": 102,
			"timestamp": int(timestamp() * 1000)
		}
		if asStaff and reason:data["adminOpNote"] = {"content": reason}

		data = json.dumps(data)
		if not asStaff: response = self.session.delete(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}", headers=headers(deviceId=self.deviceId, sid=self.sid), proxies=self.proxies)
		else: response = self.session.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}/admin", headers=headers(deviceId=self.deviceId, sid=self.sid, data=data), data=data, proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code