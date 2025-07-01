import requests, time, logging
from bs4 import BeautifulSoup # de phan tich' html
from urllib.parse import urljoin, urlparse # urljoin de ghep' tha`nh url hoa`n chinh
from queue import Queue # su dung cho BFS

START_URL = "https://quotes.toscrape.com/"
maxpage = 100
SLEEP = 1
skip_extension = {".jpg", ".jpeg", ".png", ".gif", ".css", ".js", ".svg", ".ico"} # bo qua file tinh
domain = urlparse(START_URL).netloc # chi lay' ten mien`
queue = Queue() # hang` doi queue
queue.put(START_URL)
session = requests.Session() # dung` session de tai' su dung ket' noi'
visited = set([START_URL])
session.headers.update({
    "User-Agent": "Minh/1.0 (+contact@gm.uit.edu.vn)"
})

# ham` load trang
def load_page_func(url: str):
    try:
        resp = session.get(url, timeout=5, allow_redirects = True)

        content_type = resp.headers.get("Content-Type", "")

        # neu' khong phai html thi bo qua
        if "text/html" not in content_type:
            print("Skip (Not html): ", url, "->", content_type)
            return None

        return resp.text
    except requests.RequestException as e:
        print("Error: ",e)
    return None

# ham` lay link
def get_link_func(original_url: str, html: str, domain: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    link = [] 
    seen = set() # da duyet qua url nay` chua
    for a in soup.find_all("a",href = True):
        abs_url = urljoin(original_url, a["href"]).split("#")[0].rstrip("/")

        #khac domain thi` bo qua
        if urlparse(abs_url).netloc != domain:
            continue
        #chua file tinh thi` bo qua
        if any(abs_url.lower().endswith(ext) for ext in skip_extension):
            continue        
        if abs_url not in seen:
            seen.add(abs_url)
            link.append(abs_url)
    return link

# test ham`
# html = load_page_func(START_URL)
# for l in get_link_func(START_URL, html):
#     print(l)

# BFS 
while not queue.empty() and len(visited) < maxpage:
    url = queue.get()
    print("-> %s", url)

    html = load_page_func(url)
    if not html:
        continue

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    print(f"{url}\t{title}")

    for link in get_link_func(url, html, domain):
        if link not in visited:
            visited.add(link)
            queue.put(link)

    time.sleep(SLEEP)