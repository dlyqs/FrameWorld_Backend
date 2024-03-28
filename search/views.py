from django.http import JsonResponse
from rest_framework.decorators import api_view
from utils.libvio_spider import fetch_movies_data_from_libvio
from utils.btnull_spider import fetch_btnull_data

@api_view(['GET'])
def search_movies(request):
    keyword = request.GET.get('q', '')
    libvio_data = fetch_movies_data_from_libvio(keyword)
    btnull_data = fetch_btnull_data(keyword)

    results = libvio_data + btnull_data
    # 这里可以添加排序逻辑
    return JsonResponse(results, safe=False)
