from django.db import models

class UserData(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Note(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Todo(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title
