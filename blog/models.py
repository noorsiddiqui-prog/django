
from django.db import models
# from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.



    
class Blog(models.Model):
    
    blog_title = models.CharField(max_length=255)
    blog_content = models.TextField()
    blog_image=models.ImageField(blank=True, upload_to='BlogImages')
    blog_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Blog title: "+str(self.blog_title)
    
class Comments(models.Model):
    comment_content = models.TextField()
    blog_no=models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    