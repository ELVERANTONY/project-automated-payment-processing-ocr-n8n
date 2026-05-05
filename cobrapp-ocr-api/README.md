# CobrApp OCR API - Automatización de Pagos

Este es el componente de procesamiento de imágenes para el sistema de automatización de pagos CobrApp. Utiliza FastAPI para servir una API REST y Tesseract para extraer datos de capturas de pantalla de Yape y Plin.

## Requisitos Previos

### 1. Tesseract OCR
Debes instalar Tesseract en tu sistema para que el OCR funcione:

- **macOS**: `brew install tesseract tesseract-lang`
- **Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr tesseract-ocr-spa`
- **Windows**: Descarga el instalador desde [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) e instala el lenguaje español. Asegúrate de agregar la ruta de instalación al PATH de Windows.

## Instalación

1. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para iniciar el servidor:
```bash
uvicorn main:app --reload --port 8000
```

## Uso de la API

### Procesar Imagen
**Endpoint**: `POST /procesar-imagen`
**Form-Data**:
- `file`: Archivo de imagen (JPG, PNG, etc.)

**Ejemplo con cURL**:
```bash
curl -X POST "http://localhost:8000/procesar-imagen" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@captura_yape.jpg"
```

## Integración con n8n

### 1. Nodo HTTP Request
- **Método**: `POST`
- **URL**: `http://tu-ip:8000/procesar-imagen`
- **Body Content Type**: `Form-Data Multipart`
- **Parámetro**: `file` (Binary File de Telegram/WhatsApp)

### 2. Registro en Google Sheets (Nodo Google Sheets: Append Row)
Configura el mapeo de columnas exactamente así:

| Columna | Valor (Expression) |
| :--- | :--- |
| **Fecha** | `{{$json["fecha"]}}` |
| **Hora** | `{{$json["hora"]}}` |
| **Nombre** | `{{$json["nombre"]}}` |
| **Monto** | `{{$json["monto"]}}` |
| **Tipo** | `{{$json["tipo"]}}` |
| **Operación** | `{{$json["operacion"]}}` |
| **Estado** | `Registrado` |
| **Registrado por** | `Bot Automático` |

### 3. Mensaje de Confirmación (Nodo Telegram/WhatsApp)
Usa este formato para una presentación profesional:

> ✅ **Pago registrado**
> 👤 `{{$json["nombre"]}}`
> 💰 S/`{{$json["monto"]}}`
> 📅 `{{$json["fecha"]}}` `{{$json["hora"]}}`
> 📲 `{{$json["tipo"]}}`

## Formato de Respuesta de la API

**Éxito (`valido: true`)**:
```json
{
  "valido": true,
  "monto": "50.00",
  "nombre": "Juan Perez",
  "fecha": "05/05/2026",
  "hora": "18:32",
  "tipo": "Yape",
  "operacion": "123456",
  "mensaje": "Pago detectado correctamente"
}
```

**Fallo (`valido: false`)**:
```json
{
  "valido": false,
  "mensaje": "No se detectó monto en la imagen"
}
```
