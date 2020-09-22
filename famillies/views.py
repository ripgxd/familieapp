from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import redirect

from .helper import generate_family
from .helper import set_age
from .helper import field_is_valid

from .models import Surname
from .models import RelationType
from .models import FamillieList

from dateutil.relativedelta import relativedelta
from datetime import datetime

from geopy.distance import geodesic
from geopy import Point


class IndexView(LoginRequiredMixin, ListView):
    login_url = 'login'
    context_object_name = 'objects'
    paginate_by = 10
    template_name = 'famillies/index.html'

    def get_queryset(self):
        return set_age(FamillieList.objects.all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['relations'] = RelationType.objects.all()
        query = FamillieList.objects.all()
        center = Point(48.9215, 24.70972)
        points = []
        for q in query:
            point = Point(q.point.x, q.point.y)
            if geodesic(center, point).kilometers < 5:
                print(point)
                points.append(point)
        context['points'] = points
        return context


class SearchView(LoginRequiredMixin, ListView):
    login_url = 'login'
    context_object_name = 'objects'
    paginate_by = 10
    template_name = 'famillies/search.html'

    rel = None
    name_query = None
    surname_query = None
    min_age_query = None
    max_age_query = None
    qs = None
    
    def get_queryset(self):
        surnames_queryset = Surname.objects.all()

        self.qs = FamillieList.objects.all()
        self.name_query = self.request.GET.get('name')
        self.surname_query = self.request.GET.get('surname')
        relation_query = self.request.GET.get('rel')
        self.min_age_query = self.request.GET.get('min_age')
        self.max_age_query = self.request.GET.get('max_age')

        if field_is_valid(self.name_query):
            self.qs = self.qs.filter(name__icontains=self.name_query)

        if field_is_valid(self.surname_query):
            surname = surnames_queryset.get(surname__icontains=self.surname_query)
            self.qs = self.qs.filter(surname=surname)

        if field_is_valid(relation_query):
            self.qs = self.qs.filter(relation=relation_query)
            self.rel = RelationType.objects.get(id=relation_query)

        if field_is_valid(self.min_age_query):
            min_date = datetime.today() - relativedelta(years=int(self.min_age_query))
            self.qs = self.qs.filter(date__lte=min_date.date())

        if field_is_valid(self.max_age_query):
            max_date = datetime.today() - relativedelta(years=int(self.max_age_query))
            self.qs = self.qs.filter(date__gte=max_date.date())

        return set_age(self.qs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['relation'] = self.rel
        context['min'] = self.min_age_query
        context['max'] = self.max_age_query
        context['name'] = self.name_query
        context['surname'] = self.surname_query
        context['relations'] = RelationType.objects.all()
        points = []
        for q in self.qs:
            point = Point(q.point.x, q.point.y)
            points.append(point)
        context['points'] = points
        return context


@login_required(login_url='login')
def generate(request):

    generate_family()

    return redirect('index')

