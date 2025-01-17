from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('upload_music', views.upload_music, name='upload_music'),
    path('profile/', views.profile, name='profile'),
    path('edit_song/<pk>/', views.edit_song, name='edit_song'),
    path('delete/<pk>/', views.delete, name='delete'),
    path('song/<pk>/like/', views.toggle_like, name='toggle-like'),
    path('song_obj/<pk>/comment/', views.add_comment, name='add-comment'),
    path('search/', views.search, name='search'),
    path('song/<pk>', views.song_detail, name='song_details'),
    path('like/<pk>', views.toggle_like , name='toggle-like'),
    path('song/<pk>/comments/', views.song_comments, name='song_comments'),
    path('liked_songs/', views.liked_songs, name='liked_songs'),
    # path('delete_comment/<pk>', views.delete_comment, name='delete_comment'),

]