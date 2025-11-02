# properties/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = get_all_properties()
    context = {'properties': properties}
    return render(request, 'properties/property_list.html', context)

@cache_page(60 * 15)  # cache for 15 minutes
def property_list_json(request):
    """API endpoint that returns properties as JSON"""
    properties = get_all_properties()
    data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
        }
        for prop in properties
    ]
    return JsonResponse({'properties': data, 'count': len(data)})
