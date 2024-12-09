from django.contrib.sitemaps import Sitemap
from .models import Trip

class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Trip.published.all()

    def lastmod(self, obj):
        return obj.time_update