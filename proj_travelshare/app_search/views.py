# search.views.py
from itertools import chain
from django.views.generic import ListView

from app_user.models import ProfileTraveler, ProfileHost


class SearchView(ListView):
    template_name = 'app_search/view.html'
    paginate_by = 10
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            res = ProfileTraveler.objects.search(query)


            # combine querysets
            # queryset_chain = chain(
            #     blog_results,
            #     lesson_results,
            #     profile_results
            # )
            qs = sorted(res,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return ProfileTraveler.objects.none()  # just an empty queryset as default
