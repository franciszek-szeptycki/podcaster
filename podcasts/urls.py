from django.urls import path
from podcasts.views.podcast import (
    PodcastListCreateView,
    PodcastDetailView,
    PodcastBulkAddEpisodesView,
    PodcastBulkAddEpisodesResultView,
)

urlpatterns = [
    path('', PodcastListCreateView.as_view(), name='podcast_list'),
    # path('create/', PodcastCreateView.as_view(), name='podcast_create'),
    path('<int:pk>', PodcastDetailView.as_view(), name='podcast_detail'),
    path('<int:pk>/bulk-add-episodes/', PodcastBulkAddEpisodesView.as_view(), name='bulk_add_episodes'),
    path('<int:pk>/bulk-add-episodes-result/<str:status>', PodcastBulkAddEpisodesResultView.as_view(), name='bulk_add_episodes_result'),
    path('<int:pk>/episode/>', PodcastBulkAddEpisodesResultView.as_view(), name='bulk_add_episodes_result'),
]
