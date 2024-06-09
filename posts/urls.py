from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('create/', views.post_create, name="create"),
    path('<slug:slug>/update/', views.post_update, name="update"),
    path('<slug:slug>/delete/', views.post_delete, name="delete"),
    path('<slug:slug>', views.post_detail, name="detail"),
    path('search/', views.post_search, name="search"),
]