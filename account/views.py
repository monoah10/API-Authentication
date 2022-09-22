from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserChangePasswordSerialzer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer,SendPasswordRestEmailSerializer, UserRestPasswordSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# generate_tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registraion is successfull'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login is successfull'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_erros':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerialzer(data=request.data , context=({'user':request.user}))
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response({'errors':{'non_field_erros':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)

class SendPasswordRestEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordRestEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Rest Link Sent.Please Check Your Email'},status=status.HTTP_201_CREATED)
        return Response({'errors':{'non_field_erros':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)

class UserRestPasswordView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserRestPasswordSerializer(data=request.data , context=({'uid':uid, 'token':token}))
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully'},status=status.HTTP_201_CREATED)
        return Response({'errors':{'non_field_erros':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        

