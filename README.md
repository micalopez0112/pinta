# Pinta

Qué hacer en un lugar. La primera versión muestra actividades de **Punta del Este** para el verano, con el clima de hoy y un mapa.

| Parte | Tecnología |
|---|---|
| Frontend | React + Vite, CSS puro (sin librerías de estilos) |
| Backend | FastAPI (Python) + SQLAlchemy |
| Base de datos | PostgreSQL (en Docker) |
| Clima | [Open-Meteo](https://open-meteo.com/) (gratis, sin API key) |
| Mapa | Leaflet + OpenStreetMap |
| Idiomas | Español, English, Português (Brasil) y Deutsch, con selector arriba a la derecha |
| Tema | Modo claro y oscuro: sigue al sistema y se puede cambiar con el botón de la barra superior |

## Cómo levantarlo

Necesitás Docker, Python 3 y Node (probado con Python 3.14 y Node 24). Son tres pasos; el de la base alcanza con hacerlo una vez.

**1. Base de datos** (desde la raíz del proyecto)

```bash
docker compose up -d
```

Queda en `localhost:5434`. Si ese puerto está ocupado: `PINTA_DB_PORT=5439 docker compose up -d` y ajustá `DATABASE_URL` en `backend/.env` (hay un ejemplo en `backend/.env.example`).

**2. Backend**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed          # carga las actividades (se puede repetir sin duplicar)
uvicorn app.main:app --reload
```

Si ya tenías la base de una versión anterior y la API falla con un error de columna, es porque cambió el esquema: corré `python -m app.seed --reset` (borra las tablas y las crea de nuevo).

La API queda en <http://localhost:8000> y su documentación interactiva en <http://localhost:8000/docs>.

**3. Frontend**

```bash
cd frontend
npm install
npm run dev
```

Abrí <http://localhost:5173>. En desarrollo, Vite reenvía `/api` al backend, así que no hace falta configurar nada más.

## Publicarlo gratis

Neon (base) + Render (API) + Netlify (web): la guía paso a paso está en [DEPLOY.md](DEPLOY.md).

## Estructura

```
backend/
  app/
    main.py         app FastAPI, CORS y creación de tablas
    api.py          endpoints
    models.py       tablas: destinations, activities
    schemas.py      forma de las respuestas
    weather.py      clima (Open-Meteo) con caché de 10 minutos
    i18n.py         idiomas de la API (?lang=) y cómo se arma una actividad traducida
    categories.py   categorías, con su nombre en cada idioma
    seed_data.py    las actividades en español (acá se editan y se agregan)
    seed_translations.py   sus traducciones (en, pt, de)
    seed.py         carga todo eso en la base
  tests/            pytest (usa SQLite en memoria, no necesita Postgres)
frontend/
  src/
    components/     Header, Hero, WeatherCard, Filters, ActivityCard, ActivityMap, LanguageSwitcher…
    i18n/           sistema de idiomas y los textos de la interfaz (locales/es.js, en.js, pt.js, de.js)
    icons.jsx       todos los íconos (react-icons, set Font Awesome 6)
    theme.js        modo claro / oscuro (el script de index.html lo fija antes de pintar)
    styles/         un archivo CSS por zona; los colores de los dos temas están en base.css
  scripts/check-i18n.mjs   revisa que no falte ninguna traducción
design/             logo original
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/health` | Estado de la API y de la base |
| GET | `/api/categories` | Categorías para los filtros |
| GET | `/api/destinations` | Destinos disponibles |
| GET | `/api/destinations/{slug}` | Un destino |
| GET | `/api/destinations/{slug}/activities` | Actividades (filtros opcionales: `?category=playa`, `?indoor=true`) |
| GET | `/api/destinations/{slug}/weather` | Clima actual y sugerencia del día |

Las categorías y las actividades aceptan `?lang=es|en|pt|de` (por defecto, `es`; un idioma desconocido también responde en español). El clima no lleva idioma: devuelve claves (`"condition": "overcast"`, `"suggestion": "beach"`) que el frontend traduce.

## Tareas comunes

- **Agregar o cambiar actividades:** editá `backend/app/seed_data.py` (en español) y sus traducciones en `backend/app/seed_translations.py` (mismo `slug`), y corré `python -m app.seed`. Busca por `slug`: actualiza lo existente y suma lo nuevo. No borra nada. Si a una actividad le falta una traducción, esa parte se muestra en español.
- **Cambiar un texto de la interfaz:** están en `frontend/src/i18n/locales/` (un archivo por idioma). Después corré `npm run check:i18n` (desde `frontend/`): avisa si falta una clave en algún idioma o si quedó mal un `{marcador}`.
- **Agregar un idioma** (por ejemplo, italiano `it`): sumá `it` en `backend/app/i18n.py` (`SUPPORTED_LANGUAGES`) y en los nombres de `backend/app/categories.py` y `seed_translations.py`; creá `frontend/src/i18n/locales/it.js` copiando `es.js`, registralo en `frontend/src/i18n/index.jsx` (`MESSAGES` y `LANGUAGES`) y elegí su bandera en `frontend/src/components/LanguageSwitcher.jsx` (`FLAGS`, del paquete `country-flag-icons`).
- **Agregar una categoría:** `backend/app/categories.py` (con su nombre en los 4 idiomas) + su ícono en `frontend/src/icons.jsx` (`CATEGORY_ICONS`) + sus colores en `frontend/src/styles/base.css`: las variables `--X`, `--X-ink` y `--X-fg` (en el tema claro y en el oscuro) y el bloque `[data-category='X']` (buscá `restaurante` como ejemplo). Hoy hay seis: playa, paseo, cultura, naturaleza, restaurante y supermercado.
- **Cambiar los colores de un tema:** todo está como variables en `frontend/src/styles/base.css` (`:root` es el claro, `:root[data-theme='dark']` el oscuro). Los otros `.css` no tienen colores escritos a mano, salvo el blanco sobre violeta y la tarjeta del clima, que son iguales en los dos temas.
- **Correr los tests:** `cd backend && .venv/bin/python -m pytest`
- **Borrar la base y empezar de cero:** `docker compose down -v`

## Cosas para tener en cuenta

- **Contenido a revisar.** Las descripciones, precios y duraciones del seed son una base: verificá horarios y precios antes de publicar. Las coordenadas salen de OpenStreetMap.
- **Restaurantes y supermercados son ejemplos.** Los que están cargados existen y su ubicación sale de OpenStreetMap, pero no llevan horarios ni precios (cambian seguido): confirmalos antes de publicar. La descripción de Zazú Puerto sale de su ficha pública (Rambla Gral. Artigas 652), que no dice qué tipo de cocina tiene. Los supermercados no se marcan como "bajo techo" a propósito: ese filtro es para planes de un día de lluvia.
- **Mapa en modo oscuro.** Los mosaicos de OpenStreetMap son claros, así que en modo oscuro se invierten con un filtro de CSS (`map.css`). Se ve bien, pero si Pinta crece conviene un proveedor de mapas con estilo oscuro propio.
- **Traducciones a revisar.** Las traducciones al inglés, portugués y alemán las escribió Claude: conviene que las lea una persona nativa antes de publicar. El portugués es de Brasil, el alemán usa el trato formal ("Sie") y la bandera del inglés es la del Reino Unido.
- **Idioma inicial.** La web abre en el idioma del navegador de cada persona (si es uno de los cuatro; si no, en español) y recuerda su elección en ese navegador.
- **Open-Meteo gratis es solo para uso no comercial.** Si Pinta pasa a ser un producto comercial, hay que pasar a su plan pago o cambiar de proveedor. Los cambios se hacen en un solo lugar: `backend/app/weather.py`.
- **Los mosaicos del mapa** son los públicos de OpenStreetMap, pensados para poco tráfico. Con más visitas conviene un proveedor propio (MapTiler, Stadia, etc.): se cambia la constante `TILES` en `frontend/src/components/ActivityMap.jsx`.
- **Migraciones.** Hoy las tablas se crean solas al arrancar (`create_all`). Al sumar usuarios y cambiar el esquema habrá que pasar a Alembic.

## Próximos pasos posibles

- Registro e inicio de sesión (usuarios, favoritos, "quiero ir").
- Fotos de las actividades y página de detalle.
- Más destinos (la base ya está pensada para eso: todo cuelga de un `destination`).
- Más actividades bajo techo para los días de lluvia.
- Panel para cargar actividades sin tocar código.
