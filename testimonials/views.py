from django.shortcuts import render, redirect
from .models import Testimonial
from .forms import TestimonialForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def testimonial_list(request):
    approved_testimonials = Testimonial.objects.filter(approved=True)
    context = {'testimonials': approved_testimonials}
    return render(request, 'testimonials/testimonial_list.html', context)


@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.approved = False
            testimonial.save()
            messages.success(
                request,
                'Thank you for your testimonial. It will be available shortly after it is approved by an admin.'
            )
            return redirect('home')
    else:
        form = TestimonialForm()

    context = {'form': form}
    return render(request, 'testimonials/add_testimonial.html', context)
