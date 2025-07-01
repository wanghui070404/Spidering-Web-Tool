import scrapy
from urllib.parse import urlparse, urljoin
import re

class Spidering(scrapy.Spider):
    name = "myspider"
    allowed_domains = []
    start_urls = []
    visited = set()

    def __init__(self, start_url=None, *args, **kwargs):
        super(Spidering, self).__init__(*args, **kwargs)
        if start_url:
            self.start_urls = [start_url]
            domain = urlparse(start_url).netloc
            self.allowed_domains = [domain]
        self.sensitive_keywords = ["admin", "login", "config", "cpanel", "dashboard", "manage", "secure"]

    def is_valid_url(self, url):
        # Loại bỏ link mailto:, tel:, fragment
        return url and not url.startswith(("mailto:", "tel:")) and not url.startswith("#")

    def parse(self, response):
        current_url = response.url.lower()
        parsed_domain = urlparse(current_url).netloc

        # Tránh crawl lặp
        if current_url in self.visited:
            return
        self.visited.add(current_url)

        # Phát hiện URL nhạy cảm
        sensitive = any(keyword in current_url for keyword in self.sensitive_keywords)
        if sensitive:
            self.logger.warning(f"[!] Sensitive URL found: {current_url}")

        # Trích xuất thông tin
        title = response.css("title::text").get()
        forms = response.css("form").getall()
        scripts = response.css("script::attr(src)").getall()
        images = response.css("img::attr(src)").getall()
        meta = response.css("meta[name*=description]::attr(content)").get()
        favicon = response.css("link[rel*=icon]::attr(href)").get()

        yield {
            "url": response.url,
            "status": response.status,
            "title": title,
            "meta_description": meta,
            "favicon": urljoin(response.url, favicon) if favicon else None,
            "forms_count": len(forms),
            "scripts": scripts,
            "images": images,
            "sensitive_detected": sensitive,
        }

        # Crawl các link hợp lệ và trong cùng domain
        for href in response.css("a::attr(href)").getall():
            if not self.is_valid_url(href):
                continue

            full_url = response.urljoin(href)
            parsed_href = urlparse(full_url)

            # Bỏ qua nếu khác domain
            if parsed_href.netloc not in self.allowed_domains:
                continue

            yield scrapy.Request(full_url, callback=self.parse)
