from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name="profiles"),

    path('login/', views.loginUser, name="login_user"),
    path('logout/', views.logOutUser, name="logout_user"),
    path('register/', views.registerUser, name="register_user"),

    path('editprofile/',views.editProfile,name="edit_profile"),
    path('account/', views.userAccount, name='user_account'),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-skill/',views.createSkill,name="create_skill"),
    path('update-skill/<str:pk>/',views.updateSkill,name="update_skill"),
    path('delete-skill/<str:pk>/',views.deleteSkill,name="delete_skill"),

]
