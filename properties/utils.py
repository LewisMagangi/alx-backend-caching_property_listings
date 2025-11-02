from django.core.cache import cache
from .models import Property
import logging

# Configure a logger
logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all Property objects, using cache if available.
    Cache key: 'all_properties'
    Cache timeout: 3600 seconds (1 hour)
    """
    properties = cache.get('all_properties')
    if properties is None:
        print("Cache miss — fetching properties from database.")
        logger.info("Cache miss — fetching properties from database.")
        properties = list(Property.objects.all())  # convert queryset to list for serialization
        cache.set('all_properties', properties, 3600)
    else:
        print("Cache hit — loading properties from cache.")
        logger.info("Cache hit — loading properties from cache.")
    return properties

def get_redis_cache_metrics():
    """
    Retrieve cache metrics and calculate cache hit ratio.
    Returns a dictionary with hits, misses, and hit ratio.
    
    Note: For local memory cache, Redis-specific metrics are not available.
    This function provides basic cache status information.
    """
    try:
        # Check if we're using Redis or local cache
        from django.conf import settings
        cache_backend = settings.CACHES['default']['BACKEND']
        
        if 'redis' in cache_backend.lower():
            # Redis-specific metrics
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            info = redis_conn.info()
            
            hits = info.get("keyspace_hits", 0)
            misses = info.get("keyspace_misses", 0)
            total = hits + misses
            hit_ratio = (hits / total) if total > 0 else 0
            
            metrics = {
                "backend": "Redis",
                "hits": hits,
                "misses": misses,
                "hit_ratio": round(hit_ratio * 100, 2),  # percentage
            }
        else:
            # For local memory cache, provide basic info
            metrics = {
                "backend": "Local Memory Cache",
                "message": "Detailed metrics not available for local memory cache",
                "cache_active": True,
            }
        
        logger.info(f"Cache Metrics: {metrics}")
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving cache metrics: {e}")
        return {"error": str(e)}
