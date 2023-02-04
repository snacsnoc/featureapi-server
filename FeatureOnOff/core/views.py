from django.http import JsonResponse
from django.core.cache import cache

from .models import Feature
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_status(request):
    if request.method == 'GET':
        feature_hash = request.GET.get('feature_hash')
        print(feature_hash)
        feature = Feature.objects.get(feature_hash=feature_hash)
        if feature.state:
            # get code from cache somewhere
            code = cache.get(feature_hash)
            if code is None:
                return JsonResponse({'error': 'Code cache is empty'})
            print("code:",code)
            return JsonResponse({'message': code})
        else:
            return JsonResponse({'error': 'Feature not enabled'})
    return JsonResponse({'error': 'Invalid request method'})
