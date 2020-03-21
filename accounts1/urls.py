from django.urls import path
from django.contrib.auth import views as auth_views
# from django.conf.urls.static import static
# from django.conf import settings

from .views import *
app_name = 'accounts1'
urlpatterns = [
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name='logout'),

    path('',home, name='home'),
    path('account/', accountSettings, name = 'account'),
    path('user/', userPage, name = 'user-page'),
    path('products/', products, name='products'),
    path('customer/<str:pk>/', customer, name='customer'),
    path('create_order/<str:pk>/', createOrder, name='create_order' ),
    path('update_order/<str:pk>/', updateOrder, name='update_order' ),
    path('delete_order/<str:pk>/', deleteOrder, name='delete_order' ),

    path('reset_password/'
         ,auth_views.PasswordResetView.as_view(
            template_name = 'accounts1/registration/password_reset.html',
            email_template_name = 'accounts1/registration/password_reset_email.html',
            subject_template_name= 'accounts1/registration/password_reset_subject.txt',
            ),
            name = 'password_reset' ),
    path('reset/<uidb64>/<token>/'
         ,auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts1/registration/password_reset_confirm.html'),
         name = 'password_reset_confirm'  ),
    # this view will render the success message, letting us know that the
    # reset email has been sent to the entered email adress
    path('reset_password_sent/'
         ,auth_views.PasswordResetDoneView.as_view(template_name = 'accounts1/registration/password_reset_sent.html'),
         name =  'password_reset_done'),
    # the link that will be sent to the email through which the password can be updated

    # the success message for the user to know that password reset was successful
    path('reset_password_complete/'
         ,auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts1/registration/password_reset_done.html'),
         name =  'password_reset_complete'  ),

]