import { useI18n } from '../i18n'
import WeatherCard from './WeatherCard'

export default function Hero({ placeName, onShowIndoor }) {
  const { t } = useI18n()

  return (
    <section className="hero">
      <div className="container hero__inner">
        <div className="hero__copy">
          <p className="eyebrow">{t('hero.eyebrow')}</p>
          <h1>
            {t('hero.titlePrefix')} <em>{placeName}</em>
          </h1>
          <p className="hero__lead">{t('hero.lead')}</p>
          <a className="button" href="#actividades">
            {t('hero.cta')}
          </a>
        </div>
        <WeatherCard placeName={placeName} onShowIndoor={onShowIndoor} />
      </div>
    </section>
  )
}
