import json
import socket
import subprocess
import time
import uuid


def _run(command, timeout=45):
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "returncode": completed.returncode,
            "stdout": completed.stdout[:20_000],
            "stderr": completed.stderr[:4_000],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "timeout": True,
            "stdout": (exc.stdout or "")[:20_000] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[:4_000] if isinstance(exc.stderr, str) else "",
        }


def _parse_body(text):
    body = text.split("\n__CURL_META__:", 1)[0].strip()
    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return {"body_prefix": body[:1500]}

    result = {"payload_type": type(payload).__name__}
    if not isinstance(payload, dict):
        return result

    result["keys"] = sorted(payload.keys())
    for key in ("success", "errorCode", "errorMsg", "message", "code"):
        if key in payload:
            result[key] = payload[key]

    data = payload.get("data")
    result["data_type"] = type(data).__name__
    if isinstance(data, list):
        result["data_length"] = len(data)
        result["first_point"] = data[0] if data else None
        result["last_point"] = data[-1] if data else None
    elif isinstance(data, dict):
        result["data_keys"] = sorted(data.keys())
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
                result["series_key"] = key
                result["series_length"] = len(candidate)
                result["first_point"] = candidate[0] if candidate else None
                result["last_point"] = candidate[-1] if candidate else None
                break
    return result


def _probe(base_curl, url):
    result = _run(base_curl + [url])
    result["parsed"] = _parse_body(result.get("stdout", ""))
    return result


def test_steamdt_broad_anonymous_probe():
    epoch_ms = int(time.time() * 1000)
    page_url = "https://steamdt.com/section?type=BROAD"
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/145.0.0.0 Safari/537.36"
    )

    summary = {"dns": {}, "requests": {}}
    for host in ("api.steamdt.com", "steamdt.com", "www.steamdt.com"):
        try:
            summary["dns"][host] = sorted(
                {item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)}
            )
        except Exception as exc:
            summary["dns"][host] = {"error": repr(exc)}

    base_curl = [
        "curl",
        "--ipv4",
        "--http1.1",
        "--connect-timeout",
        "15",
        "--max-time",
        "35",
        "--compressed",
        "--silent",
        "--show-error",
        "--location",
        "--user-agent",
        user_agent,
        "--header",
        "Accept: application/json, text/plain, */*",
        "--header",
        "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
        "--header",
        "access-token: undefined",
        "--header",
        "language: zh_CN",
        "--header",
        "x-app-version: 1.0.0",
        "--header",
        "x-currency: CNY",
        "--header",
        "x-device: 1",
        "--header",
        f"x-device-id: {uuid.uuid4()}",
        "--header",
        f"Referer: {page_url}",
        "--header",
        "Origin: https://steamdt.com",
        "--write-out",
        "\n__CURL_META__:status=%{http_code};remote_ip=%{remote_ip};content_type=%{content_type};redirect=%{redirect_url};time=%{time_total}",
    ]

    urls = {
        "api_v1_empty_max": (
            "https://api.steamdt.com/user/statistics/v1/kline"
            f"?timestamp={epoch_ms}&type=2&maxTime="
        ),
        "api_v1_zero_max": (
            "https://api.steamdt.com/user/statistics/v1/kline"
            f"?timestamp={epoch_ms}&type=2&maxTime=0"
        ),
        "api_v1_no_max": (
            "https://api.steamdt.com/user/statistics/v1/kline"
            f"?timestamp={epoch_ms}&type=2"
        ),
        "www_api_v1_empty_max": (
            "https://www.steamdt.com/api/user/statistics/v1/kline"
            f"?timestamp={epoch_ms}&type=2&maxTime="
        ),
        "www_api_v2_chart": (
            "https://www.steamdt.com/api/user/statistics/v2/chart"
            f"?timestamp={epoch_ms}&type=2&dateType=2&maxTime="
        ),
        "bare_api_v1_empty_max": (
            "https://steamdt.com/api/user/statistics/v1/kline"
            f"?timestamp={epoch_ms}&type=2&maxTime="
        ),
    }

    for name, url in urls.items():
        summary["requests"][name] = _probe(base_curl, url)

    raise AssertionError(
        "STEAMDT_PROBE_RESULT="
        + json.dumps(summary, ensure_ascii=False, separators=(",", ":"))[:30_000]
    )
