from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('profile', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload'),
    path('upload_comments', views.upload_comments, name='upload_comments'),
    path('upload_vedio_file', views.upload_vedio_file, name='upload_vedio_file'),
    path('get_all_comments', views.get_all_comments, name='get_all_comments'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('delete_comment', views.delete_comment, name='delete_comment'),
    path('comments_time', views.comments_time, name='comments_time'),
    path('post_seen', views.post_seen, name='post_seen'),
    path('like_seen', views.like_seen, name='like_seen'),
    path('get_Likes', views.get_Likes, name='get_Likes'),
    path('chat', views.chat, name='chat'),
    path('save_message', views.save_message, name='save_message'),
    path('status_message', views.status_message, name='status_message'),
    path('get_messages', views.get_messages, name='get_messages'),
    path('seen_all_messages', views.seen_all_messages, name='seen_all_messages'),
    path('get_all_messages', views.get_all_messages, name='get_all_messages'),
    path('user_status', views.user_status, name='user_status'),
    path('update_my_status', views.update_my_status, name='update_my_status'),
    path('update_message', views.update_message, name='update_message'),
    path('upload_photos', views.upload_photos, name='upload_photos'),
    path('upload_image_file', views.upload_image_file, name='upload_image_file'),
    path('share_post', views.share_post, name='share_post'),
    path('single_post', views.single_post, name='single_post'),
    path('update_all_comments', views.update_all_comments, name='update_all_comments'),
    path('get_last_message', views.get_last_message, name='get_last_message'),


]
