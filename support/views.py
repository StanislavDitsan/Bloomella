from django.shortcuts import render, redirect
from .forms import SupportTicketForm


def support_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('support_ticket_success')
    else:
        form = SupportTicketForm()

    context = {
        'form': form,
    }
    return render(request, 'support/support_ticket.html', context)


def support_ticket_success(request):
    return render(request, 'support/support_ticket_success.html')
