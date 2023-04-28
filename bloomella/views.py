from django.shortcuts import render


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)


def handler505(request, exception):
    """ Error Handler 505 - Internal Server Error """
    return render(request, "errors/505.html", status=505)
