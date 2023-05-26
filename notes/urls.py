from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('user/',views.user,name='user'),
    path('upload/',views.upload,name='upload'),
    path('edit/<int:pk>/',views.pdfedit,name='edit'), 
    path('delete/<int:pk>/',views.delete,name='delete'), 
    path('uploaddash/',views.uploaddash,name='uploaddash'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('logouts/',views.logouts,name='logouts'),
    path('profile/',views.editprofile,name='profile'),
    path('profilee/',views.profilee,name='profilee'),
    path('not/',views.notifications,name='not'),
    path('search/',views.search, name='search'),  
    path('post/<int:post_id>/add-to-favorites/',views.add_to_favorites, name='add_to_favorites'),
    path('favorites/',views.favorites, name='favorites'),
    path('uploadcourse/',views.upload_course,name='courseupload'),
    path('deletecourse/',views.delete_course,name='deletecourse'),
    path('editcourse/<slug:slug>/',views.edit_course, name='edit_course'),
    path('courselist/',views.course_list,name='course_list'),
    path('course_detail/<slug:slug>/',views.course_detail, name='course_detail'),
    path('coursedash/',views.coursedash,name='coursedash'),
    path('course/<int:course_id>/video/upload/', views.upload_video, name='upload_video'),
    path('course/<int:course_id>/video/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('course/<int:course_id>/video/<int:video_id>/delete/', views.delete_video, name='delete_video'),
    path('course/<int:course_id>/learning/', views.learning_view, name='learning'),
    path('course/<int:course_id>/tags/', views.tags_view, name='tags'),
    path('course/<int:course_id>/prerequisites/', views.prerequisites_view, name='prerequisites'),
    path('course/<int:course_id>/learning/', views.learning_view, name='learning'),
    path('course/<int:course_id>/tags/', views.tags_view, name='tags'),
    path('course/<int:course_id>/videos/', views.videos_view, name='videos'),
    path('course/<int:course_id>/prerequisites/', views.prerequisites_view, name='prerequisites'),

]