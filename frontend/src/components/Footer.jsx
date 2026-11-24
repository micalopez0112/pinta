import { useI18n } from '../i18n'

export default function Footer() {
  const { t } = useI18n()

  return (
    <footer className="site-footer">
      <div className="container site-footer__inner">
        <p>
          <strong>Pinta</strong> · {t('footer.note')}
        </p>
        <p>
          {t('footer.weatherBy')}{' '}
          <a href="https://open-meteo.com/" target="_blank" rel="noopener noreferrer">
            Open-Meteo
          </a>{' '}
          · {t('footer.mapBy')}{' '}
          <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">
            OpenStreetMap
          </a>
        </p>
      </div>
    </footer>
  )
}
