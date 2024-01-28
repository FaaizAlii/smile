from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import *
from base.serializers import UserSerializer


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['smile_count', 'smile_sec']


class SmileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smile
        fields = ['smile_count','smile_sec','best_smile','smile_avg','streak','max_streak']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['total_points','current_level']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImages
        fields = ['image']
    
    def validate_image(self, value):
        allowed_extensions = ['jpg', 'jpeg', 'png']
        file_extension = value.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise ValidationError(
                'Only JPEG, JPG, and PNG image formats are allowed.'
            )

        return value