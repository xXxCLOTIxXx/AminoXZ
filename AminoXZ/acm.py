from . import client
from .lib.util import exceptions, objects
from time import time as timestamp
import json

class ACM(client.Client):
	def __init__(self, profile: objects.UserProfile, comId: str = None, proxies: dict = None, deviceId: str = None):

		client.Client.__init__(self, deviceId=deviceId, proxies=proxies)

		self.profile = profile
		self.comId = comId
		self.sid = profile.sid


	def edit_community(self, name: str = None, description: str = None, aminoId: str = None, primaryLanguage: str = None, themePackUrl: str = None, joinType: int = None):

		"""
		
		joinType: int 
			0 - open
			1 - permission needed
			2 - closed

		"""

		data = {"timestamp": int(timestamp() * 1000)}

		if name: data["name"] = name
		if description: data["content"] = description
		if aminoId: data["endpoint"] = aminoId
		if primaryLanguage: data["primaryLanguage"] = primaryLanguage
		if themePackUrl: data["themePackUrl"] = themePackUrl
		if joinType: data["joinType"] = joinType

		data = json.dumps(data)

		if self.comId is None: raise exceptions.CommunityNeeded()
		response = self.session.post(f"{self.api}/x{self.comId}/s/community/settings", data=data, headers=self.parse_headers(data=data), proxies=self.proxies)
		if response.status_code != 200: return exceptions.checkExceptions(response.text)
		else: return response.status_code