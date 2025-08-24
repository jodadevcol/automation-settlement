from __future__ import annotations
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from datetime import datetime

from playwright.sync_api import sync_playwright

from utils import ensure_dir, print_file

def run_web_task(cfg: dict):
    """Ejemplo de automatización web con Playwright.
    1) Login
    2) Navegar al módulo de reportes
    3) Exportar a PDF (si el sitio lo permite) o imprimir
    """
    salida = ensure_dir(cfg["OUTPUT_DIR"])
    pdf_path = salida / f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # cambia a False si necesitas ver la UI
        context = browser.new_context()
        page = context.new_page()

        logger.info(f"Navegando a {cfg['URL']}")
        page.goto(cfg["URL"], wait_until="domcontentloaded")

        # === LOGIN (ajusta selectores) ===
        # Ejemplos de selectores robustos: roles, placeholders, test-id.
        page.get_by_placeholder("Email").fill(cfg["USER"])
        page.get_by_placeholder("Password").fill(cfg["PASS"])
        page.get_by_role("button", name="Ingresar").click()

        # Espera a que el dashboard cargue (ajusta esto a tu app)
        page.wait_for_load_state("networkidle")

        # === IR A REPORTES Y EXPORTAR ===
        # Ajusta navegación y selectores a tu app
        page.get_by_role("link", name="Reportes").click()
        page.wait_for_load_state("networkidle")

        # Si tu web soporta exportación directa a PDF, por ejemplo renderizando la página:
        # (Funciona en Chromium; no todos los sitios imprimen bonito)
        try:
            page.wait_for_selector(f"button:has-text('{cfg['REPORT_BUTTON_TEXT']}')", timeout=5000)
            page.click(f"button:has-text('{cfg['REPORT_BUTTON_TEXT']}')")
        except Exception:
            logger.warning("Botón de exportar no encontrado; intentando capturar PDF de la página actual.")
        finally:
            # Captura PDF de la página actual
            page.pdf(path=str(pdf_path))
            logger.success(f"PDF guardado en {pdf_path}")

        # SI QUIERES ENVIAR A IMPRESORA FÍSICA:
        # print_file(pdf_path)  # Descomenta si quieres imprimir

        context.close()
        browser.close()
