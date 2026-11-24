# Publicar Pinta gratis

Tres servicios gratuitos, uno por parte del proyecto:

| Parte | Servicio | Para qué |
|---|---|---|
| Base de datos | **Neon** | Postgres |
| API (FastAPI) | **Render** | el backend |
| Web (React) | **Cloudflare Pages** | lo que ve la gente |

Los tres se pueden crear con tu cuenta de GitHub ("Continue with GitHub") y ninguno pide tarjeta. **Hacelo en este orden**, porque cada paso necesita un dato del anterior.

> Los planes gratuitos cambian seguido. Esta guía es de noviembre de 2026: si alguna pantalla se ve distinta, buscá el campo por su nombre.

---

## 1. Subir el código a GitHub

```bash
brew install gh          # una sola vez
gh auth login            # GitHub.com → HTTPS → "Yes" a autenticar git → "Login with a web browser"

cd /Users/micaelalopez/Documents/pinta
git init -b main
git add .
git status               # revisá la lista: unos 63 archivos, y NINGUNO .env, .venv ni node_modules
git commit -m "Primera versión de Pinta"
git remote add origin https://github.com/micalopez0112/pinta.git
git push -u origin main
```

Abrí <https://github.com/micalopez0112/pinta> y comprobá que están las carpetas `backend`, `frontend` y los archivos `README.md` y `DEPLOY.md`.

**Tu email en los commits:** git usa el que tenés configurado (`git config --global user.email`). Si no es el de tu cuenta de GitHub, los commits no quedan vinculados a tu perfil, y si el repo es público ese email se ve en el historial. Podés usar el email privado de GitHub (`ID+usuario@users.noreply.github.com`, en Settings → Emails) con `git config --global user.email "ese-email"`.

---

## 2. Base de datos en Neon

1. Entrá a <https://neon.com> y creá la cuenta (con GitHub).
2. **Create project** → nombre `pinta`. **Región:** `AWS US East (N. Virginia)`. Usá la misma que en Render (paso 4).
3. En el panel del proyecto, botón **Connect**. **Apagá "Connection pooling"** (queremos la conexión directa) y copiá la cadena. Empieza con `postgresql://…`
4. **Guardala como si fuera una contraseña**: no la subas a GitHub ni la pegues en chats. Si se filtra, se cambia desde Neon (Roles → Reset password).

---

## 3. Cargar las actividades en esa base

Desde tu computadora (la base de Neon está vacía y las tablas se crean solas):

```bash
cd /Users/micaelalopez/Documents/pinta/backend
DATABASE_URL='PEGÁ-ACÁ-LA-CADENA-DE-NEON' .venv/bin/python -m app.seed
```

Las **comillas simples** son obligatorias (la cadena tiene símbolos como `&`). Tiene que decir:

```
Listo: 1 destino(s) y 23 actividad(es) cargadas.
```

---

## 4. La API en Render

1. Entrá a <https://render.com> y creá la cuenta (con GitHub).
2. **New +** → **Web Service** → *Build and deploy from a Git repository* → elegí el repo `pinta` (Render te pide permiso para ver tus repos).
3. Completá así:

| Campo | Valor |
|---|---|
| Name | `pinta-api` |
| Region | `Virginia (US East)` (la misma que Neon) |
| Branch | `main` |
| Root Directory | `backend` |
| Runtime / Language | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | **Free** |

4. Más abajo, **Environment Variables** → agregá:
   - `DATABASE_URL` = la cadena de Neon (la misma del paso 2).
5. En **Advanced** → **Health Check Path** = `/api/ping`. **No pongas `/api/health`**: ese consulta la base y la mantendría despierta todo el mes, gastando el cupo gratis de Neon. `/api/ping` no la toca.
6. **Deploy Web Service**. La primera vez tarda unos minutos. Al terminar te da una dirección tipo `https://pinta-api-xxxx.onrender.com`.

**Probala** abriendo en el navegador:
- `https://pinta-api-xxxx.onrender.com/api/ping` → `{"status":"ok"}`
- `https://pinta-api-xxxx.onrender.com/api/destinations/punta-del-este/activities?lang=en` → la lista de actividades en inglés.

Anotá esa dirección: la necesitás en el paso siguiente.

---

## 5. La web en Cloudflare Pages

1. Entrá a <https://dash.cloudflare.com> y creá la cuenta (gratis).
2. **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → elegí el repo `pinta`.
3. Completá así:

