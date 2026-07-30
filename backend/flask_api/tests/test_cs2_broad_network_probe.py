import http.cookiejar
import json
import time
import urllib.error
import urllib.request


def _fetch(opener, url, headers):
    request = urllib.request.Request(url, headers=headers)
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, dict(response.headers.items()), response.read(100_000)
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items()), exc.read(100_000)


def _content_type(headers):
    for key, value in headers.items():
        if key.lower() == "content-type":
            return value
    return None


def test_steamdt_broad_anonymous_probe():
    page_url = "https://steamdt.com/section?type=BROAD"
    api_url = (
        "https://api.steamdt.com/user/statistics/v2/chart"
        f"?timestamp={int(time.time() * 1000)}&type=2&dateType=2"
    )
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/145.0.0.0 Safari/537.36"
    )

    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    page_status, page_headers, page_body = _fetch(
        opener,
        page_url,
        {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )

    api_status, api_headers, api_body = _fetch(
        opener,
        api_url,
        {
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": page_url,
            "Origin": "https://steamdt.com",
        },
    )

    summary = {
        "page": {
            "status": page_status,
            "content_type": _content_type(page_headers),
            "body_prefix": page_body[:160].decode("utf-8", "replace"),
        },
        "session_cookie_names": sorted({cookie.name for cookie in cookie_jar}),
        "api": {
            "url_path": "/user/statistics/v2/chart?timestamp=<epoch_ms>&type=2&dateType=2",
            "status": api_status,
            "content_type": _content_type(api_headers),
        },
    }

    try:
        payload = json.loads(api_body.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        summary["api"]["body_prefix"] = api_body[:1000].decode("utf-8", "replace")
    else:
        summary["api"]["payload_type"] = type(payload).__name__
        if isinstance(payload, dict):
            summary["api"]["keys"] = sorted(payload.keys())
            for key in ("success", "errorCode", "errorMsg", "message", "code"):
                if key in payload:
                    summary["api"][key] = payload[key]
            data = payload.get("data")
            summary["api"]["data_type"] = type(data).__name__
            if isinstance(data, list):
                summary["api"]["data_length"] = len(data)
                summary["api"]["first_point"] = data[0] if data else None
                summary["api"]["last_point"] = data[-1] if data else None
            elif isinstance(data, dict):
                summary["api"]["data_keys"] = sorted(data.keys())
                for key in (
                    "historyMarketIndexList",
                    "list",
                    "records",
                    "items",
                    "chartData",
                    "series",
                ):
                    candidate = data.get(key)
                    if isinstance(candidate, list):
                        summary["api"]["series_key"] = key
                        summary["api"]["series_length"] = len(candidate)
                        summary["api"]["first_point"] = candidate[0] if candidate else None
                        summary["api"]["last_point"] = candidate[-1] if candidate else None
                        break

    raise AssertionError(
        "STEAMDT_PROBE_RESULT="
        + json.dumps(summary, ensure_ascii=False, separators=(",", ":"))[:8000]
    )
