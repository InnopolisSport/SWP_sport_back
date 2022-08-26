from django.contrib import admin


class SportTelegramBotAdminSite(admin.AdminSite):
    site_header = 'Telegram bot administration'
    index_title = 'innosport+'
    site_title = 'Admin telegram bot panel'


site = SportTelegramBotAdminSite(name="telegram-bot-admin")
