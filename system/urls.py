"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('users/', views.user_list, name='user_list'),
    path('password/', views.password, name='password'),
    path('profile/', views.profile, name='profile'),
    path('changeprofile/', views.changeprofile, name='changeprofile'),
    path('user/<int:user_id>', views.show_user, name='show_user'),
    path('user/<int:user_id>/promote_to_member/', views.promote_to_member, name='promote_to_member'),
    path('user/<int:user_id>/promote_to_officer/', views.promote_to_officer, name='promote_to_officer'),
    path('user/<int:user_id>/transfer_ownership/', views.transfer_ownership, name='transfer_ownership'),
    path('switch_club/<int:club_id>', views.switch_selected_club, name='switch_club'),
    path('clubs_list/', views.clubs_list, name = 'clubs_list'),
    path('club/<int:club_id>/', views.show_club, name = 'show_club'),
    path('create_club>/', views.create_club, name = 'create_club'),
]
