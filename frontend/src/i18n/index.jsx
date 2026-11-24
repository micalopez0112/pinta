// Traducciones de la interfaz. Los textos de las actividades, categorías y el clima
// NO están acá: vienen del backend (?lang=) o como claves que se traducen con estos archivos.
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import de from './locales/de'
import en from './locales/en'
import es from './locales/es'
import pt from './locales/pt'

const MESSAGES = { es, en, pt, de }

export const DEFAULT_LANGUAGE = 'es'

// Orden en el que aparecen en el selector. `short` es la sigla que se muestra junto a la bandera.
export const LANGUAGES = [
  { code: 'es', short: 'ES', label: 'Español' },
  { code: 'en', short: 'EN', label: 'English' },
  { code: 'pt', short: 'PT', label: 'Português' },
  { code: 'de', short: 'DE', label: 'Deutsch' },
]

const STORAGE_KEY = 'pinta.lang'
const isSupported = (code) => Object.hasOwn(MESSAGES, code)

// 1) el idioma que la persona eligió antes, 2) el del navegador, 3) español.
function detectLanguage() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (isSupported(saved)) return saved
  } catch {
    // sin acceso a localStorage (modo privado, etc.): seguimos sin recordar la elección
  }
  for (const tag of navigator.languages ?? [navigator.language]) {
    const base = String(tag).slice(0, 2).toLowerCase() // "pt-BR" -> "pt"
    if (isSupported(base)) return base
  }
  return DEFAULT_LANGUAGE
}

// lookup(messages, 'weather.tips.beach') -> messages.weather.tips.beach
const lookup = (messages, key) => key.split('.').reduce((node, part) => node?.[part], messages)

// "Hola {name}" + { name: 'Ana' } -> "Hola Ana"
const interpolate = (text, params) =>
  text.replace(/\{(\w+)\}/g, (match, name) => (name in params ? String(params[name]) : match))

function translate(lang, key, params = {}) {
  // Si falta la clave en este idioma, se usa el español; si falta también, se ve la clave (así se nota).
  let value = lookup(MESSAGES[lang], key) ?? lookup(MESSAGES[DEFAULT_LANGUAGE], key)
  if (value && typeof value === 'object') {
    // Plurales: { one: '{count} plan', other: '{count} planes' }
    value = value[new Intl.PluralRules(lang).select(params.count ?? 0)] ?? value.other
  }
  return typeof value === 'string' ? interpolate(value, params) : key
}

const I18nContext = createContext(null)

export function I18nProvider({ children }) {
  const [lang, setLangState] = useState(detectLanguage)

  const setLang = useCallback((code) => {
    if (!isSupported(code)) return
    setLangState(code)
    try {
      localStorage.setItem(STORAGE_KEY, code)
    } catch {
      // idem: si no se puede guardar, el cambio igual vale para esta visita
    }
  }, [])

  // El idioma de la página, para lectores de pantalla y para que el navegador ofrezca (o no) traducirla.
  useEffect(() => {
    document.documentElement.lang = lang
  }, [lang])

  const value = useMemo(
    () => ({ lang, setLang, t: (key, params) => translate(lang, key, params) }),
    [lang, setLang],
  )

  return <I18nContext value={value}>{children}</I18nContext>
}

export function useI18n() {
  const context = useContext(I18nContext)
  if (!context) throw new Error('useI18n tiene que usarse dentro de <I18nProvider>')
  return context
}
