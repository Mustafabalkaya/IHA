from django.urls import path
from . import views
from .rest import get_uavs, get_users, get_uav_models, get_uav_brands, search_uavs, rent_uav, get_rents, get_all_rents


urlpatterns = [
    #Index:
    path('', views.index, name='index'),
    #Giriş / Kayıl Ol:
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    #Logout- Global:
    path('logout/', views.logout_view, name='logout'),
    #Admin:
    #UAV:
    path('create-uav/', views.createUav, name='create-uav'),
    path('edit-uav/<int:uav_id>/', views.editUav, name='edit-uav'),
    path('save-uav/<int:uav_id>/', views.saveUav, name='save-uav'),
    path('delete-uav/<int:uav_id>/', views.deleteUav, name='delete-uav'),
    path('list-uavs/', views.listUavs, name='list-uavs'),
    #User:
    path('create-user/', views.createUser, name='create-user'),
    path('edit-user/<int:user_id>/', views.editUser, name='edit-user'),
    path('delete-user/<int:user_id>/', views.deleteUser, name='delete-user'),
    path('save-user/<int:user_id>/', views.saveUser, name='save-user'),
    path('list-users/', views.listUsers, name='list-users'),

    path('rents/', views.rents, name='rents'),
    #User:
    path('rent-a-uav/', views.rentaUav, name='rent-a-uav'),
    path('my-rents/', views.myRents, name='my-rents'),

    #Rent:
    path('delete-rent/<int:rent_id>/', views.deleteRent, name='delete-rent'),

    #REST API:
    path('rest/getUavs/', get_uavs, name='get_uavs'),
    path('rest/getUsers/', get_users, name='get_users'),
    path('rest/getUavModels/', get_uav_models, name='get_uav_models'),
    path('rest/getUavBrands/', get_uav_brands, name='get_uav_brands'),
    path('rest/searchUavs/', search_uavs, name='search_uavs'),
    path('rest/rentUav/', rent_uav, name='rent_uav'),
    path('rest/getRents/', get_rents, name='get_rents'),
    path('rest/getAllRents/', get_all_rents, name='get_all_rents'),
]