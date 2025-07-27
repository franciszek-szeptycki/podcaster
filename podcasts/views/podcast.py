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

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.shortcuts import render


class PodcastListCreateView(TemplateView):
    template_name = 'podcasts/podcast_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['podcasts'] = Podcast.objects.all()
        context['form'] = PodcastForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PodcastForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('podcast_list'))
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class PodcastDetailView(DetailView):
    model = Podcast
    context_object_name = 'podcast'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episodes_listened'] = self.object.episodes.filter(is_listened=True)
        context['episodes_not_listened'] = self.object.episodes.filter(is_listened=False)
        return context


class PodcastBulkAddEpisodesView(DetailView):
    model = Podcast
    template_name = 'podcasts/bulk_add_episodes.html'
    context_object_name = 'podcast'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        episodes_text = request.POST.get('episodes_text')

        if not episodes_text:
            messages.error(request, "Brakuje pola 'episodes_text'.")
            return redirect('bulk_add_episodes_result', pk=self.object.pk)

        episode_urls = [line.strip() for line in episodes_text.strip().splitlines() if line.strip()]

        try:
            with transaction.atomic():
                for url in episode_urls:
                    try:
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()

                        path = urlparse(url).path
                        filename = os.path.basename(path)
                        name = os.path.splitext(filename)[0]

                        episode = Episode(
                            podcast=self.object,
                            name=name,
                        )
                        episode.file.save(filename, ContentFile(response.content), save=True)

                    except Exception as e:
                        messages.error(request, f"Błąd przy {url}: {str(e)}")
                        raise

        except Exception:
            return redirect('bulk_add_episodes_result', pk=self.object.pk, status='failure')

        messages.success(request, f"Pomyślnie dodano {len(episode_urls)} odcinków.")
        return redirect('bulk_add_episodes_result', pk=self.object.pk, status='success')


class PodcastBulkAddEpisodesResultView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'pk': kwargs.get('pk'),
        }
        if kwargs.get('status') == 'success':
            return render(request, 'podcasts/bulk_add_episodes_success.html', context)
        return render(request, 'podcasts/bulk_add_episodes_failure.html', context)
