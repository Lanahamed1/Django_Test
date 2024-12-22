from django.urls import path
from.import views


urlpatterns=[
path('register/',views.register,name='register'),
path('userinfo/',views.current_user,name='user_info'),
path('userinfo/updata',views.updata_user,name='updata_user'),
path('forgot_password', views.forgot_password, name='forgot_password')

]