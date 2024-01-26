from django.db import models
from custom_user.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'),])
    age = models.CharField(max_length=10, choices=[('18-24', '18-24'), ('25-34', '25-34'), ('35-44', '35-44'), ('45-54', '45-54'), ('55-64', '55-64'), ('64+', '64 and older')])
    relationship_status = models.CharField(max_length=15, choices=[('S','Single'), ('M','Married')], null=True, blank=True)
    children = models.CharField(max_length=15, choices=[('Y','Yes'), ('N','No')], null=True, blank=True)

    image = models.ImageField(upload_to='images/',null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} -- {self.name}"


class Profile_step3(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='step3')
    
    MULTIPLE_CHOICES = [
        ('option1', 'I want to increase happiness'),
        ('option2', 'I want to express gratitude'),
        ('option3', 'I want an energy boost'),
        ('option4', 'I want to feel more confident'),
        ('option5', 'I want to feel more relaxed'),
        ('option6', 'I want to feel peace'),
        ('option7', 'I want to reduce stress'),
        ('option8', 'I want to calm anxiety'),
        ('option9', 'I want to lower my blood pressure and heart rate'),
    ]
    choice = models.CharField(max_length=20, choices=MULTIPLE_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.choice}"

    class Meta:
        verbose_name_plural = 'profile3'