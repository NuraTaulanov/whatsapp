from django.db import models


class UserResponse(models.Model):
    sender_number = models.CharField(max_length=20)
    response = models.TextField()
