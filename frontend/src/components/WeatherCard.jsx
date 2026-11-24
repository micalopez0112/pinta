import { getWeather } from '../api'
import { clockTime, degrees, uvInfo } from '../format'
import { useAsync } from '../hooks'
import { useI18n } from '../i18n'
import { WeatherIcon } from '../icons'
import '../styles/weather.css'

export default function WeatherCard({ placeName, onShowIndoor }) {
  const { t } = useI18n()
  const { status, data: weather, reload } = useAsync(getWeather)

  if (!weather) {
    return (
      <aside className="weather weather--empty" aria-busy={status === 'loading'}>
        {status === 'error' ? (
          <>
            <p>{t('weather.error')}</p>
            <button className="button button--light" onClick={reload}>
              {t('common.retry')}
            </button>
          </>
        ) : (
          <p>{t('weather.loading')}</p>
        )}
      </aside>
    )
  }

  const uv = uvInfo(weather.uv_index_max)

  return (
    <aside className="weather" aria-label={t('weather.aria', { place: placeName })}>
      <p className="weather__label">{t('weather.label', { place: placeName })}</p>

      <div className="weather__main">
        <span className="weather__icon" data-icon={weather.icon} data-day={weather.is_day}>
          <WeatherIcon icon={weather.icon} isDay={weather.is_day} />
        </span>
        <div>
          <p className="weather__temp">{degrees(weather.temperature)}</p>
          <p className="weather__condition">{t(`weather.conditions.${weather.condition}`)}</p>
        </div>
      </div>

      <p className="weather__feel">
        {t('weather.feelsLike', { temp: degrees(weather.feels_like) })} ·{' '}
        {t('weather.wind', { speed: Math.round(weather.wind_kmh) })}
      </p>

      <dl className="weather__stats">
        <div>
          <dt>{t('weather.today')}</dt>
          <dd>
            {degrees(weather.temp_min)} / {degrees(weather.temp_max)}
          </dd>
        </div>
        {weather.rain_probability != null && (
          <div>
            <dt>{t('weather.rain')}</dt>
            <dd>{weather.rain_probability}%</dd>
          </div>
        )}
        {uv && (
          <div>
            <dt>{t('weather.uv')}</dt>
            <dd>
              {uv.value} · {t(`weather.uvLevels.${uv.level}`)}
            </dd>
          </div>
        )}
        {weather.sunset && (
          <div>
            <dt>{t('weather.sunset')}</dt>
            <dd>{weather.sunset}</dd>
          </div>
        )}
      </dl>

      <div className="weather__tip">
        <p>{t(`weather.tips.${weather.suggestion}`)}</p>
        {weather.suggestion === 'indoor' && (
          <button onClick={onShowIndoor}>{t('weather.showIndoor')}</button>
        )}
      </div>

      <p className="weather__source">
        {t('weather.updated', { time: clockTime(weather.observed_at) })} ·{' '}
        <a href="https://open-meteo.com/" target="_blank" rel="noopener noreferrer">
          Open-Meteo
        </a>
      </p>
    </aside>
  )
}
