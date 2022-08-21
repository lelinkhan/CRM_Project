from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),

    path('',views.dashboard, name='dashboard'),

    path('user_page/', views.UserPage, name= 'user_page'),
    path('account/', views.accountSetting, name='account'),
    path('product/',views.product, name='product'),

    path('customer/<str:pk>/',views.customer, name='customer'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.UpdateOrder, name='update_order'),
    path('remove_order/<str:pk>/', views.RemoveOrder, name='remove_order'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "accounts/reset_password.html"), name ='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"), name ='password_reset_done'),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"), name ='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html"), name ='password_reset_complete'),

]