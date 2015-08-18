from django.conf.urls import url, include
from snippets import views
from rest_framework import renderers


snippet_list = views.SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_details = views.SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlights = views.SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = views.UserViewSet.as_view({
    'get': 'list'
})

user_detail= views.UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^snippets/$', snippet_list, name = 'snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_details, name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        snippet_highlights, name='snippet-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]