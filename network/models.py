from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(blank=True, null=True, default=0)
    following = models.IntegerField(blank=True, null=True, default=0)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userpost")
    text = models.TextField()
    likes = models.IntegerField(blank=True, null=True, default =0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} posted on {self.timestamp}"

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userf")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userfollowing")

    def __str__(self):
        return f"{self.user} follows {self.following}"

    def is_valid_following(self):
        return self.user != self.following
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userliking")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postliking")
    like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.post}"