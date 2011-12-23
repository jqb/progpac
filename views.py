from django.views.generic import FormView, RedirectView
from django.conf import settings
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from progpac import forms
from progpac import h_language
from progpac import models


class Home(RedirectView):
    permanent = False
    
    def get_redirect_url(self, **kwargs):
        level = models.Level.objects.all()[:1].get()
        return reverse('level', kwargs={'level_name': level.name})


class Level(FormView):
    template_name = "level.html"
    form_class = forms.Editor
    initial = { 'text': """x:lslsrssrsls
f:xxx
srsslsf""" }

    @property
    def level(self):
        return models.Level.objects.get(name=self.kwargs.get('level_name'))
    
    def get_context_data(self, *args, **kwargs):
        context = super(Level, self).get_context_data(*args, **kwargs)
        context["level"] = json.dumps(self.level.lines);
        context["all_levels"] = models.Level.objects.all()
        return context
        
    def form_valid(self, form):
        parser = h_language.Parser(
            form.cleaned_data['text'],
            self.level.content
        )

        context = {
            "form": form,
            "error": parser.error,
            "code": parser.code,
        }

        if self.request.POST['submit'] == 'Debug':
            context.update({
                "debug_code": parser.code,
                "debug_ast": parser.ast,
            })

        return self.render_to_response(
            self.get_context_data(**context))
