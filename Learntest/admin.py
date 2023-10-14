from django.contrib import admin
from .models import Question, MultiQuesModel, SingleQuestion, SingleChoiceQuestion
# Register your models here.
admin.site.register(Question) # will be modified into notes
admin.site.register(MultiQuesModel)
admin.site.register(SingleQuestion)

admin.site.register(SingleChoiceQuestion)
# add single question reference
