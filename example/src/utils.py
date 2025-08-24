from __future__ import annotations
import os, sys, subprocess, platform, time
from pathlib import Path
from loguru import logger

def ensure_dir(p: str | Path) -> Path:
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p

def run_cmd(cmd: list[str]):
    logger.info(f"Ejecutando: {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    if proc.returncode != 0:
        logger.error(proc.stderr.strip())
    else:
        logger.debug(proc.stdout.strip())
    return proc.returncode, proc.stdout, proc.stderr

def print_file(path: str | Path, printer: str | None = None):
    """Imprime un archivo PDF en cada SO con herramientas nativas."""
    path = str(Path(path).resolve())
    system = platform.system()
    if system == "Windows":
        # Usa PowerShell para enviar a la impresora por defecto
        ps = [
            "powershell", "-NoProfile", "-Command",
            f'Start-Process -FilePath "{path}" -Verb Print'
        ]
        return run_cmd(ps)
    elif system == "Darwin":
        # macOS
        cmd = ["lpr"]
        if printer:
            cmd += ["-P", printer]
        cmd += [path]
        return run_cmd(cmd)
    else:
        # Linux
        cmd = ["lp"]
        if printer:
            cmd += ["-d", printer]
        cmd += [path]
        return run_cmd(cmd)
