from django.db import models
from django.contrib.auth.models import User

# Модель навчальної групи
class StudyGroup(models.Model):
    number = models.CharField(max_length=10, unique=True)  # Наприклад: 301-КС

    def __str__(self):
        return self.number

# Розширена інформація про користувача
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    