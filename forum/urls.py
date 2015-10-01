from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.show_index, name='show_index'),
    url(r'^add_category$', views.add_category, name='add_category'),
    url(r'^(?:(?P<category_name>\w+)/)?start_topic/$', views.start_topic, name='start_topic'),
    url(r'^(?P<category_name>\w+)/$', views.show_category, name='show_category'),
    url(r'^(?P<category_name>\w+)/(?P<topic_id>[0-9]+)/$', views.show_or_comment_topic, name='show_or_comment_topic'),
    url(r'^(?P<category_name>\w+)/(?P<topic_id>[0-9]+)/vote$', views.vote_for_topic, name='vote_for_topic'),
    url(r'^upload_image$', views.upload_image, name='upload_image'),
    url(r'^(?P<category_name>\w+)/(?P<topic_id>[0-9]+)/(?P<comment_id>[0-9]+)/vote$',
        views.vote_for_comment, name='vote_for_comment'
    ),
]
