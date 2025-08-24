from __future__ import annotations
import argparse, os, time
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import schedule

from utils import ensure_dir

def cargar_env():
    load_dotenv()
    cfg = {
        "TIME": os.getenv("TIME", "07:45"),
        "URL": os.getenv("URL"),
        "USER": os.getenv("USER"),
        "PASS": os.getenv("PASS"),
        "REPORT_BUTTON_TEXT": os.getenv("REPORT_BUTTON_TEXT", "Exportar"),
        "OUTPUT_DIR": os.getenv("OUTPUT_DIR", "outputs"),
        "APP_PATH": os.getenv("APP_PATH"),
        "MAIN_WINDOW_TITLE": os.getenv("MAIN_WINDOW_TITLE"),
    }
    ensure_dir(cfg["OUTPUT_DIR"])
    return cfg

def job_web(cfg):
    from web_task import run_web_task
    logger.info("Iniciando tarea web...")
    run_web_task(cfg)
    logger.info("Tarea web terminada.")

def job_desktop(cfg):
    from desktop_task import run_desktop_task
    logger.info("Iniciando tarea desktop...")
    run_desktop_task(cfg)
    logger.info("Tarea desktop terminada.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=["web","desktop"], required=True)
    parser.add_argument("--programar", action="store_true", help="Ejecuta diariamente a la hora TIME del .env (mantiene el proceso en primer plano)")
    args = parser.parse_args()

    cfg = cargar_env()

    if args.programar:
        if args.modo == "web":
            schedule.every().day.at(cfg["TIME"]).do(job_web, cfg=cfg)
        else:
            schedule.every().day.at(cfg["TIME"]).do(job_desktop, cfg=cfg)
        logger.info(f"Programado diario a las {cfg['TIME']} (modo={args.modo}). Ctrl+C para salir.")
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        if args.modo == "web":
            job_web(cfg)
        else:
            job_desktop(cfg)

if __name__ == "__main__":
    main()
