from django.contrib import admin
from .models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at', 'approved')
    list_filter = ('approved', )
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at', )
    actions = ['approve_testimonials']

    def approve_testimonials(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request,
                          f"{len(queryset)} testimonials have been approved.")

    approve_testimonials.short_description = 'Approve selected testimonials'


admin.site.register(Testimonial, TestimonialAdmin)
