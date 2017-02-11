import http.client
from urllib.parse import urlparse

def checkUrl(url):
    p = urlparse(url)
    conn = http.client.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400

if __name__ == '__main__':
    print(checkUrl('http://www.stackoverflow.com')) # True
    print(checkUrl('http://localhost:9090/stream.mjpg'))