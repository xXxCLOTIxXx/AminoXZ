import json

class UnsupportedService(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidRequest(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidSession(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class AccessDenied(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class UnexistentData(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class ActionNotAllowed(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class ServiceUnderMaintenance(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class MessageNeeded(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidAccountOrPassword(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class AccountDisabled(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidEmail(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidPassword(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class EmailAlreadyTaken(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class UnsupportedEmail(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class AccountDoesntExist(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidDevice(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class AccountLimitReached(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class TooManyRequests(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class CantFollowYourself(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class UserUnavailable(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class YouAreBanned(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class UserNotMemberOfCommunity(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class RequestRejected(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class ActivateAccount(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class CantLeaveCommunity(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class ReachedTitleLength(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class EmailFlaggedAsSpam(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class AccountDeleted(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class API_ERR_EMAIL_NO_PASSWORD(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_VERIFY(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class VerificationRequired(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class API_ERR_INVALID_AUTH_NEW_DEVICE_LINK(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class CommandCooldown(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class UserBannedByTeamAmino(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class IpTemporaryBan(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class UnknownError(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)



class IncorrectType(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class NotAuthorized(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class CapchaNotRecognize(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class WrongType(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InternalServerError(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidVerificationCode(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)



def checkExceptions(data = None, local: dict = None):
	local_code = None
	code = None
	if local:local_code = local['code']
	if data:
		try:
			data = json.loads(data)
			try:code = data["api:statuscode"]
			except:raise UnknownError(data)
		except json.decoder.JSONDecodeError:code = 403




	if code == 100: raise UnsupportedService(data)
	elif code == 101: raise InternalServerError(data)
	elif code == 103 or code == 104: raise InvalidRequest(data)
	elif code == 105: raise InvalidSession(data)
	elif code == 106: raise AccessDenied(data)
	elif code == 107: raise UnexistentData(data)
	elif code == 110: raise ActionNotAllowed(data)
	elif code == 111: raise ServiceUnderMaintenance(data)
	elif code == 113: raise MessageNeeded(data)
	elif code == 201: raise AccountDisabled(data)
	elif code == 210: raise AccountDisabled(data)
	elif code == 213: raise InvalidEmail(data)
	elif code == 214: raise InvalidPassword(data)
	elif code == 215: raise EmailAlreadyTaken(data) and UnsupportedEmail(data)
	elif code == 216: raise AccountDoesntExist(data)
	elif code == 218: raise InvalidDevice(data)
	elif code == 219: raise AccountLimitReached(data) or TooManyRequests(data)
	elif code == 225: raise UserUnavailable(data)
	elif code == 229: raise YouAreBanned(data)
	elif code == 230: raise UserNotMemberOfCommunity(data)
	elif code == 235: raise RequestRejected(data)
	elif code == 238: raise ActivateAccount(data)
	elif code == 239: raise CantLeaveCommunity(data)
	elif code == 241: raise EmailFlaggedAsSpam(data)
	elif code == 246: raise AccountDeleted(data)
	elif code == 251: raise API_ERR_EMAIL_NO_PASSWORD(data)
	elif code == 257: raise API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_VERIFY(data)
	elif code == 270: raise VerificationRequired(data)
	elif code == 271: raise API_ERR_INVALID_AUTH_NEW_DEVICE_LINK(data)
	elif code == 291: raise CommandCooldown(data)
	elif code == 293: raise UserBannedByTeamAmino(data)
	elif code == 3102: raise InvalidVerificationCode(data)

	elif local_code == 1: raise IncorrectType(local['text'])
	elif local_code == 2: raise NotAuthorized(local['text'])
	else: raise UnknownError(data)