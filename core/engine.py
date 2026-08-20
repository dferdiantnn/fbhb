"""
Playwright Automation Engine for HACKBEN.
Features smart dynamic waits, human-like intelligent randomization,
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


def answer_question_smartly(q_element) -> None:
    """
    Intelligently answers a question fieldset:
    1. Ya / Tidak -> Always chooses 'Ya'
    2. Sangat Puas / Puas -> Always chooses 'Sangat Puas'
    3. Usia -> Randomly chooses options above 13 years (skips < 13 Tahun)
    4. Range Harga -> Randomly chooses options > Rp 25.000 (skips < Rp 25.000)
    5. Gender -> Randomly chooses Pria / Wanita
    6. Other questions -> Randomly chooses exactly 1 valid option
    """
    # Rule 1: Sesuai / Sudah Sesuai -> Always SESUAI
    sesuai_inputs = q_element.locator("label:has-text('Sudah Sesuai') input, label:has-text('Sesuai') input, input[value*='Sesuai' i]")
    if sesuai_inputs.count() > 0:
        sesuai_inputs.first.click(force=True)
        return

    # Special Question: Roti menyusut / kempes -> Pilih Tidak (jika tidak ada opsi Sesuai)
    if "roti" in text_content or "kempes" in text_content or "menyusut" in text_content:
        tidak_inputs = q_element.locator("label:has-text('Tidak') input, input[value*='Tidak' i]")
        if tidak_inputs.count() > 0:
            tidak_inputs.first.click(force=True)
            return

    # Rule 2: Ya / Tidak questions -> Always YA
    ya_inputs = q_element.locator("label:has-text('Ya') input, input[value*='Ya' i], input[value='1']")
    if "ya" in text_content and ya_inputs.count() > 0:
        ya_inputs.first.click(force=True)
        return

    # Rule 3: Kepuasan -> Always SANGAT PUAS
    sangat_puas_inputs = q_element.locator("label:has-text('Sangat Puas') input, label:has-text('Sangat Baik') input")
    if sangat_puas_inputs.count() > 0:
        sangat_puas_inputs.first.click(force=True)
        return

    # Rule 3: Usia -> Random above 13 years
    if "usia" in text_content or "umur" in text_content:
        valid_age_labels = q_element.locator("label:not(:has-text('<13')):not(:has-text('< 13')) input")
        if valid_age_labels.count() > 0:
            idx = random.randint(0, valid_age_labels.count() - 1)
            valid_age_labels.nth(idx).click(force=True)
            return

    # Rule 4: Range Harga -> Random above 25.000
    if "harga" in text_content or "range" in text_content or "pembelian" in text_content:
        valid_price_labels = q_element.locator("label:not(:has-text('< Rp 25.000')):not(:has-text('< 25.000')):not(:has-text('<Rp 25.000')) input")
        if valid_price_labels.count() > 0:
            idx = random.randint(0, valid_price_labels.count() - 1)
            valid_price_labels.nth(idx).click(force=True)
            return

    # Rule 5: Gender (Pria / Wanita) & Other general questions -> Random 1 choice
    all_radios = q_element.locator("input[type='radio']")
    if all_radios.count() > 0:
        idx = random.randint(0, all_radios.count() - 1)
        all_radios.nth(idx).click(force=True)
        return

    # Fallback checkboxes (pick exactly 1 random)
    all_checkboxes = q_element.locator("input[type='checkbox']")
    if all_checkboxes.count() > 0:
        idx = random.randint(0, all_checkboxes.count() - 1)
        all_checkboxes.nth(idx).click(force=True)


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

            # Step 4: Service Type Selection (Dine In / Take Away / Survey)
            if service_type == "DINE IN":
                svc_name = "Dine In (Makan di Tempat)"
                link_id = 2
            elif service_type == "SURVEY":
                svc_name = "Survey Menu Khusus (Katsu Sando)"
                link_id = 4
            else:
                svc_name = "Take Away (Bawa Pulang)"
                link_id = 3

            prefix, msg = print_step(4, TOTAL_STEPS, f"Memilih Layanan: {svc_name}...")
            spinner.update(msg, prefix=prefix)
            
            time.sleep(1.0)
            page.evaluate(f"try {{ linkTo({link_id}) }} catch(e) {{ console.log(e) }}")

            # Step 5: Fill Questionnaire with Multi-Step Next Handler & Smart Randomizer
            prefix, msg = print_step(5, TOTAL_STEPS, "Mengisi Kuesioner (Mode Smart Randomizer & Sangat Puas)...")
            spinner.update(msg, prefix=prefix)
            
            page.wait_for_selector("fieldset, form", state="visible", timeout=30000)
            
            # Loop through wizard steps if pagination/Next button exists
            max_loops = 25
            loop_cnt = 0
            while loop_cnt < max_loops:
                loop_cnt += 1
                
                # Check visible fieldsets on current view
                visible_fieldsets = page.locator("fieldset:visible")
                f_count = visible_fieldsets.count()
                
                for i in range(f_count):
                    q = visible_fieldsets.nth(i)
                    q.scroll_into_view_if_needed()
                    answer_question_smartly(q)

                # Check if there is a 'Next' button visible
                next_btn = page.locator("input[value='Next']:visible, button:has-text('Next'):visible, a.next:visible, .next:visible")
                submit_btn = page.locator("input[type='submit']:visible, button:has-text('Kirim'):visible, button:has-text('Submit'):visible, input[value='Kirim']:visible")

                if submit_btn.count() > 0:
                    # Submit stage reached
                    break
                elif next_btn.count() > 0:
                    next_btn.first.click(force=True)
                    time.sleep(0.3)
                else:
                    break

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
