"""Capture browser evidence from the running student-test demo."""
import csv
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
        ids = page.locator("#trip option").evaluate_all("(options) => options.map(option => option.value)")
        ui_rows = []
        # Finish on the short trip for the mobile and download checks.
        for trip in [label for label in ids if label != "00000052"] + ["00000052"]:
            page.select_option("#trip", trip)
            with page.expect_response(lambda response: response.url.endswith("/match"),
                                      timeout=180000) as received:
                page.get_by_role("button", name="Reconstruct route").click()
            response = received.value
            assert response.ok
            payload = response.json()
            page.get_by_text(f"Reconstructed trip {trip}.").wait_for()
            assert page.locator("#accuracy").inner_text() == f"{payload['accuracy'] * 100:.2f}%"
            ui_rows.append((trip, payload["accuracy"], payload["observations"]))
            if trip in {"00000052", "00000056", "00000076"}:
                page.screenshot(path=target / f"ui_{trip}.png", full_page=True)
        with Path("results/ui_smoke.csv").open("w", newline="") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(("trip", "accuracy", "observations"))
            writer.writerows(ui_rows)
        page.set_viewport_size({"width": 390, "height": 844})
        assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
        page.get_by_role("checkbox", name="GPS observations").uncheck()
        with page.expect_download() as download:
            page.get_by_role("button", name="Download prediction").click()
        assert download.value.suggested_filename == "pathsnap-00000052.json"
        page.set_viewport_size({"width": 1100, "height": 680})
        def browser_asset(route):
            with urlopen(route.request.url, timeout=20) as response:
                route.fulfill(body=response.read(), content_type=response.headers.get_content_type())

        # Use the system trust store for public CDN assets in managed browsers.
        for domain in ("cdn.jsdelivr.net", "cdnjs.cloudflare.com", "code.jquery.com"):
            page.route(f"https://{domain}/**", browser_asset)
        for trip in ("00000052", "00000056"):
            map_url = f"{ui}/pathsnap-evidence-map-{trip}.html"
            map_file = f"results/student_trip_map_{trip}.html"
            page.route(map_url, lambda route: route.fulfill(path=map_file, content_type="text/html"))
            page.goto(map_url, timeout=120000)
            page.locator(".leaflet-control-layers").wait_for(timeout=30000)
            page.wait_for_function("document.querySelectorAll('.leaflet-overlay-pane path').length > 10")
            page.screenshot(path=target / f"folium_{trip}.png")
        page.set_viewport_size({"width": 1550, "height": 620})
        receiver = Path("results/receiver.log").read_text().splitlines()
        requests = [line for line in receiver if "PathSnap match " in line or ("POST /match" in line and "200 OK" in line)]
        assert len([line for line in requests if "PathSnap match " in line]) >= 10
        page.set_content(
            '<body style="background:#101916;color:#d8f2e2;padding:26px;font:15px monospace">'
            '<h2 style="color:#b9f66a">PathSnap receiving server log</h2><pre>'
            + html.escape("\n".join(requests[:20])) + "</pre></body>")
        page.screenshot(path=target / "api.png")
        browser.close()


if __name__ == "__main__":
    capture(*sys.argv[1:])
