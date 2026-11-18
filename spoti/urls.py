from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', musice_list_view, name='musice_list'),
    path('musice/create/', musice_create_view, name='musice_create'),
    path('musice/update/<int:id>/', musice_update_view, name='musice_update'),
    path('musice/delete/<int:id>/', musice_delete_view, name='musice_delete'),
    path('genere/', genere_list_view, name='genere_list'),
    path('genere/create/', genere_create_view, name='genere_create'),
    path('genere/update/<int:id>/', genere_update_view, name='genere_update'),
    path('genere/delete/<int:id>/', genere_delete_view, name='genere_delete'),
    path('alsbome/', alsbome_list_view, name='alsbome_list'),
    path('alsbome/create/', alsbome_create_view, name='alsbome_create'),
    path('alsbome/update/<int:id>/', alsbome_update_view, name='alsbome_update'),
    path('alsbome/delete/<int:id>/', alsbome_delete_view, name='alsbome_delete'),
    path('like/', like_list_view, name='like_list'),
    path('like/create/', like_create_view, name='like_create'),
    path('like/delete/<int:id>/', like_delete_view, name='like_delete')
]