from django.shortcuts import render
from church.models import Church, Priest


def index(request):
    churches = Church.objects.all()
    priests = Priest.objects.all()

    return render(request, "news/index.html", {"churches": churches, "priests": priests})
