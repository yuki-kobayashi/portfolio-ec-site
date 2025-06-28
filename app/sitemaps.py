
from django.contrib.sitemaps import Sitemap
from .models import Item
from django.urls import reverse
from django.contrib.sites.models import Site

# Sitemapクラスを継承したカスタムサイトマップクラス
class ItemSitemap(Sitemap):
    changefreq = "weekly" # 週に1回程度の更新を予定
    priority = 0.8 # 画面の重要度(最大 1.0)

    # sitemapに載せるアイテム(URL)のリストを返す
    def items(self):
        return Item.objects.all()

    # sitemap.xmlに書かれる各URLを生成
    def location(self, obj):
        return reverse('product', args=[obj.slug])
    
    def get_urls(self, site=None, **kwargs):
        if site is None:
            # ドメインを指定
            site = Site(domain="portfolio-ec-site.onrender.com", name="portfolio-ec-site")
        return super().get_urls(site=site, **kwargs)