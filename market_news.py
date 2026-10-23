"""Allowlisted RSS feeds with short caching and last-success fallback."""
import html
import re
import threading
import time
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

FEEDS = {
 'https://www.business-standard.com/rss/markets-106.rss',
 'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms',
 'https://economictimes.indiatimes.com/markets/ipos/fpos/rssfeeds/14655708.cms',
 'https://economictimes.indiatimes.com/mf/rssfeeds/837555174.cms',
}
_cache = {}
_lock = threading.Lock()

def safe_url(value):
 return value if urlparse(value or '').scheme in ('https', 'http') else ''

def parse_feed(data):
 root = ET.fromstring(data)
 items = []
 for item in root.findall('./channel/item')[:15]:
  description = item.findtext('description', '')
  image = ''
  for child in item.iter():
   if child.tag.rsplit('}', 1)[-1] in ('thumbnail','content','enclosure'):
    candidate = child.get('url', '')
    if safe_url(candidate):
     image = candidate
     break
  if not image:
   match = re.search(r'<img[^>]+src=[\"\x27]([^\"\x27]+)', description, re.I)
   if match:image = safe_url(html.unescape(match.group(1)))
  link = safe_url(item.findtext('link', ''))
  if not link:continue
  # These values are inserted into existing HTML templates by the client.
  text = lambda value: html.escape(re.sub('<[^>]+>', '', html.unescape(value)), quote=True)
  items.append({'title':text(item.findtext('title','')), 'description':text(description),
   'link':html.escape(link, quote=True), 'pubDate':item.findtext('pubDate',''),
   'thumbnail':html.escape(image, quote=True)})
 if not items:raise ValueError('No usable RSS articles')
 return items

def get_news(feed):
 if feed not in FEEDS:raise ValueError('Unsupported news feed')
 now = time.time()
 with _lock:cached = _cache.get(feed)
 if cached and now-cached[0]<300:return dict(cached[1], stale=False)
 try:
  req=urllib.request.Request(feed,headers={'User-Agent':'Mozilla/5.0 (compatible; MarketInsight/1.0)', 'Accept':'application/rss+xml,application/xml,text/xml'})
  with urllib.request.urlopen(req,timeout=12) as response:
   data=response.read(2_000_001)
  if len(data)>2_000_000:raise ValueError('Feed too large')
  result={'status':'ok','items':parse_feed(data)}
  with _lock:_cache[feed]=(now,result)
  return dict(result,stale=False)
 except Exception:
  if cached and now-cached[0]<86400:return dict(cached[1],stale=True)
  raise
