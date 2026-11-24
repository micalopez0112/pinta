// Todos los íconos de la app salen de acá (react-icons, set Font Awesome 6),
// así se ven coherentes y cambiar uno es tocar un solo archivo.
import { flushSync } from 'react-dom'
import { createRoot } from 'react-dom/client'
import {
  FaArrowUpRightFromSquare,
  FaCartShopping,
  FaCheck,
  FaChevronDown,
  FaCloud,
  FaCloudBolt,
  FaCloudMoon,
  FaCloudRain,
  FaCloudSun,
  FaLeaf,
  FaMapPin,
  FaMoon,
  FaPalette,
  FaPersonWalking,
  FaSmog,
  FaSnowflake,
  FaSun,
  FaUmbrella,
  FaUmbrellaBeach,
  FaUtensils,
  FaXmark,
} from 'react-icons/fa6'

const CATEGORY_ICONS = {
  playa: FaUmbrellaBeach,
  paseo: FaPersonWalking,
  cultura: FaPalette,
  naturaleza: FaLeaf,
  restaurante: FaUtensils,
  supermercado: FaCartShopping,
}

// Ícono de una categoría (por su slug). Si llega una categoría nueva sin ícono, usa un pin.
export function CategoryIcon({ slug, ...props }) {
  const Icon = CATEGORY_ICONS[slug] ?? FaMapPin
  return <Icon aria-hidden="true" {...props} />
}

// Leaflet arma los pines del mapa con HTML (no con React). Por eso, al cargar la página
// convertimos una sola vez el ícono de cada categoría a su SVG en texto.
// (No usamos react-dom/server: sumaría más de 200 KB al JS solo para esto.)
function toHtml(element) {
  const host = document.createElement('div')
  const root = createRoot(host)
  flushSync(() => root.render(element))
  const html = host.innerHTML
  root.unmount()
  return html
}

const CATEGORY_ICON_HTML = Object.fromEntries(
  [...Object.keys(CATEGORY_ICONS), 'default'].map((slug) => [slug, toHtml(<CategoryIcon slug={slug} />)]),
)

export const categoryIconHtml = (slug) => CATEGORY_ICON_HTML[slug] ?? CATEGORY_ICON_HTML.default

// [de día, de noche]
const WEATHER_ICONS = {
  clear: [FaSun, FaMoon],
  partly: [FaCloudSun, FaCloudMoon],
  cloudy: [FaCloud, FaCloud],
  fog: [FaSmog, FaSmog],
  rain: [FaCloudRain, FaCloudRain],
  storm: [FaCloudBolt, FaCloudBolt],
  snow: [FaSnowflake, FaSnowflake],
}

export function WeatherIcon({ icon, isDay, ...props }) {
  const [day, night] = WEATHER_ICONS[icon] ?? WEATHER_ICONS.cloudy
  const Icon = isDay ? day : night
  return <Icon aria-hidden="true" {...props} />
}

export const IndoorIcon = FaUmbrella
export const ExternalLinkIcon = FaArrowUpRightFromSquare
export const CloseIcon = FaXmark
export const MoonIcon = FaMoon
export const SunIcon = FaSun
export const CheckIcon = FaCheck
export const ChevronDownIcon = FaChevronDown
