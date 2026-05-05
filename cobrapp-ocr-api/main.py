from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import io
import re
from datetime import datetime

app = FastAPI()

def mejorar_imagen_pil(imagen_bytes):
    img = Image.open(io.BytesIO(imagen_bytes))
    img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.5)
    img = img.filter(ImageFilter.SHARPEN)
    return img

def extraer_datos(texto):
    datos = {
        "valido": False,
        "monto": "0.00",
        "nombre": "No identificado",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "hora": datetime.now().strftime("%H:%M"),
        "tipo": "Yape",
        "operacion": "N/A",
        "mensaje": ""
    }

    texto_lower = texto.lower()
    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    texto_limpio = " ".join(lineas).replace(',', '.')

    # 1. Detectar Tipo (Prioridad Plin)
    if "plin" in texto_lower:
        datos["tipo"] = "Plin"
    elif "yape" in texto_lower:
        datos["tipo"] = "Yape"

    # 2. Buscar Monto
    patrones_monto = [
        r"(?:S/|S/\.|S\.|S)\s*(\d+(?:\.\d{2})?)",
        r"(\d{1,4}\.\d{2})",
        r"(?<=exitoso!)\s*S/\s*(\d+)",
        r"S/\s*(\d+)"
    ]
    for patron in patrones_monto:
        match = re.search(patron, texto_limpio, re.IGNORECASE)
        if match:
            val = match.group(1)
            if "." not in val: val = f"{val}.00"
            datos["monto"] = val
            datos["valido"] = True
            break

    # 3. Buscar Nombre (Específico para Plin y Yape)
    # Patrón Plin: "Enviado a: [Nombre]"
    nombre_match = re.search(r"(?:enviado a|para|recibe|a:)\s*:?\s*([A-Za-z\s]+)", texto_limpio, re.IGNORECASE)
    if nombre_match:
        nombre_candidato = nombre_match.group(1).strip()
        # Limpiar palabras basura
        for palabra in ["yape", "plin", "celular", "destino", "comisi"]:
            nombre_candidato = nombre_candidato.split(palabra)[0].strip()
        if len(nombre_candidato) > 3:
            datos["nombre"] = nombre_candidato
    
    # Si no se encontró por patrón, buscar por posición (Yape)
    if datos["nombre"] == "No identificado":
        for i, linea in enumerate(lineas):
            if "yapeaste" in linea.lower() or "pagaste" in linea.lower() or "exitoso" in linea.lower():
                for j in range(1, 4):
                    if i + j < len(lineas):
                        candidato = lineas[i+j]
                        if len(candidato) > 3 and not any(x in candidato.lower() for x in ["s/", "monto", "operación", "fecha"]):
                            datos["nombre"] = candidato
                            break
                break

    # 4. Buscar Operación
    operacion_match = re.search(r"(?:operaci.n|nro|n.mero)\s*:?\s*(\d+)", texto_limpio, re.IGNORECASE)
    if operacion_match:
        datos["operacion"] = operacion_match.group(1)

    return datos

@app.post("/procesar-imagen")
async def procesar_imagen(file: UploadFile = File(...)):
    contents = await file.read()
    
    # OCR Multi-Motor
    image_pil = Image.open(io.BytesIO(contents))
    texto1 = pytesseract.image_to_string(image_pil, lang='spa')
    
    image_mej = mejorar_imagen_pil(contents)
    texto2 = pytesseract.image_to_string(image_mej, lang='spa')
    
    nparr = np.frombuffer(contents, np.uint8)
    img_cv = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    img_cv = cv2.threshold(img_cv, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    texto3 = pytesseract.image_to_string(img_cv, lang='spa')
    
    texto_total = f"{texto1}\n{texto2}\n{texto3}"
    return extraer_datos(texto_total)

@app.get("/")
def read_root():
    return {"status": "CobrApp OCR Multi-App Ready"}
