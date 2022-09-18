from django.contrib import admin
# from django import forms
# from django_admin_json_editor import JSONEditorWidget

from training_suggestor.admin.site import site
from training_suggestor.models import Poll, PollQuestion

# DATA_SCHEMA = {
#     "type": "array",
#     "title": "Answers",
#     "items": {
#         "type": "object",
#         "properties": {
#             "answer": {
#                 "type": "string"
#             },
#             "time_ratio_influence": {
#                 "type": "number"
#             },
#             "working_load_ratio_influence": {
#                 "type": "number"
#             }
#         },
#         "required": [
#             "answer"
#         ]
#     }
# }
#
#
# class PollQuestionForm(forms.ModelForm):
#     class Meta:
#         model = PollQuestion
#         fields = '__all__'
#         widgets = {
#             'answers': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
#         }

class PollQuestionInline(admin.TabularInline):
    model = PollQuestion
    # form = PollQuestionForm


@admin.register(Poll, site=site)
class PollAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (PollQuestionInline,)
