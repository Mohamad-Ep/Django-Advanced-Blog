from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import (RegisterationSerializer,CustomAuthTokenSerializer,
                          CustomTokenObtainPairSerializer,ChangePasswordSerializer,
                          ProfileSerializer,ResendActivationSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import User,Profile
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from mail_templated import send_mail,EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from django.conf import settings
# __________________________________________________________

class RegisterationApiView(generics.GenericAPIView):
    serializer_class = RegisterationSerializer
    
    def post(self, request, *args, **kwargs):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            
            email = ser_data.validated_data['email']
            user = get_object_or_404(User,email=email)
            token = self.get_tokens_for_user(user)
            
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@gmail.com',to=[email])

            EmailThread(email_obj).start()
            
            data = {
                'email':email,
                'message':'registeration is successfully',
                'verificate_email':'link verify send to your email; checkuot'
            }
            
            return Response(data=data,status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_tokens_for_user(self,user):
        """ get jwt token for user by refresh token """
    
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
# __________________________________________________________

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
# __________________________________________________________

class CustomDicardAthToken(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'Logout: Token is Removed'},status=status.HTTP_204_NO_CONTENT)
# __________________________________________________________

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
# __________________________________________________________

class ChangePasswordApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    model = User
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        object = self.get_object()
        ser_data = self.get_serializer(data=request.data)
        if ser_data.is_valid():
            if object.check_password(ser_data.data.get('old_password')):
                object.set_password(ser_data.data.get('new_password'))
                object.save()
                return Response(data={'details':'set new password is successfuly'},status=status.HTTP_200_OK)
            return Response(data={'details':'old password is invalid'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data=ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
# __________________________________________________________

class ProfileApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    
    def get_object(self):
        obj = get_object_or_404(self.queryset,user=self.request.user)
        return obj
# __________________________________________________________

class TestEmailSend(APIView):
    
    def get(self,request,*args, **kwargs):
        
        # send_mail(
        #     "Subject here",
        #     "Here is the message.",
        #     "from@example.com",
        #     ["to@example.com"],
        #     fail_silently=False,
        # )
        self.email = 'nazanin.bayat@gmail.com'
        user = get_object_or_404(User,email=self.email)
        token = self.get_tokens_for_user(user)
        
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'admin@gmail.com',to=[self.email])

        EmailThread(email_obj).start()
        
        return Response({'details':'EmailTest is Send'})
    
    def get_tokens_for_user(self,user):
        if not user.is_active:
            raise AuthenticationFailed("User is not active")
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
# __________________________________________________________

class ActivationApiView(APIView):
    def get(self,request,token):
        try:
            token_obj = jwt.decode(jwt=token,key=settings.SECRET_KEY,algorithms=['HS256'])
            user_id = token_obj.get("user_id")
            user = get_object_or_404(User,pk=user_id)
            if not user.is_verficated:
                user.is_verficated = True
                user.save()
                return Response(data={'details':'User activation has been successfully completed.'},status=status.HTTP_200_OK)
            else:
                return Response(data={'details':'The user has already been confirmed'},status=status.HTTP_400_BAD_REQUEST)
            
        except ExpiredSignatureError:
            return Response({'details':'token is Expired'})
        
        except ExpiredSignatureError:
            return Response({'details':'token is not valid'})
        
# __________________________________________________________

class ResendActivationApiView(generics.GenericAPIView):
    serializer_class = ResendActivationSerializer
    def post(self,request,*args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        
        user = ser_data.validated_data['user']
        token = get_tokens_for_user(user)       
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@gmail.com',to=[user.email])
        EmailThread(email_obj).start()
        
        return Response(data={'details':'User activation resend successfully.'})
# __________________________________________________________

def get_tokens_for_user(user):
    """ get jwt token for user by refresh token """

    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

# def get_tokens_for_user(user):
#     if not user.is_active:
#       raise AuthenticationFailed("User is not active")

#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
# __________________________________________________________

    