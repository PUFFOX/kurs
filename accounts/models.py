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
    

# Метод для назв дисциплін
class Subject(models.Model):
    name_subject = models.CharField(max_length=100, unique=True)  # Назва предмету, наприклад: "Програмування"

    def __str__(self): #"магічний метод" 
        return self.name_subject
    

# Метод для тип дисциплін
class LessonType(models.Model):
    name_lesson_type = models.CharField(max_length=10, unique=True)  # Тип заняття, наприклад: "Лекція", "Практика"
    def __str__(self):
        return self.name_lesson_type


class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Курсант
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Предмет
    lesson_type = models.ForeignKey(LessonType, on_delete=models.CASCADE)  # Тип заняття
    grade = models.IntegerField()  # Оцінка або бали (2–5 або 50–100)
    date_given = models.DateField(auto_now_add=True)  # Дата виставлення

    def __str__(self):
        return f"{self.user.username} — {self.subject.name_subject} — {self.grade}"
