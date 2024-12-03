from django.http import JsonResponse
import requests

def search(request):
    query = request.GET.get("query", '')
    print("hello")
    try:
        solr_params = {
            "q": query,
            "useParams": "params",
            "wt": "json"
        }
        uri = "http://localhost:8983/solr/episodes/select"
        response = requests.post(uri, params=solr_params, headers={"Content-Type": "application/x-www-form-urlencoded"})
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")

    # Process the query and generate results
    return JsonResponse(response.json()['response']['docs'], safe=False)