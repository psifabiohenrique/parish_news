# from django.db.models import Q
# from django.shortcuts import redirect
# from django.urls import reverse


class ChurchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            response = self.get_response(request)
            return response

        # Se o usuário estiver autenticado, associe a igreja
        if request.user.is_authenticated:
            try:
                request.church = request.user.church
            except AttributeError:
                # Usuário não tem uma igreja associada
                request.church = None  # Ou defina um valor padrão
        else:
            request.church = None  # Usuário não autenticado

        response = self.get_response(request)
        return response