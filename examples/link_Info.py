import AminoXZ

link = 'http://aminoapps.com/p/poejw4' #your link from aminoapps -> example: http://aminoapps.com/p/q9op9y

client = AminoXZ.Client()
linkInfo = client.get_from_link(link)

_dict = linkInfo.json #full info

comId = linkInfo.comId #id of community
objectId = linkInfo.objectId #chatId if link to chat, blogId if link to blog ....
objectType = linkInfo.objectType #type of object (see documentation)
