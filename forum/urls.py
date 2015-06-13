from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.show_index, name='show_index'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^(?P<category_name>\w+)/$', views.show_category, name='show_category'),
    url(r'^(?P<category_name>\w+)/add_topic/$', views.add_topic, name='add_topic'),
    url(r'^(?P<category_name>\w+)/(?P<topic_id>[0-9]+)/$', views.show_topic, name='show_topic'),
    url(r'^(?P<category_name>\w+)/(?P<topic_id>[0-9]+)/vote$', views.vote_for_topic, name='vote_for_topic'),
    url(r'^(?P<category_name>\w+)/(?P<topic_id>[0-9]+)/add_comment/$', views.add_comment_to_topic, name='add_comment'),
]