from django.http import HttpResponse

def home(request):
    return HttpResponse("🎉 Hey there! 🎉", content_type='text/plain; charset=utf-8')