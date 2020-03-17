"""second URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts1/', include('accounts1.urls')),
    # path('', include('django.contrib.auth.urls')),
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

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# anytime you pass the MEDIA_URL pattern"/images/" as url, go into the MEDIA_ROOT
# and look for the file
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.aol.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'leoklems@aol.com'
# EMAIL_HOST_PASSWORD = 'tsctxqnbmbttjcyo'