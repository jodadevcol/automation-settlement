from __future__ import annotations
import time, sys, platform
from pathlib import Path
from loguru import logger

from utils import ensure_dir, print_file

def run_desktop_task(cfg: dict):
    """Dos rutas:
    - Windows + pywinauto (selectores de controles, robusto)
    - Fallback PyAutoGUI + OpenCV (búsqueda por imagen, multi‑plataforma)
    """
    salida = ensure_dir(cfg["OUTPUT_DIR"])
    system = platform.system()

    if system == "Windows":
        try:
            from pywinauto import Application, timings
            # Lanzar app
            app = Application(backend="uia").start(cfg["APP_PATH"])
            win = app.window(title_re=cfg["MAIN_WINDOW_TITLE"])
            win.wait("visible", timeout=30)

            # TODO: Ajustar estos pasos a tu app real
            # Ejemplo: navegar menú → Reportes → Generar
            # win.menu_select("Reportes->Diario")  # si la app tiene menús
            # win.child_window(title="Generar", control_type="Button").click_input()

            # Esperar a que aparezca diálogo de "Guardar como..."
            # dlg = app.window(title_re="Guardar.*")
            # dlg.wait("visible", timeout=30)
            # dlg.child_window(auto_id="1001", control_type="Edit").type_keys(str(salida / "reporte.pdf"))
            # dlg.child_window(title="Guardar", control_type="Button").click_input()

            # SUPONIENDO que generó un PDF en salida:
            pdf_path = salida / "reporte_desktop.pdf"
            with open(pdf_path, "wb") as f:
                f.write(b"%PDF-FAKE%")  # placeholder; cambia por tu flujo real
            logger.success(f"PDF generado (placeholder) en {pdf_path}")
            # print_file(pdf_path)

            return
        except Exception as e:
            logger.warning(f"pywinauto falló o no disponible: {e}. Probando PyAutoGUI...")

    # Fallback genérico por imágenes
    import pyautogui as pag
    import cv2  # noqa: F401  # necesario para locateOnScreen con OpenCV
    pag.FAILSAFE = True  # esquina sup. izq. para abortar
    time.sleep(2)
    # TODO: coloca assets/*.png de tus botones
    # x = pag.locateCenterOnScreen('assets/boton_reporte.png', confidence=0.8)
    # if x:
    #     pag.moveTo(x, duration=0.2)
    #     pag.click()
    # else:
    #     logger.error("No encontré boton_reporte.png en pantalla.")
    #     return

    # DEMO: crear un PDF falso
    pdf_path = salida / "reporte_desktop_fallback.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-FAKE%")
    logger.success(f"PDF (placeholder) en {pdf_path}")
