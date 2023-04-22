from django.shortcuts import render, redirect
from .models import Testimonial
from .forms import TestimonialForm


def testimonial_list(request):
    testimonials = Testimonial.objects.filter(approved=True)
    context = {'testimonials': testimonials}
    return render(request, 'testimonials/testimonial_list.html', context)


def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('testimonial_list')
    else:
        form = TestimonialForm()
    context = {'form': form}
    return render(request, 'testimonials/add_testimonial.html', context)
