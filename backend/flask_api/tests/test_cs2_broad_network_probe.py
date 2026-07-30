import json
import shutil
import socket
import subprocess
import time


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
            "stdout": completed.stdout[:12_000],
            "stderr": completed.stderr[:4_000],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "timeout": True,
            "stdout": (exc.stdout or "")[:12_000] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[:4_000] if isinstance(exc.stderr, str) else "",
        }


def _parse_body(text):
    body = text.split("\n__CURL_META__:", 1)[0].strip()
    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return {"body_prefix": body[:1200]}

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


def test_steamdt_broad_anonymous_probe():
    epoch_ms = int(time.time() * 1000)
    page_url = "https://steamdt.com/section?type=BROAD"
    api_url = (
        "https://api.steamdt.com/user/statistics/v2/chart"
        f"?timestamp={epoch_ms}&type=2&dateType=2"
    )
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/145.0.0.0 Safari/537.36"
    )

    summary = {"dns": {}, "curl": {}, "browser": {}}
    for host in ("api.steamdt.com", "steamdt.com"):
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
        f"Referer: {page_url}",
        "--header",
        "Origin: https://steamdt.com",
        "--write-out",
        "\n__CURL_META__:status=%{http_code};remote_ip=%{remote_ip};content_type=%{content_type};time=%{time_total}",
    ]

    direct = _run(base_curl + [api_url])
    direct["parsed"] = _parse_body(direct.get("stdout", ""))
    summary["curl"]["api_direct"] = direct

    plain_http_url = api_url.replace("https://", "http://", 1)
    plain = _run(base_curl + [plain_http_url])
    plain["parsed"] = _parse_body(plain.get("stdout", ""))
    summary["curl"]["api_http_redirect"] = plain

    page = _run(
        [
            "curl",
            "--ipv4",
            "--http1.1",
            "--connect-timeout",
            "10",
            "--max-time",
            "20",
            "--silent",
            "--show-error",
            "--location",
            "--user-agent",
            user_agent,
            "--write-out",
            "\n__CURL_META__:status=%{http_code};remote_ip=%{remote_ip};content_type=%{content_type};time=%{time_total}",
            page_url,
        ],
        timeout=30,
    )
    page["body_prefix"] = page.get("stdout", "")[:500]
    page.pop("stdout", None)
    summary["curl"]["page"] = page

    chrome = next(
        (
            path
            for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
            if (path := shutil.which(name))
        ),
        None,
    )
    summary["browser"]["executable"] = chrome
    if chrome:
        browser = _run(
            [
                chrome,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--dump-dom",
                api_url,
            ],
            timeout=50,
        )
        browser["parsed"] = _parse_body(browser.get("stdout", ""))
        summary["browser"]["api_direct"] = browser

    raise AssertionError(
        "STEAMDT_PROBE_RESULT="
        + json.dumps(summary, ensure_ascii=False, separators=(",", ":"))[:20_000]
    )
