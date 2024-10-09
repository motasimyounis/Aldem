
from django.contrib.sitemaps import Sitemap
from .models import Services

class YourModelSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Services.objects.all()

    
