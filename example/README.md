# Automatizador de reporte diario (Python)

Este proyecto es un *starter kit* para automatizar una tarea diaria que:
1) Abre una aplicación web o de escritorio,
2) Navega/da clics,
3) Exporta o imprime un reporte.

Incluye tres caminos:
- **Web (Playwright)** → estable y rápido si el reporte sale de un sitio web.
- **Windows Desktop (pywinauto)** → fiable si la app es nativa de Windows.
- **Cruzado por imágenes (PyAutoGUI + OpenCV)** → último recurso cuando no hay selectores ni accesibilidad.

---

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`
- Para Playwright: `python -m playwright install`

Copia `.env.example` a `.env` y ajusta tus variables.

---

## Ejecutar una vez (prueba)
```bash
# Modo web
python src/main.py --modo web

# Modo escritorio (Windows con pywinauto) 
python src/main.py --modo desktop
```

## Programar la ejecución diaria
### Opción A) Con este propio script (siempre que deje un proceso activo)
```bash
python src/main.py --modo web --programar
```
El script usará `TIME` de tu `.env` (por ejemplo `07:45`) para correr todos los días.

### Opción B) Programador del SO (recomendado)
- **Windows (Task Scheduler):**
  1. Abrir *Task Scheduler* → *Create Task...*
  2. Trigger: Daily a la hora deseada (ej. 07:45)
  3. Action: `python` con *Arguments*: `src/main.py --modo web`
  4. Start in: la carpeta del proyecto.
  *CLI alternativa:*
  ```bat
  schtasks /Create /SC DAILY /TN "ReporteDiario" /TR "python %cd%\src\main.py --modo web" /ST 07:45
  ```

- **macOS / Linux (cron):**
  ```bash
  crontab -e
  # Todos los días 07:45
  45 7 * * * /usr/bin/python3 /RUTA/automatizador_reporte/src/main.py --modo web >> /RUTA/log.txt 2>&1
  ```

---

## Dónde personalizar
- `src/web_task.py`: pon tus *selectores* (Playwright) y la ruta de guardado del PDF.
- `src/desktop_task.py`: ajusta la lógica para tu app (pywinauto) o usa imágenes (`assets/*.png`) con PyAutoGUI.
- `src/utils.py`: impresión del archivo (Windows/macOS/Linux) y utilidades.

Sugerencias de robustez:
- Esperar por elementos (no `sleep` ciego).
- Retries y timeouts coherentes.
- Logs con evidencias (screenshots si falla).
- No guardes credenciales en el código: usa `.env`.

> **Tip DPI/escala:** si usas PyAutoGUI, desactiva escalado de pantalla o captura imágenes al 100% de zoom para que el *match* sea consistente.
