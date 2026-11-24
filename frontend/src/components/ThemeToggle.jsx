import { useI18n } from '../i18n'
import { MoonIcon, SunIcon } from '../icons'
import { useTheme } from '../theme'
import '../styles/theme.css'

// Botón redondo de la barra superior: luna en modo claro (para ir al oscuro), sol en modo oscuro.
export default function ThemeToggle() {
  const { t } = useI18n()
  const { theme, toggle } = useTheme()
  const isDark = theme === 'dark'

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={toggle}
      aria-label={isDark ? t('theme.toLight') : t('theme.toDark')}
      title={isDark ? t('theme.toLight') : t('theme.toDark')}
    >
      {isDark ? <SunIcon aria-hidden="true" /> : <MoonIcon aria-hidden="true" />}
    </button>
  )
}
