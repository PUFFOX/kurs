from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Subject
admin.site.register(Subject)  # Реєструємо модель Subject в адмінці
from .models import LessonType
admin.site.register(LessonType)  # Реєструємо модель LessonType в адмінці

from .models import Grade
admin.site.register(Grade)




#admin.site.register(Group)  # ← це показує "Групи" в адмінці


