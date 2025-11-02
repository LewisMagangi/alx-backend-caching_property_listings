from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Retrieve all Property objects, using Redis cache if available.
    Cache key: 'all_properties'
    Cache timeout: 3600 seconds (1 hour)
    """
    properties = cache.get('all_properties')
    if properties is None:
        print("Cache miss — fetching properties from database.")
        properties = list(Property.objects.all())  # convert queryset to list for serialization
        cache.set('all_properties', properties, 3600)
    else:
        print("Cache hit — loading properties from Redis.")
    return properties
