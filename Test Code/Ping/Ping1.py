import requests
from Ping1_resc import ForcedIPHTTPSAdapter

# for k in range(0, 100):
#     # r = requests.get('https://www.google.com', stream=True)
#     r = requests.get('http://104.160.131.3', headers={'host': 'www.example.com'})
#     # grab the IP while you can, before you consume the body!!!!!!!!
#     # print r.raw._fp.fp._sock.getpeername()
#     # consume the body, which calls the read(), after that fileno is no longer available.
#     # print r.content
#     print r.elapsed.total_seconds()

session = requests.Session()
session.mount("https://example.com", ForcedIPHTTPSAdapter(dest_ip='104.160.131.3'))
response = session.get('', headers={'Host': 'example.com'}, verify=False)
