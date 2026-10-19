import argparse
import ssl
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Disable SSL verification globally for urllib
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# List of popular User-Agent headers for Google, major search engines, AI agents, and social crawlers
USER_AGENTS = [
    # Google Search Crawlers
    (
        "Googlebot (Desktop)",
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
    ),
    (
        "Googlebot (Mobile)",
        (
            "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0"
            " Mobile Safari/537.36 (compatible; Googlebot/2.1;"
            " +http://www.google.com/bot.html)"
        ),
    ),
    (
        "Google InspectionTool",
        (
            "Mozilla/5.0 (compatible; Google-InspectionTool/1.0;"
            " +https://search.google.com/search-console/inspections)"
        ),
    ),
    # AI Crawlers & Scrapers
    (
        "GPTBot (OpenAI Web Crawler)",
        (
            "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible;"
            " GPTBot/1.2; +https://openai.com/gptbot)"
        ),
    ),
    (
        "ChatGPT-User (OpenAI Web Browsing)",
        (
            "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible;"
            " ChatGPT-User/1.0; +https://openai.com/bot)"
        ),
    ),
    (
        "OAI-SearchBot (OpenAI Search)",
        ("Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"),
    ),
    (
        "ClaudeBot (Anthropic)",
        "Mozilla/5.0 (compatible; ClaudeBot/1.0; +https://claude.ai/claudebot)",
    ),
    (
        "PerplexityBot (Perplexity AI)",
        (
            "Mozilla/5.0 (compatible; PerplexityBot/1.0;"
            " +https://perplexity.ai/perplexitybot)"
        ),
    ),
    (
        "Bytespider (ByteDance/TikTok)",
        ("Mozilla/5.0 (compatible; Bytespider; spider-feedback@bytedance.com)"),
    ),
    # Meta / Facebook Crawlers
    (
        "Meta-ExternalAgent (Meta AI/Fetcher)",
        (
            "Mozilla/5.0 (compatible; Meta-ExternalAgent/1.1;"
            " +https://www.facebook.com/externalhit_uatext.php)"
        ),
    ),
    (
        "facebookexternalhit (Meta Link Preview)",
        ("facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"),
    ),
    # Other Search Crawlers
    (
        "Bingbot (Microsoft Bing)",
        ("Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"),
    ),
    (
        "DuckDuckGo-Favicons-Bot",
        "Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +http://duckduckgo.com)",
    ),
    (
        "Applebot (Apple)",
        (
            "Mozilla/5.0 (Device; OS version) AppleWebKit/605.1.15 (KHTML,"
            " like Gecko) Version/13.0 Applebot/0.18"
            " (+http://www.apple.com/go/applebot)"
        ),
    ),
]


def test_user_agents(target_url: str, delay: float = 2.0):
    """Makes HTTP GET requests to `target_url` using different User-Agent strings.

    Paces requests with `delay` seconds between each call.
    """
    print(f"Starting test for URL: {target_url}")
    print(f"Delay between requests: {delay} seconds\n")
    print(f"{'Bot Name':<38} | {'HTTP Status':<12} | {'Response Time'}")
    print("-" * 68)

    for bot_name, ua_string in USER_AGENTS:
        # Build request with custom User-Agent header
        req = Request(
            target_url,
            headers={
                "User-Agent": ua_string,
                "Accept": "*/*",
            },
        )

        start_time = time.time()
        try:
            with urlopen(req, timeout=10, context=ssl_context) as response:
                elapsed = round((time.time() - start_time) * 1000, 2)
                status = response.getcode()
                print(f"{bot_name:<38} | {status:<12} | {elapsed} ms")
        except HTTPError as e:
            elapsed = round((time.time() - start_time) * 1000, 2)
            print(f"{bot_name:<38} | HTTP {e.code:<7} | {elapsed} ms")
        except URLError as e:
            elapsed = round((time.time() - start_time) * 1000, 2)
            print(f"{bot_name:<38} | Failed ({e.reason})")
        except Exception as e:
            print(f"{bot_name:<38} | Error: {e}")

        # Wait `delay` seconds before sending the next request
        time.sleep(delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test web server response to popular Search Engine, AI Crawler, and Meta User-Agents."
    )
    parser.add_argument("url", help="Target URL to test (e.g., https://example.com)")
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between requests in seconds (default: 2.0)",
    )

    args = parser.parse_args()

    # Prepend http:// if schema is missing
    target_url = args.url
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    test_user_agents(target_url, delay=args.delay)
