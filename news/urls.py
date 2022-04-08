from django.urls import path
from .views import PostsList, PostDetail, Posts_search, PostCreate,  PostDelete, PostUpdate, IndexView
from .views import upgrade_me, subscribe

urlpatterns = [
    path('news/', PostsList.as_view(), name='news'),
    #path('', PostsList.as_view()), не удалил на случай изменений в будущем
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', Posts_search.as_view(), name='Posts_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/create/', PostUpdate.as_view(), name='post_update'),
    path('', IndexView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('subscriptions/', subscribe, name='subscriptions'),
    ]