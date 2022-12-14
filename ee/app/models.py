from django.db import models

class UserImage(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, )
    img = models.ImageField(upload_to='userimg/', blank=True)

    def __str__(self): 
        return self.author
