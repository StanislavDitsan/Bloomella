from django.shortcuts import render
from testimonials.models import Testimonial

# Create your views here.


def index(request):
    """ A view to return the index page and the testimonials """
    testimonials = Testimonial.objects.all()
    return render(request, 'home/index.html', {'testimonials': testimonials})