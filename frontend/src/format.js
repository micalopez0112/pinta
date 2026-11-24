// price_level: 0 = gratis, 1 a 3 = de más barato a más caro, null = "consultar".
// `t` es la función de traducción (useI18n).
export function priceLabel(level, t) {
  if (level === 0) return t('card.free')
  if (level == null) return t('card.askPrice')
  return '$'.repeat(level)
}

export const directionsUrl = ({ latitude, longitude }) =>
  `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`

export const degrees = (value) => `${Math.round(value)}°`

// "2026-11-23T20:45" -> "20:45"
export const clockTime = (iso) => iso.slice(11, 16)

// Índice UV: escala de la OMS. `level` es una clave de weather.uvLevels.* en los idiomas.
export function uvInfo(uv) {
  if (uv == null) return null
  const value = Math.round(uv)
  const level = value <= 2 ? 'low' : value <= 5 ? 'moderate' : value <= 7 ? 'high' : value <= 10 ? 'veryHigh' : 'extreme'
  return { value, level }
}
