// Revisa las traducciones de la interfaz:  npm run check:i18n
//   1. Todos los idiomas tienen exactamente las mismas claves que el español.
//   2. Los {marcadores} de cada texto (por ejemplo {place}) son los mismos en todos los idiomas.
//   3. Cada t('clave') que se usa en el código existe.
//   4. Cada estado del tiempo que puede devolver el backend tiene traducción.
import { readdirSync, readFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import es from '../src/i18n/locales/es.js'
import en from '../src/i18n/locales/en.js'
import pt from '../src/i18n/locales/pt.js'
import de from '../src/i18n/locales/de.js'

const LOCALES = { en, pt, de }
const problems = []

// { a: { b: 'x' } } -> { 'a.b': 'x' }. Los plurales ({ one, other }) cuentan como un solo texto.
function flatten(node, prefix = '', out = {}) {
  for (const [key, value] of Object.entries(node)) {
    const path = prefix ? `${prefix}.${key}` : key
    const isPlural = value && typeof value === 'object' && 'other' in value
    if (value && typeof value === 'object' && !isPlural) flatten(value, path, out)
    else out[path] = value
  }
  return out
}

const placeholders = (value) =>
  [...new Set([...JSON.stringify(value).matchAll(/\{(\w+)\}/g)].map((m) => m[1]))].sort().join(',')

const base = flatten(es)

// 1 y 2
for (const [code, messages] of Object.entries(LOCALES)) {
  const flat = flatten(messages)
  for (const key of Object.keys(base)) {
    if (!(key in flat)) problems.push(`[${code}] falta la clave "${key}"`)
    else if (placeholders(flat[key]) !== placeholders(base[key]))
      problems.push(`[${code}] "${key}" tiene marcadores distintos: {${placeholders(flat[key])}} en vez de {${placeholders(base[key])}}`)
  }
  for (const key of Object.keys(flat)) if (!(key in base)) problems.push(`[${code}] sobra la clave "${key}"`)
}

// 3: claves usadas en el código (las dinámicas, con ${...}, se revisan en el punto 4 y a mano)
function sourceFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name)
    if (entry.isDirectory()) return entry.name === 'locales' ? [] : sourceFiles(path)
    return /\.(jsx?|mjs)$/.test(entry.name) ? [path] : []
  })
}
for (const file of sourceFiles('src')) {
  const text = readFileSync(file, 'utf8')
  for (const match of text.matchAll(/\bt\(\s*'([\w.]+)'/g)) {
    if (!(match[1] in base)) problems.push(`${file}: usa t('${match[1]}') pero esa clave no existe`)
  }
}

// 4: estados del tiempo del backend
const weatherFile = '../backend/app/weather.py'
if (existsSync(weatherFile)) {
  const keys = [...readFileSync(weatherFile, 'utf8').matchAll(/\("(\w+)", "(?:clear|partly|cloudy|fog|rain|storm|snow)"\)/g)].map((m) => m[1])
  for (const key of new Set([...keys, 'unknown'])) {
    if (!(`weather.conditions.${key}` in base)) problems.push(`el backend puede devolver el estado "${key}" y no tiene traducción`)
  }
}

if (problems.length) {
  console.error(`✗ ${problems.length} problema(s) en las traducciones:\n  - ${problems.join('\n  - ')}`)
  process.exit(1)
}
console.log(`✓ Traducciones OK: ${Object.keys(base).length} textos × ${Object.keys(LOCALES).length + 1} idiomas.`)
