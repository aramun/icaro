import urlparse

def url_to_dict(url):
   return urlparse.parse_qs(urlparse.urlsplit('?' + url).query)
