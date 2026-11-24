import { useI18n } from '../i18n'
import ActivityCard from './ActivityCard'
import '../styles/activities.css'

export default function ActivityList({
  status,
  activities,
  selection,
  hasFilters,
  onSelect,
  onShowOnMap,
  onClearFilters,
  onRetry,
}) {
  const { t } = useI18n()

  if (status === 'error') {
    return (
      <div className="notice" role="alert">
        <p>{t('activities.error')}</p>
        <button className="button button--small" onClick={onRetry}>
          {t('common.retry')}
        </button>
      </div>
    )
  }

  if (status === 'loading') {
    return (
      <ul className="cards" aria-busy="true" aria-label={t('activities.loading')}>
        {[0, 1, 2].map((i) => (
          <li key={i}>
            <div className="card card--skeleton" />
          </li>
        ))}
      </ul>
    )
  }

  if (activities.length === 0) {
    return (
      <div className="notice">
        <p>{t('activities.empty')}</p>
        {hasFilters && (
          <button className="button button--small" onClick={onClearFilters}>
            {t('activities.clearFilters')}
          </button>
        )}
      </div>
    )
  }

  return (
    <ul className="cards">
      {activities.map((activity) => (
        <ActivityCard
          key={activity.slug}
          activity={activity}
          selected={selection?.slug === activity.slug}
          revealOnSelect={selection?.source === 'map'}
          onSelect={onSelect}
          onShowOnMap={onShowOnMap}
        />
      ))}
    </ul>
  )
}
