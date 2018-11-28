from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [

    path('',views.Index, name='index'),

    #/bankaccount/<bankaccount_id>/
    path('bankaccount/<int:bankaccount_id>/', views.Detail, name='bankacc-detail'),

    path('bankaccount/<int:bankaccount_id>/delete/', views.Delete, name='bankacc-delete'),

    path('bankaccount/<int:bankaccount_id>/history/', views.TransactionHistory, name='bankacc-history'),

    path('bankaccount/add/', views.AddBankAccount, name='bankacc-add'),

    path('bankaccount/<int:bankaccount_id>/deposit/',views.Deposit, name='deposit'),

    path('bankaccount/<int:bankaccount_id>/withdraw/',views.Withdraw, name='withdraw'),

    path('bankaccount/<int:bankaccount_id>/transfer/',views.Transfer, name='transfer'),

    path('bankaccount/<int:bankaccount_id>/transfer/<int:tobankaccount_id>/',views.Transfer2, name='transfer2'),

    path('bankaccount/<int:bankaccount_id>/receipt/<int:transactionlog_id>/',views.Receipt, name='receipt'),

    path('bankaccount/<int:bankaccount_id>/favorite',views.FavoriteView, name='favorite'),

    path('bankaccount/<int:bankaccount_id>/favorite/add/', views.AddFavorite, name='favorite-add'),

    path('bankaccount/<int:bankaccount_id>/favorite/<int:favorite_id>/delete', views.DeleteFavorite, name='favorite-delete'),

    path('enterbankacc/',views.EnterBankAcc, name='enterbankacc'),

    path('logout/',views.logout_view, name='logout'),
]