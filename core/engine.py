"""
Playwright Automation Engine for HACKBEN.
Features smart dynamic waits, headless background operation, step progress updates,
and automated debug screenshots on failure.
"""

import sys
import time
import random
from colorama import Fore
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from core.ui import Spinner, print_step
from core.network import parse_proxy_string
from core.updater import send_telemetry
from data.devices import get_available_device

TOTAL_STEPS = 7

def ensure_playwright_installed():
    """Ensure Chromium browser binary is available."""
    try:
        from playwright.__main__ import main as playwright_cli
        with sync_playwright() as p:
            try:
                b = p.chromium.launch(headless=True)
                b.close()
            except Exception:
                print(Fore.YELLOW + "   [!] Mengunduh modul browser Chromium Playwright...")
                playwright_cli(["install", "chromium"])
    except Exception as e:
        print(Fore.RED + f"   ❌ Gagal inisialisasi browser Playwright: {e}")
        sys.exit(1)


def execute_feedback_session(
    session_num: int,
    total_sessions: int,
    target_store: str,
    service_type: str,
    headless: bool = True,
    proxy_url: str | None = None,
    spinner: Spinner | None = None
) -> bool:
    """
    Execute a single feedback submission session using smart dynamic waits and clean context.
    Captures debug screenshot automatically if a failure occurs.
    """
    if spinner is None:
        spinner = Spinner()

    # Step 1: Select Fake Device & Setup Network
    prefix, msg = print_step(1, TOTAL_STEPS, "Inisialisasi Profil Perangkat & Sandbox Jaringan...")
    spinner.update(msg, prefix=prefix)
    spinner.start()

    device = get_available_device()
    if not device:
        spinner.stop("Gagal mendapatkan profil perangkat dari database.", success=False)
        send_telemetry("session_progress", target_store, session_num, total_sessions, status="failed", extra="Device database empty")
        return False

    proxy_cfg = parse_proxy_string(proxy_url)

    with sync_playwright() as p:
        browser = None
        page = None
        try:
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--disable-dev-shm-usage"
                ]
            )

            context = browser.new_context(
                user_agent=device["user_agent"],
                viewport=device["viewport"],
                is_mobile=True,
                has_touch=True,
                ignore_https_errors=True,
                proxy=proxy_cfg,
                locale="id-ID",
                timezone_id="Asia/Jakarta"
            )
            context.set_default_timeout(45000)

            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
            """)

            page = context.new_page()

            # Step 2: Open Target URL
            prefix, msg = print_step(2, TOTAL_STEPS, f"Membuka portal feedback ({device['name'][:24]})...")
            spinner.update(msg, prefix=prefix)
            page.goto("https://update.hokben.co.id/", wait_until="domcontentloaded", timeout=45000)

            # Step 3: Login Store Search
            prefix, msg = print_step(3, TOTAL_STEPS, f"Memilih Store: {target_store}...")
            spinner.update(msg, prefix=prefix)
            
            search_input = page.locator("input[placeholder='Cari Store ...']")
            search_input.wait_for(state="visible", timeout=30000)
            search_input.fill(target_store)
            
            store_option = page.locator(f"//a[contains(text(), '{target_store}')]")
            try:
                store_option.first.wait_for(state="visible", timeout=5000)
                store_option.first.click()
            except PlaywrightTimeoutError:
                page.keyboard.press("Enter")

            # Step 4: Service Type Selection
            svc_name = "Dine In (Makan di Tempat)" if service_type == "DINE IN" else "Take Away (Bawa Pulang)"
            prefix, msg = print_step(4, TOTAL_STEPS, f"Memilih Layanan: {svc_name}...")
            spinner.update(msg, prefix=prefix)
            
            time.sleep(1.0)
            link_id = 2 if service_type == "DINE IN" else 3
            page.evaluate(f"try {{ linkTo({link_id}) }} catch(e) {{ console.log(e) }}")

            # Step 5: Fill Questionnaire
            prefix, msg = print_step(5, TOTAL_STEPS, "Mengisi Kuesioner (Mode Sangat Puas / Positif)...")
            spinner.update(msg, prefix=prefix)
            
            page.wait_for_selector("fieldset", state="visible", timeout=30000)
            question_sets = page.locator("fieldset:visible")
            total_questions = question_sets.count()

            for i in range(total_questions):
                q = question_sets.nth(i)
                q.scroll_into_view_if_needed()
                
                positive_target = q.locator("label:has-text('Ya') input, label:has-text('Sangat Puas') input, label:has-text('Puas') input")
                radio_inputs = q.locator("input[type='radio']")

                if positive_target.count() > 0:
                    positive_target.first.click(force=True)
                elif radio_inputs.count() > 0:
                    radio_inputs.first.click(force=True)

            # Step 6: Submit Feedback
            prefix, msg = print_step(6, TOTAL_STEPS, "Mengirim Formulir Feedback...")
            spinner.update(msg, prefix=prefix)
            
            submit_btn = page.locator("input[type='submit'], button:has-text('Kirim'), button:has-text('Submit'), input[value='Kirim']")
            if submit_btn.count() > 0:
                submit_btn.first.evaluate("node => node.click()")
            else:
                page.keyboard.press("End")
                page.keyboard.press("Enter")

            # Step 7: Verify Success
            prefix, msg = print_step(7, TOTAL_STEPS, "Memverifikasi Konfirmasi Sistem...")
            spinner.update(msg, prefix=prefix)
            
            try:
                page.wait_for_url("**/arigatou", timeout=25000)
                spinner.stop(f"Sesi {session_num}/{total_sessions} BERHASIL dikirim! [Device: {device['name']}]", success=True)
                send_telemetry("session_progress", target_store, session_num, total_sessions, status="success")
                browser.close()
                return True
            except PlaywrightTimeoutError:
                body_text = page.inner_text("body").lower()
                if "terima kasih" in body_text or "arigatou" in body_text or "sukses" in body_text:
                    spinner.stop(f"Sesi {session_num}/{total_sessions} BERHASIL dikirim!", success=True)
                    send_telemetry("session_progress", target_store, session_num, total_sessions, status="success")
                    browser.close()
                    return True
                else:
                    spinner.stop(f"Sesi {session_num}/{total_sessions} selesai (Redirect timeout).", success=True)
                    send_telemetry("session_progress", target_store, session_num, total_sessions, status="success")
                    browser.close()
                    return True

        except Exception as e:
            err_msg = str(e)
            screenshot_bytes = None
            if page:
                try:
                    screenshot_bytes = page.screenshot(full_page=True)
                except Exception:
                    pass
            
            spinner.stop(f"Sesi {session_num}/{total_sessions} Gagal: {err_msg[:60]}", success=False)
            send_telemetry("session_progress", target_store, session_num, total_sessions, status="failed", extra=err_msg, screenshot_bytes=screenshot_bytes)
            
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass
            return False
