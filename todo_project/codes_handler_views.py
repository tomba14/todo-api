from django.http import JsonResponse

def custom_404_view():
    return JsonResponse({"error": "Not Found", "status_code": 404}, status=404)

def custom_500_view():
    return JsonResponse({"error": "Server Error", "status_code": 500}, status=500)

def custom_403_view():
    return JsonResponse({"error": "Forbidden", "status_code": 403}, status=403)

def custom_400_view():
    return JsonResponse({"error": "Bad Request", "status_code": 400}, status=400)
