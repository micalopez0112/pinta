import { useEffect, useRef } from 'react'
import { directionsUrl, priceLabel } from '../format'
import { useI18n } from '../i18n'
import { CategoryIcon, ExternalLinkIcon, IndoorIcon } from '../icons'

export default function ActivityCard({ activity, selected, revealOnSelect, onSelect, onShowOnMap }) {
  const { t } = useI18n()
  const ref = useRef(null)

  // Si la selección vino del mapa, traemos la tarjeta a la vista.
  useEffect(() => {
    if (selected && revealOnSelect) {
      ref.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
    }
  }, [selected, revealOnSelect])

  const price = priceLabel(activity.price_level, t)

  return (
    <li>
      <article
        ref={ref}
        className="card"
        data-category={activity.category}
        aria-current={selected ? 'true' : undefined}
        onClick={() => onSelect(activity.slug)}
      >
        <span className="card__icon">
          <CategoryIcon slug={activity.category} />
        </span>

        <div className="card__body">
          <h3 className="card__title">{activity.title}</h3>
          <p className="card__meta">
            {activity.zone}
            {activity.duration && ` · ${activity.duration}`}
          </p>
          <p className="card__description">{activity.description}</p>

          <div className="card__tags">
            <span className={`tag ${activity.price_level === 0 ? 'tag--free' : ''}`}>{price}</span>
            {activity.indoor && (
              <span className="tag tag--indoor">
                <IndoorIcon aria-hidden="true" />
                {t('card.indoor')}
              </span>
            )}
          </div>

          <div className="card__actions">
            <button
              type="button"
              className="button button--small button--ghost card__map-button"
              onClick={(event) => {
                event.stopPropagation()
                onShowOnMap(activity.slug)
              }}
            >
              {t('card.showOnMap')}
            </button>
            <a
              className="card__link"
              href={directionsUrl(activity)}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(event) => event.stopPropagation()}
            >
              {t('card.directions')}
              <ExternalLinkIcon aria-hidden="true" />
            </a>
          </div>
        </div>
      </article>
    </li>
  )
}
