from django.http import JsonResponse

def search(request):
    query = request.GET.get("query", '')
    # Process the query and generate results
    results = [f'{query} result {i+1}' for i in range(10)]
    return JsonResponse(results, safe=False)