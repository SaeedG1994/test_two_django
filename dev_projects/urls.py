from django.urls import path
from . import views
urlpatterns = [
    path('',views.projects,name='projects'),
    path('create-project',views.create_project, name='create-project'),
    path('single-project/<str:pk>/',views.single_project,name='single_project'),
    path('update-project/<str:pk>/',views.update_project, name='update_project'),
    path('delete-project/<str:pk>/',views.delete_project, name='delete_project'),
]