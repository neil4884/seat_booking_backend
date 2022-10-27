import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}


def json2dict(data):
    try:
        return json.loads(data, strict=False) if data else dict()
    except json.decoder.JSONDecodeError:
        return dict()


def api_url(api_path: str):
    return 'http://127.0.0.1:5000/api/' + api_path


def http_get(url: str):
    r = requests.get(url, headers=headers)
    return json2dict(r.text), r.status_code


def http_post(url: str, payload: dict):
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    return json2dict(r.text), r.status_code


def printf(p):
    for e in p:
        print(e)


if __name__ == '__main__':
    printf(http_get(api_url('users/088')))
    printf(http_get(api_url('seats/F1-A08')))
    printf(http_post(api_url('custom/check_out'), payload={'user': '088'}))
    printf(http_post(api_url('custom/book'), payload={'user': '088', 'seat': 'F1-A08', 'caption': 'hi', 'whatsup': 'et'}))
    # printf(http_post(api_url('custom/check_in'), payload={'user': '088'}))
    printf(http_get(api_url('custom/get_occupied_floor1')))

    # r = requests.get('http://demo.api.booking.vtneil.space/')
