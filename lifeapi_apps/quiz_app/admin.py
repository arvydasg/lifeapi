from django.contrib import admin
from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'type', 'created_by')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('formatted_date_added', 'question', 'answer', 'created_by')

    def formatted_date_added(self, obj):
        return obj.date_added.strftime('%Y-%m-%d %H:%M')

    formatted_date_added.short_description = 'Date Added'

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)