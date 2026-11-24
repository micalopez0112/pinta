import { useI18n } from '../i18n'
import { CategoryIcon, IndoorIcon } from '../icons'
import '../styles/activities.css'

// El nombre de cada categoría (c.label) viene del backend ya en el idioma elegido.
export default function Filters({ categories, category, onCategory, indoorOnly, onIndoorOnly, onClear }) {
  const { t } = useI18n()

  return (
    <div className="filters" role="group" aria-label={t('filters.aria')}>
      {/* "Todas" está activo solo cuando no hay ningún filtro; al tocarlo, los limpia. */}
      <button className="chip" aria-pressed={category === null && !indoorOnly} onClick={onClear}>
        {t('filters.all')}
      </button>

      {categories.map((c) => (
        <button
          key={c.slug}
          className="chip"
          aria-pressed={category === c.slug}
          onClick={() => onCategory(category === c.slug ? null : c.slug)}
        >
          <CategoryIcon slug={c.slug} />
          {c.label}
        </button>
      ))}

      <span className="filters__divider" aria-hidden="true" />

      <button className="chip" aria-pressed={indoorOnly} onClick={() => onIndoorOnly(!indoorOnly)}>
        <IndoorIcon aria-hidden="true" />
        {t('filters.indoor')}
      </button>
    </div>
  )
}
