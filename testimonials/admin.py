from django.contrib import admin
from .models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at', 'approved')
    list_filter = ('approved', )
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at', )

    def approve_testimonial(self, request, queryset):
        queryset.update(approved=True)

    approve_testimonial.short_description = 'Approve selected testimonials'


admin.site.register(Testimonial, TestimonialAdmin)
