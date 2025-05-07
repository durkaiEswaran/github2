from django.contrib import admin
from django.urls import path,include
from . import views
from .views import Home
# from .views import ClubChartView
urlpatterns = [
    # path('', Home.as_view()),
    path('', views.login_view, name='login'),
    path('dashboard/', views.user_list, name='user_list'),
    path('create/', views.user_creates, name='user_create'),
    path('create/user/', views.user_create, name='user_created'),
    path('users/update/<int:pk>/', views.user_update_api, name='user_update_api'),
    path('users/delete/<int:pk>/', views.user_delete_api, name='user_delete_api'),
    path('update/<int:id>/', views.user_update, name='user_update'),
    path('dashboarduser/',views.dashborard_view,name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('imagetotext', views.upload_image, name='upload_image'), 
]
    # path('delete/<int:id>/', views.user_delete, name='user_delete'),