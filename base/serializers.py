from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from custom_user.models import User

from .models import Profile, Profile_step3


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# class Profile1Serializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Profile
#         fields = ['user', 'name', 'age', 'gender']


# class Profile2Serializer(serializers.Serializer):
#     relationship_status = serializers.CharField(max_length=5)
#     children = serializers.CharField(max_length=5)

#     def update(self, instance, validated_data):
#         instance.relationship_status = validated_data.get(
#             'relationship_status', instance.relationship_status)
#         instance.children = validated_data.get('children', instance.children)
#         instance.save()
#         return instance


class Profile3Serializer(serializers.Serializer):
    choice = serializers.CharField(max_length=10)

    def create(self, validated_data):
        profile3 = Profile_step3.objects.create(
            user=validated_data['user'],
            choice=validated_data['choice']
        )
        return profile3


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
