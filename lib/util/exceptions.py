from colored import fore


def checkExceptions(response):
	codes = {
		'100': "\nUnsupported service. Your client may be out of date. Please update it to the latest version.\nнеподдерживаемый сервис. Возможно, ваш клиент устарел. Пожалуйста, обновите его до последней версии\n",
		'103': "\nInvalid Request. Please update to the latest version. If the problem continues, please contact us.\nНеверный запрос. Пожалуйста, обновите до последней версии. Если проблема не исчезнет, свяжитесь с нами.\n",
		'104': "\nInvalid Request. Please update to the latest version. If the problem continues, please contact us.\nНеверный запрос. Пожалуйста, обновите до последней версии. Если проблема не исчезнет, свяжитесь с нами.\n",
		'105': "\nInvalid Session.\nНеверный сеанс.\n",
		'106': "\nAccess denied.\nВ доступе отказано.\n",
		'107': "\nThe requested data does not exist.\nЗапрошенные данные не существуют.\n",
		'110': "\nAction not allowed.\nДействие запрещено.\n",
		'111': "\nSorry, this service is under maintenance. Please check back later.\nИзвините, этот сервис находится на техническом обслуживании. Пожалуйста, зайдите позже.\n",
		'113': "\nBe more specific, please.\nБудьте конкретнее, пожалуйста.\n",
		'201': "\n\n\n",
		'210': "\nThis account is disabled.\nЭта учетная запись отключена.\n",
		'213': "\nInvalid email address.\nНеверный адрес электронной почты.\n",
		'214': "\nInvalid password. Password must be 6 characters or more and contain no spaces.\nНеверный пароль. Пароль должен состоять из 6 символов или более и не содержать пробелов.\n",
		'215': "\nThis email has been registered already.\n'Этот электронный адрес уже зарегистрирован.\n",
		'216': "\nThis email address is not supported.\nЭтот адрес электронной почты не поддерживается.\n",
		'218': "\nStatusCode: 218\nYour device is currently not supported or the app is out of date. Update it to the latest version.\nВаше устройство сейчас не поддерживается или приложение устарело. Обновите его до последней версии.\n",
		'219': "\nToo many requests, please wait a while and try again, or enable VPN.\nСлишком много запросов, подождите немного и повторите попытку или включите VPN\n",
		'225': "\nThis user is unavailable.\nЭтот пользователь недоступен.\n",
		'229': "\nYou are banned.\nВы заблокированы.\n",
		'230': "\nYou have to join this Community first.\nСначала вы должны присоединиться к этому сообществу.\n",
		'235': "\nRequest rejected. You have been temporarily muted (read only mode) because you have received a strike. To learn more, please check the Help Center.\nЗапрос отклонен. Вы были временно заблокированы (режим только для чтения), потому что получили предупреждение. Чтобы узнать больше, посетите Справочный центр.\n",
		'238': "\nPlease activate your account first.\nСначала активируйте свою учетную запись.\n",
		'239': "\nSorry, you can not do this before transferring your Agent status to another member.\nК сожалению, вы не можете сделать это до передачи статуса Агента другому участнику.\n",
		'240': "\nSorry, the max length of member's title is limited to 20.\nИзвините, максимальная длина титула участника ограничена 20.\n",
		'241': "\nThis email provider has been flagged for use in spamming.\nЭтот провайдер электронной почты был помечен для рассылки спама.\n",
		'246': "\nAccount deleted.\nАккаунт удалён.\n",
		'262': "\nYou can only add up to 20 Titles. Please choose the most relevant ones.\nВы можете добавить не более 20 заголовков. Пожалуйста, выберите наиболее подходящие.\n",
		'270': "\nVerification Required.\nТребуется проверка.\n",
		'291': "\nYou've done too much too quickly. Take a break and try again later.\nВы сделали запросы слишком слишком быстро и много. Сделайте перерыв и повторите попытку позже.\n",
		'293': "\nSorry, this user has been banned by Team Amino.\nИзвините, этот пользователь был забанен Командой Amino.\n",
		'1600': "\nData not found, you may not have specified some parameter.\nДанные не найдены, возможно вы не указали какой-то параметр.\n",

	}
	try:return print(fore.RED, codes[str(response["api:statuscode"])], fore.WHITE)
	except:return print(fore.RED, response, fore.WHITE)


def checkExceptionsLocal(error):
	errors = {
		'0': 'You are not logged in.\nВы не вошли.\n',
		'1': "You are not logged in.\nВы не вошли в аккаунт.",
		'2': "\nType not found\nТип не найден\n"
	}

	try:return print(fore.ORANGE_1, errors[error], fore.WHITE)
	except:return print(fore.ORANGE_1,'Error\n Error type not found', fore.WHITE)