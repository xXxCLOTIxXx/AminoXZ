from . import client

from .lib.util.generator import Generator

from .lib.util import exceptions, objects



import requests
import json
import base64

from typing import BinaryIO, Union
from time import time as timestamp
from threading import Thread

class LocalClient(client.Client):
	def __init__(self, comId: str, profile: objects.UserProfile, deviceId: str = None):
		client.Client.__init__(self, deviceId=deviceId)
		self.comId = comId
		self.profile = profile
		self.sid = profile.sid


	def get_my_chats(self, start: int = 0, size: int = 10):

		response = self.session.get(f"{self.api}/x{self.comId}/s/chat/thread?type=joined-me&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.ThreadList(json.loads(response.text)["threadList"])


	def send_message(self, chatId: str, message: str = None, messageType: int = 0, file: BinaryIO = None, fileType: str = None, replyTo: str = None, mentionUserIds: list = None, stickerId: str = None, embedId: str = None, embedType: int = None, embedLink: str = None, embedTitle: str = None, embedContent: str = None, embedImage: BinaryIO = None, linkSnippet: str = None, linkSnippetImage: BinaryIO = None):

		if message is not None and file is None:
			message = message.replace("<@", "‎‏").replace("@>", "‬‭")

		mentions = []
		if mentionUserIds:
			for mention_uid in mentionUserIds:
				mentions.append({"uid": mention_uid})

		if embedImage:
			embedImage = [[100, self.upload_media(embedImage, "image"), None]]

		if linkSnippetImage:
			linkSnippetImage = base64.b64encode(linkSnippetImage.read()).decode()

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
			"extensions": {
				"mentionedArray": mentions,
				"linkSnippetList": [{
					"link": linkSnippet,
					"mediaType": 100,
					"mediaUploadValue": linkSnippetImage,
					"mediaUploadValueContentType": "image/png"
				}]
			},
			"timestamp": int(timestamp() * 1000)
		}

		if replyTo: data["replyMessageId"] = replyTo

		if stickerId:
			data["content"] = None
			data["stickerId"] = stickerId
			data["type"] = 3

		if file:
			data["content"] = None
			if fileType == "audio":
				data["type"] = 2
				data["mediaType"] = 110

			elif fileType == "image":
				data["mediaType"] = 100
				data["mediaUploadValueContentType"] = "image/jpg"
				data["mediaUhqEnabled"] = True

			elif fileType == "gif":
				data["mediaType"] = 100
				data["mediaUploadValueContentType"] = "image/gif"
				data["mediaUhqEnabled"] = True

			else: raise exceptions.WrongType(fileType)

			data["mediaUploadValue"] = base64.b64encode(file.read()).decode()

		data = json.dumps(data)

		response = self.session.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code

	def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None):

		data = {
			"adminOpName": 102,
			"timestamp": int(timestamp() * 1000)
		}
		if asStaff and reason:data["adminOpNote"] = {"content": reason}

		data = json.dumps(data)
		if not asStaff: response = self.session.delete(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}", headers=self.parse_headers(data=data), proxies=self.proxies, verify=self.certificatePath)
		else: response = self.session.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}/admin", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code



	def join_chat(self, chatId: str):

		response = self.session.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.uid}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code

	def leave_chat(self, chatId: str):

		response = self.session.delete(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.uid}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code


	def get_all_users(self, type: str = "recent", start: int = 0, size: int = 25):

		if type == "recent": response = self.session.get(f"{self.api}/x{self.comId}/s/user-profile?type=recent&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		elif type == "banned": response = self.session.get(f"{self.api}/x{self.comId}/s/user-profile?type=banned&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		elif type == "featured": response = self.session.get(f"{self.api}/x{self.comId}/s/user-profile?type=featured&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		elif type == "leaders": response = self.session.get(f"{self.api}/x{self.comId}/s/user-profile?type=leaders&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		elif type == "curators": response = self.session.get(f"{self.api}/x{self.comId}/s/user-profile?type=curators&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		else: raise exceptions.WrongType(type)

		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.UserProfileCountList(json.loads(response.text)).UserProfileCountList


	def get_online_users(self, start: int = 0, size: int = 25):

		response = self.session.get(f"{self.api}/x{self.comId}/s/live-layer?topic=ndtopic:x{self.comId}:online-members&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.UserProfileCountList(json.loads(response.text)).UserProfileCountList

	def get_online_favorite_users(self, start: int = 0, size: int = 25):

		response = self.session.get(f"{self.api}/x{self.comId}/s/user-group/quick-access?type=online&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.UserProfileCountList(json.loads(response.text)).UserProfileCountList

	def get_user_info(self, userId: str):

		response = self.session.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.UserProfile(json.loads(response.text)["userProfile"]).UserProfile


	def get_chat_threads(self, start: int = 0, size: int = 25):

		response = self.session.get(f"{self.api}/x{self.comId}/s/chat/thread?type=joined-me&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.ThreadList(json.loads(response.text)["threadList"]).ThreadList

	def get_public_chat_threads(self, type: str = "recommended", start: int = 0, size: int = 25):

		response = self.session.get(f"{self.api}/x{self.comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.ThreadList(json.loads(response.text)["threadList"]).ThreadList

	def get_chat_thread(self, chatId: str):

		response = self.session.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.Thread(json.loads(response.text)["thread"]).Thread

	def get_chat_messages(self, chatId: str, size: int = 25, pageToken: str = None):

		if pageToken is not None: url = f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&pageToken={pageToken}&size={size}"
		else: url = f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"

		response = self.session.get(url, headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.GetMessages(json.loads(response.text)).GetMessages

	def get_message_info(self, chatId: str, messageId: str):

		response = self.session.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}", headers=self.parse_headers(), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.Message(json.loads(response.text)["message"]).Message

	#need fix :(
	def create_chat(self, userId: Union[str, list], message: str, title: str = None, content: str = None, isGlobal: bool = False, publishToGlobal: bool = False):
		if isinstance(userId, str): userIds = [userId]
		elif isinstance(userId, list): userIds = userId
		else: raise exceptions.WrongType(type(userId))

		data = {
			"title": title,
			"inviteeUids": userIds,
			"initialMessageContent": message,
			"content": content,
			"timestamp": int(timestamp() * 1000)
		}

		if isGlobal is True: data["type"] = 2; data["eventSource"] = "GlobalComposeMenu"
		else: data["type"] = 0

		if publishToGlobal is True: data["publishToGlobal"] = 1
		else: data["publishToGlobal"] = 0

		data = json.dumps(data)
		
		response = self.session.post(f"{self.api}/x{self.comId}/s/chat/thread", data=data, headers=self.parse_headers(data=data), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return objects.Thread(json.loads(response.text)["thread"]).Thread


	def follow(self, userId: Union[str, list]):

		if isinstance(userId, str):
			response = self.session.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/member", headers=self.parse_headers(type='android'), proxies=self.proxies, verify=self.certificatePath)
		elif isinstance(userId, list):
			data = json.dumps({"targetUidList": userId, "timestamp": int(timestamp() * 1000)})
			response = self.session.post(f"{self.api}/x{self.comId}/s/user-profile/{self.profile.userId}/joined", headers=self.parse_headers(data=data), data=data, proxies=self.proxies, verify=self.certificatePath)
		else: raise exceptions.WrongType(type(userId))
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code

	def unfollow(self, userId: str):

		response = self.session.delete(f"{self.api}/x{self.comId}/s/user-profile/{self.profile.userId}/joined/{userId}", headers=self.parse_headers(type='android'), proxies=self.proxies, verify=self.certificatePath)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code