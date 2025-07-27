from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import View
import os
import requests
from urllib.parse import urlparse
from django.db import transaction
from django.core.files.base import ContentFile
from django.contrib import messages
from podcasts.models import Podcast, Episode
from podcasts.forms.podcast_form import PodcastForm
from django.views.generic import DeleteView, TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404


class EpisodeDeleteView(DeleteView):
    model = Episode
    context_object_name = 'episode'
    template_name = 'podcasts/episode_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['podcast_pk'] = self.kwargs.get('podcast_pk')
        return context

    def get_success_url(self):
        podcast_pk = self.kwargs.get('podcast_pk')
        return reverse('podcast_detail', kwargs={'pk': podcast_pk})


class ToggleEpisodeListenedView(View):
    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        episode = get_object_or_404(Episode, pk=pk)
        episode.is_listened = not episode.is_listened
        episode.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
