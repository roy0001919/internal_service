from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'eform'
urlpatterns = [
    path('tab_coform/', views.tab_coform, name='tab_coform'),
    path('tab_daily/', views.tab_daily, name='tab_daily'),
    path('tab_cashpymt/', views.tab_cashpymt, name='tab_cashpymt'),
    path('tab_search/', views.tab_search, name='tab_search'),
    path('tab_search/daily/', views.daily, name='daily'),
    path('tab_search/mailOrder/', views.mailOrder, name='mailOrder'),
    path('tab_search/cashPymt/', views.cashPymt, name='cashPymt'),
    path('login/', auth_views.LoginView.as_view(template_name='myweb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='myweb/logout.html'), name='logout'),
    path('index/', views.index, name='index'),
]