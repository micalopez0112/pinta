import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet.markercluster' // agrega L.markerClusterGroup (agrupa pines cercanos)
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import { directionsUrl, priceLabel } from '../format'
import { useI18n } from '../i18n'
import { CategoryIcon, CloseIcon, ExternalLinkIcon, categoryIconHtml } from '../icons'
import '../styles/map.css'

// Mosaicos de OpenStreetMap: sirven para desarrollo y poco tráfico. Si Pinta crece,
// conviene un proveedor de mapas propio (MapTiler, Stadia, etc.).
const TILES = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
const ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'

// Zoom al que volamos cuando se elige una actividad (a este nivel los pines ya no se agrupan).
const FOCUS_ZOOM = 15
const UNCLUSTER_ZOOM = 14

const safeClass = (value) => String(value).replace(/[^a-z0-9_-]/gi, '')
const escapeHtml = (text) =>
  String(text).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c])

// Pin propio hecho con CSS (evita el problema de los íconos por defecto de Leaflet con bundlers).
// El título va como texto oculto para que los lectores de pantalla nombren el pin.
function pinIcon(activity, active) {
  return L.divIcon({
    className: `pin pin--${safeClass(activity.category)}${active ? ' pin--active' : ''}`,
    html:
      `<span class="pin__body"><span class="pin__icon">${categoryIconHtml(activity.category)}</span></span>` +
      `<span class="sr-only">${escapeHtml(activity.title)}</span>`,
    iconSize: [38, 38],
    iconAnchor: [19, 46],
    tooltipAnchor: [0, -48],
  })
}

// Burbuja con la cantidad de actividades cuando varios pines quedan muy juntos.
function clusterIcon(cluster) {
  return L.divIcon({
    className: 'cluster',
    html: `<span>${cluster.getChildCount()}</span>`,
    iconSize: [44, 44],
  })
}

function fitAll(map, activities) {
  // Con el mapa oculto (tamaño 0) Leaflet no puede calcular el zoom: se reintenta al mostrarse.
  const { x, y } = map.getSize()
  if (activities.length === 0 || x === 0 || y === 0) return
  const bounds = L.latLngBounds(activities.map((a) => [a.latitude, a.longitude]))
  map.fitBounds(bounds, { padding: [48, 48], maxZoom: 13, animate: false })
}

export default function ActivityMap({ center, activities, selected, onSelect, onClear }) {
  const { t } = useI18n()
  const containerRef = useRef(null)
  const mapRef = useRef(null)
  const layerRef = useRef(null)
  const markersRef = useRef(new Map()) // slug -> marker
  const fittedKeyRef = useRef(null) // para qué actividades se encuadró el mapa por última vez

  const selectedSlug = selected?.slug ?? null

  // Últimos valores, para usarlos dentro de callbacks que se crean una sola vez.
  const latest = useRef({})
  latest.current = { activities, selectedSlug, onSelect }

  // 1) Crear el mapa una sola vez.
  useEffect(() => {
    const map = L.map(containerRef.current, { scrollWheelZoom: false }).setView(center, 11)
    L.tileLayer(TILES, { maxZoom: 19, attribution: ATTRIBUTION }).addTo(map)
    layerRef.current = L.markerClusterGroup({
      iconCreateFunction: clusterIcon,
      maxClusterRadius: 44,
      disableClusteringAtZoom: UNCLUSTER_ZOOM,
      showCoverageOnHover: false,
      spiderfyOnMaxZoom: false,
    }).addTo(map)
    mapRef.current = map

    // En celular el mapa puede arrancar oculto (vista "Lista"). Cuando aparece, o cuando
    // cambia el tamaño de la ventana, hay que recalcular tamaño y encuadre.
    const observer = new ResizeObserver(() => {
      const wasHidden = map.getSize().x === 0
      map.invalidateSize()
      if (wasHidden && map.getSize().x > 0) {
        const { activities, selectedSlug } = latest.current
        const marker = markersRef.current.get(selectedSlug)
        if (marker) map.setView(marker.getLatLng(), Math.max(map.getZoom(), FOCUS_ZOOM), { animate: false })
        else fitAll(map, activities)
      }
    })
    observer.observe(containerRef.current)

    const markers = markersRef.current
    return () => {
      observer.disconnect()
      map.remove()
      mapRef.current = null
      fittedKeyRef.current = null
      markers.clear()
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // 2) Dibujar un pin por actividad cada vez que cambia la lista filtrada.
  useEffect(() => {
    const map = mapRef.current
    const layer = layerRef.current
    layer.clearLayers()
    markersRef.current.clear()

    for (const activity of activities) {
      const marker = L.marker([activity.latitude, activity.longitude], {
        icon: pinIcon(activity, false),
        riseOnHover: true,
      })
      const label = document.createElement('span') // textContent: sin HTML inyectado
      label.textContent = activity.title
      marker.bindTooltip(label, { direction: 'top', opacity: 1 })
      marker.on('click', () => latest.current.onSelect(activity.slug))
      marker.activity = activity
      marker.active = false
      layer.addLayer(marker)
      markersRef.current.set(activity.slug, marker)
    }

    // Se reencuadra solo si cambió QUÉ actividades hay (por un filtro). Si únicamente cambiaron
    // los textos (cambio de idioma), se respeta el zoom y la posición que la persona dejó.
    const key = activities.map((a) => a.slug).join('|')
    if (fittedKeyRef.current !== key) {
      fitAll(map, activities)
      fittedKeyRef.current = key
    }
  }, [activities])

  // 3) Resaltar el pin seleccionado (se vuelve a dibujar su ícono con la clase "pin--active").
  useEffect(() => {
    markersRef.current.forEach((marker, slug) => {
      const active = slug === selectedSlug
      if (marker.active !== active) {
        marker.active = active
        marker.setIcon(pinIcon(marker.activity, active))
      }
      marker.setZIndexOffset(active ? 1000 : 0)
    })
  }, [selectedSlug, activities])

  // 4) Al elegir una actividad, volar hasta ella.
  useEffect(() => {
    const map = mapRef.current
    const marker = markersRef.current.get(selectedSlug)
    if (!map || !marker) return
    // En celular el mapa puede acabar de pasar de oculto a visible: Leaflet todavía cree que
    // mide 0×0 y volar daría coordenadas NaN. Recalculamos el tamaño; si sigue oculto, no
    // volamos (el ResizeObserver encuadra la actividad cuando el mapa aparezca).
    map.invalidateSize()
    const { x, y } = map.getSize()
    if (x === 0 || y === 0) return
    map.flyTo(marker.getLatLng(), Math.max(map.getZoom(), FOCUS_ZOOM), { duration: 0.8 })
  }, [selectedSlug])

  return (
    <div className="map-wrap">
      <div ref={containerRef} className="map" role="region" aria-label={t('map.aria')} />

      {selected && (
        <div className="map-selected" data-category={selected.category}>
          <span className="map-selected__icon">
            <CategoryIcon slug={selected.category} />
          </span>
          <div className="map-selected__text">
            <p className="map-selected__title">{selected.title}</p>
            <p className="map-selected__meta">
              {selected.zone} · {priceLabel(selected.price_level, t)}
            </p>
            <a href={directionsUrl(selected)} target="_blank" rel="noopener noreferrer">
              {t('card.directions')}
              <ExternalLinkIcon aria-hidden="true" />
            </a>
          </div>
          <button className="map-selected__close" onClick={onClear} aria-label={t('map.close')}>
            <CloseIcon aria-hidden="true" />
          </button>
        </div>
      )}
    </div>
  )
}
