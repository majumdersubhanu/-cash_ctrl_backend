from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
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
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')
        user = User.objects.filter(
            Q(username=login) | Q(email=login) | Q(phone_number=login)
        ).first()

        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            return user
        raise serializers.ValidationError('Unable to log in with provided credentials.')


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
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
