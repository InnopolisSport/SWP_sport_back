from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)
import requests


def telegram_bot_sendtext(id: str, message: str):
    send_text = 'https://api.telegram.org/bot' + settings.TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + id + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response.json()


def auth_view(request):
    if not request.GET.get('hash'):
        return HttpResponse('Handle the missing Telegram data in the response.')

    try:
        result = verify_telegram_authentication(settings.TELEGRAM_BOT_TOKEN, request_data=request.GET)
    except TelegramDataIsOutdatedError:
        return HttpResponse('Authentication was received more than a day ago.')
    except NotTelegramDataError:
        return HttpResponse('The data is not related to Telegram!')

    request.user.telegram_id = result['id']
    request.user.save()

    telegram_bot_sendtext(result['id'], 'Hello, ' + result['first_name'] + ' ' + result['last_name'] + '!')

    # Or handle it as you wish. For instance, save to DB.
    return redirect('/')
