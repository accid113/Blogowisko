from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Post(models.Model):
    user = models.ForeignKey(
        User, related_name="Post",
        on_delete=models.DO_NOTHING,
    )
    body = models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user}"
            f" ({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self',
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)

    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]