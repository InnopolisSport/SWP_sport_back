from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)


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

    # Or handle it as you wish. For instance, save to DB.
    return HttpResponse('Hello, ' + result['first_name'] + '!')
