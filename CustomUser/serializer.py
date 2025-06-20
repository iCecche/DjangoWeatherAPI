from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'username': {'required': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': "Le password non coincidono."})
        return data

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            is_premium=validated_data['is_premium']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user