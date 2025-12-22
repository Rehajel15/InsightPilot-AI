from django.shortcuts import render

# Create your views here.
def home(request):
    shop_url = request.GET.get('shop')

    return render(request, 'index.html', {'shop_url':shop_url})