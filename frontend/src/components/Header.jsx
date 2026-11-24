import { useI18n } from '../i18n'
import LanguageSwitcher from './LanguageSwitcher'
import ThemeToggle from './ThemeToggle'

export default function Header() {
  const { t } = useI18n()

  return (
    <header className="site-header">
      <div className="container site-header__inner">
        <a className="brand" href="/" aria-label={t('header.home')}>
          <img className="brand__logo" src="/logo.png" alt="" width="31" height="40" />
          <span className="brand__name">Pinta</span>
        </a>

        <div className="site-header__actions">
          <nav className="site-header__nav" aria-label={t('header.nav')}>
            <a className="site-header__link" href="#actividades">
              {t('header.activities')}
            </a>
          </nav>
          <ThemeToggle />
          <LanguageSwitcher />
        </div>
      </div>
    </header>
  )
}
