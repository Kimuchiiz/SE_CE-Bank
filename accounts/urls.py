from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
    # /registration/
    path('register/', views.UserFormView.as_view(), name='register'),

    path('login/', views.Login, name='login'),

    path('createbankaccount/', views.BankAccountCreate.as_view(), name='createbankaccount'),

    #path('',include('django.contrib.auth.urls')),

    path('detail/', views.AccDetail, name='acc-detail'),

    path('password/', views.change_password, name='change_password'),
    
    #/accounts/<user_id>/
    #path('<int:user_id>/', views.detail, name='user-detail'),

    # /music/<album_id>/favorite/
    #path('<int:album_id>/favorite/', views.favorite, name='favorite'),
]