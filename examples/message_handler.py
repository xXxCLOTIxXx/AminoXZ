import AminoXZ

client = AminoXZ.Client()
client.login(email='email', password='password')


@client.event('on_text_message')
def on_text_message(data):
	comId = data.comId
	chatId = data.message.chatId
	message = data.message.content
	print(f"New message:\n {message}")


@client.event('on_group_member_join')
def on_leave(data):
	comId = data.comId
	chatId = data.message.chatId
	lClient = AminoXZ.LocalClient(comId=comId, profile=client.profile)
	lClient.send_message(chatId=chatId, message='Welcome to chat')

@client.event('on_group_member_leave')
def on_join(data):
	comId = data.comId
	chatId = data.message.chatId
	lClient = AminoXZ.LocalClient(comId=comId, profile=client.profile)
	lClient.send_message(chatId=chatId, message='Bye')