# CobrApp: Automatización de Pagos con OCR y n8n 🚀

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![n8n](https://img.shields.io/badge/n8n-Workflow-red?style=for-the-badge&logo=n8n)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi)

**CobrApp** es una solución de ingeniería diseñada para automatizar la conciliación de pagos digitales (Yape y Plin). Utiliza inteligencia artificial para procesar capturas de pantalla, extraer datos financieros y registrarlos automáticamente en Google Sheets, notificando a los usuarios vía Telegram.

## 🌟 Características principales
- **OCR Multi-Motor**: Procesa imágenes con OpenCV y Tesseract utilizando 3 métodos de filtrado simultáneos para máxima precisión.
- **Detección Inteligente**: Identifica automáticamente montos, nombres, fechas y números de operación de Yape y Plin.
- **Orquestación n8n**: Flujo de trabajo robusto que maneja descargas, validaciones y respuestas automáticas.
- **Despliegue con Docker**: Toda la infraestructura se levanta con un solo comando.

## 🛠️ Arquitectura del Sistema
1. **Telegram Bot**: Interfaz de usuario para recibir capturas.
2. **n8n (Orquestador)**: Gestiona el flujo de datos y la lógica de negocio.
3. **FastAPI (Cerebro OCR)**: API en Python que aplica visión artificial.
4. **Google Sheets**: Base de datos en la nube para el registro histórico.

## 🚀 Instalación y Despliegue

### Requisitos previos
- Docker y Docker Compose instalados.
- Token de Bot de Telegram (@BotFather).
- Credenciales de Service Account de Google Cloud.

### Pasos
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/ELVERANTONY/project-automated-payment-processing-ocr-n8n.git
   ```
2. Levantar los servicios:
   ```bash
   docker-compose up -d --build
   ```
3. Importar el flujo de n8n:
   - Importar el archivo `.json` incluido en la carpeta raíz.
   - Configurar las credenciales de Telegram y Google Sheets.

## 📂 Estructura del Proyecto
```
.
├── cobrapp-ocr-api/     # Código de la API Python (FastAPI + OCR)
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml   # Orquestación de contenedores
├── .gitignore
└── README.md
```

## 👨‍💻 Autor
**Antony Cholan** - *Desarrollador del Proyecto*

---
Desarrollado para el curso de **Desarrollo de Soluciones en la Nube**. 2026.
