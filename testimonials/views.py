from django.shortcuts import render, redirect
from .models import Testimonial
from .forms import TestimonialForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


@login_required
def unapproved_testimonials(request):
    unapproved_testimonials = Testimonial.objects.filter(approved=False)
    context = {'unapproved_testimonials': unapproved_testimonials}
    return render(request, 'testimonials/unapproved_testimonials.html',
                  context)


@user_passes_test(lambda u: u.is_superuser)
def approve_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, pk=testimonial_id)
    testimonial.approved = True
    testimonial.save()
    messages.success(request, 'Testimonial was successfully approved')
    return redirect('testimonial_list')


@login_required
def testimonial_list(request):
    if request.user.is_superuser:
        testimonials = Testimonial.objects.all()
    else:
        testimonials = Testimonial.objects.filter(approved=True)
    context = {'testimonials': testimonials}
    return render(request, 'testimonials/testimonial_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, pk=testimonial_id)
    testimonial.delete()
    messages.success(request, 'Testimonial was successfully deleted')
    return redirect('testimonial_list')


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
