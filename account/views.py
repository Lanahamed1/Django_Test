from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializer import SingUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string  
from django.core.mail import send_mail
# Create your views here.




@api_view(['POST'])
def register(request):
    data=request.data
    user=SingUpSerializer(data=data)


    if user.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user=User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            password=make_password(data['password']),
            )
            return Response(
                  {'details':'Your account registered susccessfull!'},
                    status=status.HTTP_201_CREATED
                   )

        else:
            return Response(
                 {'erorr':'This email already exists!'},
                    status=status.HTTP_400_BAD_REQUEST
            )  
    

    else:
        return Response(user.errors)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user=UserSerializer(request.user,many=False)
    return Response(user.data)




api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updata_user(request):
    user= request.user
    data=request.data
    
    user.first_name=data['first_name']
    user.last_name=data['last_name']
    user.username=data['username']
    user.email=data['email']


    if data['password']!='':
     user.password=make_password [data['password']] 
    user.save()
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)

def get_current_host(request):
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return '{protocol}://{host}/'.format(protocol=protocol, host=host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=40)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = '{host}api/reset_password/{token}'.format(host=host, token=token)
    body = 'Your password reset link is: {link}'.format(link=link)
    send_mail(
        'Password reset from Test',
        body,
        'Market@gmail.com',
        [data['email']]
    )
    return Response({'details': 'Password reset link sent to {email}'.format(email=data['email'])})