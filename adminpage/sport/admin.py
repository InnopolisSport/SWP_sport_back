from django.contrib import admin
import sport.models as models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Group)
admin.site.register(models.Quiz)
admin.site.register(models.SelectedPriority)
admin.site.register(models.Sport)

