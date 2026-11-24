import { useEffect, useRef, useState } from 'react'
import { BR, DE, ES, GB } from 'country-flag-icons/react/3x2'
import { LANGUAGES, useI18n } from '../i18n'
import { CheckIcon, ChevronDownIcon } from '../icons'
import '../styles/language.css'

// Banderas en SVG (los emojis de bandera no se ven en Windows).
// Inglés: Reino Unido. Portugués: Brasil (el contenido está en portugués de Brasil).
const FLAGS = { es: ES, en: GB, pt: BR, de: DE }

function Flag({ code }) {
  const Svg = FLAGS[code]
  return <Svg className="flag" aria-hidden="true" />
}

export default function LanguageSwitcher() {
  const { lang, setLang, t } = useI18n()
  const [open, setOpen] = useState(false)
  const buttonRef = useRef(null)
  const rootRef = useRef(null)
  const current = LANGUAGES.find((l) => l.code === lang)

  // Se cierra con Escape (devolviendo el foco al botón) o tocando fuera.
  useEffect(() => {
    if (!open) return
    const onKeyDown = (event) => {
      if (event.key === 'Escape') {
        setOpen(false)
        buttonRef.current?.focus()
      }
    }
    const onPointerDown = (event) => {
      if (!rootRef.current?.contains(event.target)) setOpen(false)
    }
    document.addEventListener('keydown', onKeyDown)
    document.addEventListener('pointerdown', onPointerDown)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      document.removeEventListener('pointerdown', onPointerDown)
    }
  }, [open])

  const choose = (code) => {
    setLang(code)
    setOpen(false)
    buttonRef.current?.focus()
  }

  return (
    <div
      className="lang"
      ref={rootRef}
      // Si el foco sale del selector (Tab), se cierra.
      onBlur={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget)) setOpen(false)
      }}
    >
      <button
        ref={buttonRef}
        type="button"
        className="lang__button"
        aria-expanded={open}
        aria-controls="lang-menu"
        aria-label={`${t('language.change')}: ${current.label}`}
        onClick={() => setOpen((value) => !value)}
      >
        <Flag code={lang} />
        <span className="lang__code">{current.short}</span>
        <ChevronDownIcon className="lang__chevron" aria-hidden="true" />
      </button>

      {open && (
        <ul id="lang-menu" className="lang__menu">
          {LANGUAGES.map((language) => (
            <li key={language.code}>
              <button
                type="button"
                className="lang__option"
                lang={language.code}
                aria-current={language.code === lang ? 'true' : undefined}
                onClick={() => choose(language.code)}
              >
                <Flag code={language.code} />
                <span className="lang__name">{language.label}</span>
                <span className="lang__code">{language.short}</span>
                {language.code === lang && <CheckIcon className="lang__check" aria-hidden="true" />}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
