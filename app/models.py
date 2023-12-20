from django.db import models

class Chat(models.Model):
    user_input = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    
class CsvFile(models.Model):
    file = models.FileField(upload_to='uploads/')