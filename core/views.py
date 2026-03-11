from django.http import JsonResponse
from core.models import Testing
from core.serializers import TestingSerializer

def testing_view(request):
    testing_records = Testing.objects.all()
    serializer = TestingSerializer(testing_records, many=True)
    return JsonResponse(serializer.data, safe=False)
def health_check(request):
    return JsonResponse({'status': 'ok'})