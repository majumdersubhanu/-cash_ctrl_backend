from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password', 'profile_pic')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Unable to log in with provided credentials.')


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'full_name', 'date_of_birth', 'gender', 'current_address', 'nationality',
            'job_title', 'company_name', 'employment_status', 'monthly_income',
            'account_number', 'ifsc_code', 'bank_name', 'upi_id',
            'pan_card', 'aadhaar_card',
        ]
        extra_kwargs = {
            'full_name': {'required': True},
            'date_of_birth': {'required': True},
            'gender': {'required': True},
            'current_address': {'required': True},
            'nationality': {'required': True},
            'job_title': {'required': True},
            'company_name': {'required': True},
            'employment_status': {'required': True},
            'monthly_income': {'required': True},
            'account_number': {'required': True},
            'ifsc_code': {'required': True},
            'bank_name': {'required': True},
            'upi_id': {'required': True},
            'pan_card': {'required': True},
            'aadhaar_card': {'required': True},
        }
