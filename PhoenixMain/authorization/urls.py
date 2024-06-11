from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.authorizationPage),
    re_path('login', views.login),
    re_path('createUser', views.createUser),
    path('tokenTest', views.tokenTest),
    path('verify', views.verify_account),
    # this particular api returns user(id,username,email) object by
    re_path('getUserByToken', views.getUserByToken),
    path('test2tokens', views.only_with_2tokens),
    path('send_em', views.send_email_code),
    # Provide 2 tokens and json with "uid","password", "new_password","username","email" -> updates user
    re_path('updateUser', views.updateUser),
    # Returns json of {"users": [{"uid": 1, "username": "v", "email": "..."}, {..}]}
    re_path('getUserDetails', views.get_all_user_details),

]