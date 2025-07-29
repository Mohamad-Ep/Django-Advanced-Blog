from rest_framework import serializers
from ...models import User,Profile
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# __________________________________________________________

class RegisterationSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128)
    
    class Meta:
        model = User
        fields = ['email','password','re_password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        
        if password != re_password:
            raise serializers.ValidationError({'details':'password is not match'})
        
        errors = dict()
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
          errors['passsword'] = list(e.messages)
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('re_password',None)
        return User.objects.create_user(**validated_data)
# __________________________________________________________

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verficated:
                raise serializers.ValidationError({'details':'user is not Verficated'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
# __________________________________________________________

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verficated:
            raise serializers.ValidationError({'details':'user is not Verficated'})
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        return data
# __________________________________________________________

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    confirm_new_password = serializers.CharField(max_length=128, required=True)
    
    def validate(self, attrs):
        password = attrs.get('new_password')
        re_password = attrs.get('confirm_new_password')
        
        if password != re_password:
            raise serializers.ValidationError({'details':'password is not match'})
        
        errors = dict()
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
          errors['passsword'] = list(e.messages)
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('re_password',None)
        return User.objects.create_user(**validated_data)
# __________________________________________________________

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email',read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id','email','first_name','last_name','description','created_date']
        
# __________________________________________________________

class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)
            if user_obj.is_verficated:
                raise serializers.ValidationError({'details':'The user has already been confirmed'})
        
        except User.DoesNotExist:
            raise serializers.ValidationError({'email':'email dos not exits'})
         
        attrs['user'] = user_obj
         
        return super().validate(attrs)
# __________________________________________________________