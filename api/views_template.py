from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class MapView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, ** kwargs):
        data = super(MapView, self).get_context_data(**kwargs)
        data['maps'] = []
        return data
    template_name = "api/dashboard.html"

