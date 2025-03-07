from django.http import HttpResponse, JsonResponse


def index(request):
    return JsonResponse({
        'success': True,
    }, status=200)