from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard', views.dashboard ,name='dashboard'),
    path('logout',views.logout,name='logout'),
    path('adduser',views.add_user,name='adduser'),
    path('deleteuser/<int:id>',views.delete_user,name='deleteuser'),
    path('update/<int:id>',views.update,name='update'),
    # path('update',views.update,name='update'),
    path('search',views.search)
   

    

   
]
