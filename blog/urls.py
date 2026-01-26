from . import views
from django.urls import path, include

app_name = 'blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('blog/detail/<blog_id>',views.blog_detail,name='blog_detail'),
    path('blog/pub',views.pub_blog,name='pub_blog'),
    path('auth/', include('blogauth.urls')),
    path('blog/comment',views.pub_comment,name='pub_comment'),
    path('search/',views.search,name='search'),
]