from django.http import JsonResponse
from core.models import Testing
from django.shortcuts import get_object_or_404 
from core.serializers import TestingSerializer

def testing_view(request):
    testing_records = Testing.objects.all()
    serializer = TestingSerializer(testing_records, many=True)
    return JsonResponse(serializer.data, safe=False)

def testing_detail_view(request, id):
    testing = get_object_or_404(Testing, id=id)
    serializer = TestingSerializer(testing)
    return JsonResponse(serializer.data)
def health_check(request):
    return JsonResponse({'status': 'ok'})