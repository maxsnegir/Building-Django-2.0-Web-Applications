from django.contrib import admin

# Register your models here.
from qanda.models import Question, Answer

admin.site.register(Answer)
admin.site.register(Question)
