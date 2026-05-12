# CobrApp: Automatización de Pagos con OCR y n8n 

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![n8n](https://img.shields.io/badge/n8n-Workflow-red?style=for-the-badge&logo=n8n)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi)

**CobrApp** es una solución de ingeniería diseñada para automatizar la conciliación de pagos digitales (Yape y Plin). Utiliza inteligencia artificial para procesar capturas de pantalla, extraer datos financieros y registrarlos automáticamente en Google Sheets, notificando a los usuarios vía Telegram.

## Características principales
- **OCR Multi-Motor**: Procesa imágenes con OpenCV y Tesseract utilizando 3 métodos de filtrado simultáneos para máxima precisión.
- **Detección Inteligente**: Identifica automáticamente montos, nombres, fechas y números de operación de Yape y Plin.
- **Orquestación n8n**: Flujo de trabajo robusto que maneja descargas, validaciones y respuestas automáticas.
- **Despliegue con Docker**: Toda la infraestructura se levanta con un solo comando.

## Arquitectura del Sistema
1. **Telegram Bot**: Interfaz de usuario para recibir capturas.
2. **n8n (Orquestador)**: Gestiona el flujo de datos y la lógica de negocio.
3. **FastAPI (Cerebro OCR)**: API en Python que aplica visión artificial.
4. **Google Sheets**: Base de datos en la nube para el registro histórico.

---

## 🛠️ Requisitos Previos

Antes de empezar, asegúrate de tener instalado lo siguiente:
- **Docker Desktop**: Necesario para correr n8n y la API de OCR.
- **Git**: Para clonar el repositorio localmente.
- **Cuenta de Google Cloud**: Para acceso a APIs de Sheets y Drive.
- **Telegram**: Para la creación y gestión del Bot.

---

# 🚀 Guía de Despliegue Paso a Paso: CobrApp

Esta documentación está estructurada para seguir el flujo lógico de instalación y configuración del sistema. Síguela en este orden para tener el proyecto funcionando en menos de 10 minutos.

## 📦 Paso 1: Clonación y Preparación de Infraestructura

Lo primero es traer el código a tu máquina local y levantar los servicios base.

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/ELVERANTONY/project-automated-payment-processing-ocr-n8n.git
    cd project-automated-payment-processing-ocr-n8n
    ```

2.  **Levantar el entorno con Docker**:
    Asegúrate de tener Docker abierto y ejecuta:
    ```bash
    docker-compose up -d --build
    ```
    *Esto creará dos contenedores: `n8n` (puerto 5678) y `cobrapp-ocr-api` (puerto 8000).*

3.  **Acceder a n8n**:
    Entra a `http://localhost:5678` y crea tu cuenta de administrador.

---

## 🔄 Paso 2: Importación del Corazón del Sistema

1.  Descarga el archivo `workflow_cobrapp.json` que está en la raíz de este proyecto.
2.  En n8n, ve a **Workflows > Import from File** y selecciona dicho archivo.

---

## 🛠️ Paso 3: Configuración Nodo por Nodo (Guion del Flujo)

A continuación, explicamos qué se necesita configurar en cada etapa del flujo para que el sistema cobre vida:

### 3.1. Disparador: "Cada 3 segundos"
- **Función**: Es el reloj del sistema. No requiere cambios, está configurado para consultar Telegram cada 3 segundos.

### 3.2. Ingesta: "Succión de Datos"
- **Requerimiento**: **Telegram Bot Token**.
- **Acción (Paso a paso en Telegram)**:
    1. Busca a [@BotFather](https://t.me/botfather) y pulsa "Start".
    2. Envía el comando `/newbot`.
    3. **Nombre del Bot**: Escribe el nombre que verán los usuarios (ej: `CobrApp Pagos`).
    4. **Username**: Escribe un nombre único que termine en `_bot` (ej: `academia_fitness_bot`).
    5. **El Tesoro**: BotFather te responderá con un mensaje que contiene el **HTTP API Token** (una cadena larga de números y letras). **Cópialo**.
- **Configuración en n8n**: Sustituye el texto `[TU_BOT_TOKEN]` en la URL del nodo por el Token que acabas de copiar.

### 3.3. Filtros de Control: "IF" y "Es Imagen?"
- **Función**: Estos nodos deciden si el mensaje es nuevo y si contiene una foto.
- **Lógica**: Si el usuario envía texto, el flujo se desvía al nodo **"Pedir Captura"**.

### 3.4. Interacción: "Pedir Captura"
- **Requerimiento**: **Credencial de Telegram**.
- **Acción**: En la pestaña "Credentials" de n8n, crea una de tipo "Telegram API" usando tu mismo Token. Vincúlala a este nodo.

### 3.5. Descarga de Imagen: "Obtener Ruta" y "HTTP Request"
- **Requerimiento**: **Telegram Bot Token**.
- **Acción**: Sustituye `[TU_BOT_TOKEN]` en las URLs de ambos nodos. Esto permite al bot entrar a los servidores de Telegram y bajar la foto temporalmente.

### 3.6. Procesamiento: "Cerebro Python"
- **Función**: Envía la foto a nuestro contenedor de FastAPI (puerto 8000).
- **Detalle**: Aplica los 3 filtros de imagen y extrae los datos mediante Regex.

### 3.7. Persistencia: "Guardar en Excel"
- **Requerimiento**: **Google Cloud Service Account (JSON)**.
- **Acción (Paso a paso en Google Cloud)**:
    1. Entra a [Google Cloud Console](https://console.cloud.google.com/).
    2. **Crear Proyecto**: Si no tienes uno, haz clic en el selector de proyectos (arriba a la izquierda) y dale a **"Proyecto nuevo"**. Ponle un nombre (ej: `CobrApp-Project`).
    3. **Habilitar APIs**: Busca "Google Sheets API" y "Google Drive API" y dale a **Habilitar** a ambas.
    4. **Crear Cuenta**: Ve a "IAM y administración" > "Cuentas de servicio" > "Crear cuenta de servicio". Dale el nombre `bot-pagos` y el rol de **Editor**.
    5. **Descargar JSON**: Entra a la cuenta creada, ve a la pestaña **"Claves"** > "Agregar clave" > "Crear clave nueva" > **JSON**. Se bajará un archivo a tu PC.
    6. **Preparar el Excel**: Crea un Google Sheet nuevo y en la primera fila (encabezados) escribe exactamente estos nombres:
       | Fecha | Hora | Nombre | Monto | Tipo | Operación | Estado |
    7. **Compartir Excel**: Haz clic en "Compartir" y pega el `client_email` que viene dentro del archivo JSON (permiso de Editor).
- **Configuración en n8n**:
    1. Crea una credencial de tipo "Google Sheets Service Account" y sube el archivo JSON.
    2. En el nodo, pega el **ID de tu hoja** (el código largo que sale en la URL de tu Excel).
    3. **⚠️ IMPORTANTE**: Si al seleccionar tu nueva credencial se borran los campos de abajo ("Values to Send"), deberás volver a agregarlos con estos valores exactos:
       - **Fecha**: `{{ $json.fecha }}`
       - **Hora**: `{{ $json.hora }}`
       - **Nombre**: `{{ $json.nombre }}`
       - **Monto**: `{{ $json.monto }}`
       - **Tipo**: `{{ $json.tipo }}`
       - **Operación**: `{{ $json.operacion }}`
       - **Estado**: `{{ $json.valido ? 'Verificado' : 'Revisión Manual' }}`

### 3.8. Cierre: "Confirmar al Cliente"
- **Requerimiento**: **Credencial de Telegram**.
- **Acción**: Vincula la misma credencial que creaste en el paso 3.4. Este nodo enviará el resumen del pago al usuario.

---

## ✅ Paso 4: Activación Final

Una vez configurados los Tokens y el JSON de Google:
1.  Haz clic en el botón **"Execute Workflow"** para probar.
2.  Si todo sale verde, activa el interruptor **"Active"** arriba a la derecha.

---

## 📂 Estructura del Proyecto
```
.
├── cobrapp-ocr-api/     # Código de la API Python (FastAPI + OCR)
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── workflow_cobrapp.json # Flujo de n8n (Importable)
├── docker-compose.yml   # Orquestación de contenedores
├── .gitignore
└── README.md
```

**Autor:** Antony Cholan  
**Curso:** Desarrollo de Soluciones en la Nube - 2026