| Campo | Valor |
|---|---|
| Project name | `pinta` (la web quedará en `https://pinta.pages.dev`; si el nombre está tomado, Cloudflare agrega un sufijo) |
| Production branch | `main` |
| Framework preset | `None` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Root directory (Advanced) | `frontend` |

4. **Environment variables** → agregá:
   - `VITE_API_URL` = `https://pinta-api-xxxx.onrender.com/api`  ← la dirección de Render **terminada en `/api`**, sin barra al final.
5. **Save and Deploy**. Al terminar te muestra la dirección de tu web.

---

## 6. Conectar la web con la API

Por seguridad, la API solo acepta pedidos de las direcciones que le avises. En Render:

1. Tu servicio `pinta-api` → **Environment** → agregá `CORS_ORIGINS` = `https://pinta.pages.dev` (la dirección **exacta** de tu web, sin barra final).
2. **Save**: Render reinicia la API solo.

Abrí tu web. Tendría que mostrar las actividades, el clima y el mapa. Probá el selector de idioma y el botón de modo oscuro.

> **La primera visita después de un rato sin uso es lenta** (hasta ~1 minuto): Render duerme la API gratis a los 15 minutos sin tráfico. La web carga enseguida y muestra el esqueleto de carga hasta que la API despierta.

---

## Si algo falla

| Qué ves | Causa probable | Qué hacer |
|---|---|---|
| La web muestra "No pudimos cargar las actividades" | La API no le responde a la web | Abrí la consola del navegador (F12). Si dice **CORS**, revisá `CORS_ORIGINS` (exacto, `https://`, sin barra final). Si dice **404** o no encuentra el servidor, revisá `VITE_API_URL`. |
| Cambié `VITE_API_URL` y sigue igual | El valor se "graba" al compilar la web | En Cloudflare, **Deployments → Retry deployment** (o hacé un push nuevo). |
| La lista de actividades está vacía | Falta el paso 3 | Corré el comando de carga contra Neon. |
| `/api/ping` anda pero `/api/health` da error | Problema con la base | Revisá `DATABASE_URL` en Render: volvé a copiarla de Neon. |
| El deploy de Render falla por la versión de Python | Render usa una versión distinta de Python | Agregá la variable `PYTHON_VERSION` = `3.13.5` en Render y redeployá. |
| Error de SSL o "password authentication failed" | Cadena de conexión mal copiada | Copiala de nuevo desde Neon (conexión directa) y pegala entera. |
| Tarda ~1 minuto en cargar | Render estaba dormida | Es normal en el plan gratis (ver abajo). |

---

## Que la API no se duerma (opcional)

Un servicio gratuito de monitoreo (por ejemplo UptimeRobot) puede visitar tu API cada 10 minutos o menos y evitar que se duerma. Configuralo con la dirección:

```
https://pinta-api-xxxx.onrender.com/api/ping
```

**Usá `/api/ping`, no `/api/health`**, para no mantener despierta la base de Neon. Dos advertencias: una API despierta todo el mes consume unas 744 de las 750 horas gratis (queda casi sin margen), y no verifiqué que los términos de Render permitan este tipo de chequeo: confirmalo antes.

---

## Límites de lo gratis (noviembre de 2026)

- **Render:** 750 horas por mes, la API se duerme a los 15 minutos sin tráfico. Render dice que el plan gratis no es para producción. **No uses su Postgres gratis**: expira a los 30 días y borra los datos.
- **Neon:** 1 GB de almacenamiento y 100 horas de cómputo por proyecto (según su FAQ). La base de Pinta usa casi nada.
- **Cloudflare Pages:** ancho de banda ilimitado y 500 compilaciones por mes.
- **Open-Meteo (el clima)** es gratis solo para uso no comercial, y los mapas de OpenStreetMap son para poco tráfico. Si Pinta pasa a ser un negocio o crece, hay que cambiar de proveedor de clima y de mapas, y pasar la API a un plan pago.
- Estos planes cambian: antes de depender de ellos, revisá las páginas de precios de cada servicio.

---

## Después: actualizar el sitio

Cada cambio que subas a GitHub se publica solo:

```bash
git add .
git commit -m "Describí el cambio"
git push
```

Render y Cloudflare vuelven a compilar. Si cambiaste las actividades (`seed_data.py` o `seed_translations.py`), **repetí el paso 3** para actualizar la base de Neon.

## Dominio propio (opcional)

En Cloudflare Pages → tu proyecto → **Custom domains**. Después, en Render, agregá la dirección nueva a `CORS_ORIGINS` separada por coma: `https://pinta.pages.dev,https://tudominio.com`.
