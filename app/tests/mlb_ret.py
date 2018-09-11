import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '07a0c018b0ed4d80b0ad540d45144f96',
}

params = urllib.urlencode({
	'format': 'JSON',
	'season': '2017',
})

try:
    conn = httplib.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", "/v3/mlb/stats/JSON/Standings/2018?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
