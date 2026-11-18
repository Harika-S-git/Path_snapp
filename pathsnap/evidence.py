"""Capture browser evidence from the running student-test demo."""
import html
import os
from pathlib import Path
import sys
from urllib.request import urlopen

from playwright.sync_api import sync_playwright


def capture(ui, api):
    target = Path("results/figures")
    target.mkdir(exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=os.getenv("PATHSNAP_CHROMIUM"),
            args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1280, "height": 980})
        page.goto(ui + "?api=" + api)
        page.wait_for_function("document.querySelector('#trip').options.length === 10")
        page.select_option("#trip", "00000052")
        with page.expect_response(lambda response: response.url.endswith("/match"), timeout=180000) as received:
            page.get_by_role("button", name="Reconstruct route").click()
        response = received.value
        assert response.ok
        payload = response.json()
        page.get_by_text("Reconstructed trip 00000052.").wait_for()
        assert page.locator("#accuracy").inner_text() == f"{payload['accuracy'] * 100:.2f}%"
        page.screenshot(path=target / "ui.png", full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
        page.get_by_role("checkbox", name="GPS observations").uncheck()
        with page.expect_download() as download:
            page.get_by_role("button", name="Download prediction").click()
        assert download.value.suggested_filename == "pathsnap-00000052.json"
        page.set_viewport_size({"width": 1100, "height": 680})
        map_url = ui + "/pathsnap-evidence-map.html"
        page.route(map_url, lambda route: route.fulfill(
            path="results/student_trip_map.html", content_type="text/html"))

        def browser_asset(route):
            with urlopen(route.request.url, timeout=20) as response:
                route.fulfill(body=response.read(), content_type=response.headers.get_content_type())

        # Use the system trust store for public CDN assets in managed browsers.
        for domain in ("cdn.jsdelivr.net", "cdnjs.cloudflare.com", "code.jquery.com"):
            page.route(f"https://{domain}/**", browser_asset)
        page.goto(map_url, timeout=120000)
        page.locator(".leaflet-control-layers").wait_for(timeout=30000)
        page.wait_for_function("document.querySelectorAll('.leaflet-overlay-pane path').length > 10")
        page.screenshot(path=target / "folium.png")
        page.set_viewport_size({"width": 1350, "height": 590})
        command = "python -m pathsnap.smoke " + api
        transcript = Path("results/api_smoke.txt").read_text()
        page.set_content(
            '<body style="background:#101916;color:#d8f2e2;padding:26px;font:17px monospace">'
            '<h2 style="color:#b9f66a">PathSnap API smoke test</h2><pre>'
            + html.escape("$ " + command + "\n\n" + transcript) + "</pre></body>")
        page.screenshot(path=target / "api.png")
        browser.close()


if __name__ == "__main__":
    capture(*sys.argv[1:])
