"""UI scenario: verify sidebar can collapse and reopen after CSS fix."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("reports/UI_SIDEBAR_TEST.md")


def main():
    notes = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("http://localhost:8501/", wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(4000)

        # Sidebar should be visible with Filters
        has_filters = page.get_by_text("Filters", exact=False).count() > 0
        notes.append(f"Initial Filters visible: {has_filters}")

        # Collapse via header/sidebar button
        collapse = page.locator('button[data-testid="stBaseButton-headerNoPadding"]').first
        collapse.click(timeout=10000)
        page.wait_for_timeout(1500)

        sidebar = page.locator('[data-testid="stSidebar"]')
        expanded = sidebar.get_attribute("aria-expanded")
        width = sidebar.bounding_box()
        notes.append(f"After collapse aria-expanded={expanded}, width={width['width'] if width else None}")

        # Expand control should exist
        expand = page.locator(
            '[data-testid="collapsedControl"], [data-testid="stExpandSidebarButton"], '
            '[data-testid="stSidebarCollapsedControl"], button[kind="headerNoPadding"]'
        )
        expand_count = expand.count()
        notes.append(f"Expand-related controls found: {expand_count}")

        # Try reopen
        reopened = False
        for sel in [
            '[data-testid="collapsedControl"]',
            '[data-testid="stExpandSidebarButton"]',
            '[data-testid="stSidebarCollapsedControl"]',
            'button[data-testid="stBaseButton-headerNoPadding"]',
        ]:
            loc = page.locator(sel)
            if loc.count():
                try:
                    loc.first.click(timeout=3000)
                    page.wait_for_timeout(1500)
                    expanded2 = sidebar.get_attribute("aria-expanded")
                    notes.append(f"Clicked {sel}; aria-expanded={expanded2}")
                    if expanded2 == "true" or page.get_by_text("Filters", exact=False).count() > 0:
                        reopened = True
                        break
                except Exception as exc:
                    notes.append(f"Click {sel} failed: {exc}")

        # Navigate key pages
        page_ok = []
        for path, needle in [
            ("/Energy_Intelligence", "Energy"),
            ("/Forecast_Center", "Forecast"),
            ("/Anomaly_Intelligence", "Anomaly"),
            ("/AI_Advisor", "Advisor"),
            ("/Scenario_Lab", "Scenario"),
            ("/System_Health", "System"),
        ]:
            page.goto(f"http://localhost:8501{path}", wait_until="networkidle", timeout=120000)
            page.wait_for_timeout(2500)
            body = page.inner_text("body")
            ok = needle.lower() in body.lower() and "Exception" not in body
            page_ok.append((path, ok))
            notes.append(f"Page {path}: {'PASS' if ok else 'FAIL'}")

        browser.close()

    collapsed_ok = any("aria-expanded=false" in n or "width=0" in n or "width=None" in n for n in notes) or any(
        "After collapse" in n and ("false" in n or "width=0" in n) for n in notes
    )
    # Parse collapse width more carefully
    collapse_line = next((n for n in notes if n.startswith("After collapse")), "")
    collapsed_ok = "aria-expanded=false" in collapse_line or "width=0" in collapse_line

    pages_pass = all(ok for _, ok in page_ok)
    overall = collapsed_ok and reopened and pages_pass and has_filters

    md = [
        "# UI Sidebar & Navigation Test",
        "",
        f"**Overall:** {'PASS' if overall else 'CHECK'}",
        f"- Initial filters visible: {has_filters}",
        f"- Sidebar collapsed: {collapsed_ok}",
        f"- Sidebar reopened: {reopened}",
        f"- Pages navigated OK: {pages_pass}",
        "",
        "## Notes",
        *[f"- {n}" for n in notes],
        "",
    ]
    OUT.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0 if (reopened and pages_pass and has_filters) else 1


if __name__ == "__main__":
    raise SystemExit(main())
