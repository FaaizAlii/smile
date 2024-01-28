from django.db import models
from custom_user.models import User

from django.core.validators import MaxValueValidator


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Smile(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    smile_count = models.IntegerField(default=0)
    smile_sec = models.IntegerField(default=0)
    best_smile = models.IntegerField(default=0)
    smile_avg = models.DecimalField(max_digits = 10, decimal_places=2, default=0)
    streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    streak_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - streak - {self.streak}"


class Goal(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    # smile = models.OneToOneField(Smile, on_delete=models.CASCADE, related_name='goal', default=None)
    smile_sec = models.IntegerField(default=0)
    smile_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - goal"


class Level(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_level = models.PositiveIntegerField(default=1)
    points = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.profile.name} - level = {self.current_level}"

class Activity(TimestampModel):
    task = models.CharField(max_length=255)
    details = models.TextField()
    

class Community(TimestampModel):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    max_users = models.IntegerField(validators=[MaxValueValidator(100)])

class UserJoinedCommunity(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    joined = models.BooleanField(default=False)

class CommPost(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

class Friend(TimestampModel):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend = models.OneToOneField(User, related_name='friend', on_delete=models.CASCADE)

class UserImages(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
