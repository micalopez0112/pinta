import { useEffect, useMemo, useRef, useState } from 'react'
import { getActivities, getCategories, getDestination } from './api'
import { useAsync } from './hooks'
import { useI18n } from './i18n'
import ActivityList from './components/ActivityList'
import ActivityMap from './components/ActivityMap'
import Filters from './components/Filters'
import Footer from './components/Footer'
import Header from './components/Header'
import Hero from './components/Hero'
import MapErrorBoundary from './components/MapErrorBoundary'
import './styles/layout.css'

// Valores por si la API del destino tarda o falla: la página sigue mostrándose.
const FALLBACK_DESTINATION = { name: 'Punta del Este', latitude: -34.9632, longitude: -54.944 }
const NONE = []

export default function App() {
  const { lang, t } = useI18n()

  const destinationRequest = useAsync(getDestination)
  // Los textos de las actividades y de las categorías vienen del backend en el idioma elegido:
  // al cambiar de idioma se vuelven a pedir.
  const activitiesRequest = useAsync((signal) => getActivities(lang, signal), [lang])
  const categoriesRequest = useAsync((signal) => getCategories(lang, signal), [lang])

  const [category, setCategory] = useState(null) // null = todas
  const [indoorOnly, setIndoorOnly] = useState(false)
  const [selection, setSelection] = useState(null) // { slug, source: 'list' | 'map' }
  const [mobileView, setMobileView] = useState('list') // 'list' | 'map' (solo en pantallas chicas)
  const mapPaneRef = useRef(null)

  const destination = destinationRequest.data ?? FALLBACK_DESTINATION
  const allActivities = activitiesRequest.data ?? NONE
  const hasFilters = category !== null || indoorOnly

  // Al cambiar de idioma se sigue mostrando la lista anterior hasta que llegan los textos nuevos
  // (así no parpadea con el esqueleto de carga).
  const listStatus = activitiesRequest.data ? 'ready' : activitiesRequest.status

  // Título y descripción de la pestaña en el idioma elegido.
  useEffect(() => {
    document.title = t('meta.title', { place: destination.name })
    document
      .querySelector('meta[name="description"]')
      ?.setAttribute('content', t('meta.description', { place: destination.name }))
  }, [t, destination.name])

  const activities = useMemo(
    () =>
      allActivities.filter(
        (a) => (category === null || a.category === category) && (!indoorOnly || a.indoor),
      ),
    [allActivities, category, indoorOnly],
  )

  // Si el filtro esconde la actividad seleccionada, la selección deja de valer.
  const selected = activities.find((a) => a.slug === selection?.slug) ?? null
  const activeSelection = selected ? selection : null

  const clearFilters = () => {
    setCategory(null)
    setIndoorOnly(false)
  }

  const showIndoor = () => {
    setCategory(null)
    setIndoorOnly(true)
    document.getElementById('actividades')?.scrollIntoView({ behavior: 'smooth' })
  }

  const showOnMap = (slug) => {
    setSelection({ slug, source: 'list' })
    setMobileView('map')
    // En celular, subimos el mapa al tope para que se vea entero (con su ficha).
    requestAnimationFrame(() => mapPaneRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
  }

  const countText = listStatus === 'ready' ? t('activities.count', { count: activities.length }) : ''

  return (
    <>
      <Header />
      <main>
        <Hero placeName={destination.name} onShowIndoor={showIndoor} />

        <section id="actividades" className="container activities" aria-labelledby="actividades-titulo">
          <div className="activities__head">
            <h2 id="actividades-titulo">{t('activities.title')}</h2>
            <p className="activities__count" aria-live="polite">
              {countText}
            </p>
          </div>

          <Filters
            categories={categoriesRequest.data ?? NONE}
            category={category}
            onCategory={setCategory}
            indoorOnly={indoorOnly}
            onIndoorOnly={setIndoorOnly}
            onClear={clearFilters}
          />

          <div className="view-toggle" role="group" aria-label={t('activities.viewAria')}>
            <button aria-pressed={mobileView === 'list'} onClick={() => setMobileView('list')}>
              {t('activities.list')}
            </button>
            <button aria-pressed={mobileView === 'map'} onClick={() => setMobileView('map')}>
              {t('activities.map')}
            </button>
          </div>

          <div className="layout" data-view={mobileView}>
            <div className="list-pane">
              <ActivityList
                status={listStatus}
                activities={activities}
                selection={activeSelection}
                hasFilters={hasFilters}
                onSelect={(slug) => setSelection({ slug, source: 'list' })}
                onShowOnMap={showOnMap}
                onClearFilters={clearFilters}
                onRetry={activitiesRequest.reload}
              />
            </div>

            <div className="map-pane" ref={mapPaneRef}>
              <MapErrorBoundary message={t('map.error')} retryLabel={t('common.retry')}>
                <ActivityMap
                  center={[destination.latitude, destination.longitude]}
                  activities={activities}
                  selected={selected}
                  onSelect={(slug) => setSelection({ slug, source: 'map' })}
                  onClear={() => setSelection(null)}
                />
              </MapErrorBoundary>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
