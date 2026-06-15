from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_user, name='login'),

    path('register/', views.register, name='register'),

    path('logout/', views.logout_user, name='logout'),

    ########## Admin Dashboard ##########

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('view_destination/', views.view_destination, name='view_destination'),

    path('delete_destination/<int:id>/', views.delete_destination, name='delete_destination'),

    path('add_destination/', views.add_destination, name='add_destination'),

    path('edit_destination/<int:id>/', views.edit_destination, name='edit_destination'),

    path('view_contact_messages/', views.view_contact_messages, name='view_contact_messages'),
    
    path('view_bookings/', views.view_bookings, name='view_bookings'),

    path('view_users/', views.view_users, name='view_users'),

    path('admin_view_packages/', views.admin_view_packages, name='admin_view_packages'),

    path('add_package/', views.add_package, name='add_package'),

    path('delete_package/<int:id>/', views.delete_package, name='delete_package'),

    path('edit_package/<int:id>/', views.edit_package, name='edit_package'),

    path('admin_view_touristplace/', views.admin_view_touristplace, name='admin_view_touristplace'),

    path('admin_add_touristplace/', views.admin_add_touristplace, name='admin_add_touristplace'),

    path('admin_delete_touristplace/<int:id>/', views.admin_delete_touristplace, name='admin_delete_touristplace'),

    path('admin_edit_touristplace/<int:id>/', views.admin_edit_touristplace, name='admin_edit_touristplace'),

    path('admin_view_hotels/', views.admin_view_hotels, name='admin_view_hotels'),

    path('admin_delete_hotel/<int:id>/', views.admin_delete_hotel, name='admin_delete_hotel'),

    path('add_hotel/', views.add_hotel, name='add_hotel'),

    path('edit_hotel/<int:id>/', views.edit_hotel, name='edit_hotel'),

    path('admin_view_restuarant', views.admin_view_restuarant, name='admin_view_restuarant'),

    path('admin_delete_restuarant/<int:id>/', views.admin_delete_restuarant, name="admin_delete_restuarant"),

    path('add_restaurant/',views.add_restaurant,name='add_restaurant'),

    path('edit_restaurant/<int:id>/',views.edit_restaurant,name='edit_restaurant'),
    
    ########## User Dashboard ##########

    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('destination/<int:id>/', views.destination_detail, name='destination_detail'),

    path('place/<int:id>/', views.place_detail, name='place_detail'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('packages/', views.packages, name='packages'),

    path('package-booking/<int:id>/', views.package_booking, name='package_booking'),
]