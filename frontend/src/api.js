// En desarrollo, Vite reenvía /api al backend (ver vite.config.js).
// En producción, si la API vive en otro dominio: VITE_API_URL=https://api.ejemplo.com/api
const BASE = import.meta.env.VITE_API_URL ?? '/api'

// Por ahora la app muestra un solo destino.
export const DESTINATION = 'punta-del-este'

async function get(path, signal) {
  const response = await fetch(`${BASE}${path}`, { signal })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

// `lang` (es, en, pt, de) es el idioma de los textos que devuelve el backend.
export const getDestination = (signal) => get(`/destinations/${DESTINATION}`, signal)
export const getActivities = (lang, signal) => get(`/destinations/${DESTINATION}/activities?lang=${lang}`, signal)
export const getCategories = (lang, signal) => get(`/categories?lang=${lang}`, signal)
// El clima no lleva idioma: llega con claves ("overcast") que el frontend traduce.
export const getWeather = (signal) => get(`/destinations/${DESTINATION}/weather`, signal)
