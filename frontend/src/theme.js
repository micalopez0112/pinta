// Modo claro / oscuro.
//
// El tema es el atributo data-theme="light" | "dark" de <html>. Lo pone por primera vez el
// script de index.html, ANTES de que se pinte la página (así no hay un destello del tema
// equivocado). Orden de prioridad: 1) lo que la persona eligió con el botón, 2) el tema de
// su sistema operativo. Si nunca eligió, la página sigue los cambios del sistema.
import { useCallback, useEffect, useState } from 'react'

const STORAGE_KEY = 'pinta.theme'
const COLORS = { light: '#5f14ed', dark: '#121019' } // color de la barra del navegador en el celular

const readSaved = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved === 'light' || saved === 'dark' ? saved : null
  } catch {
    return null // sin acceso a localStorage (modo privado, etc.)
  }
}

const systemTheme = () => (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')

export function useTheme() {
  // index.html ya lo dejó en <html>; si por algún motivo no, se calcula igual.
  const [theme, setTheme] = useState(() => document.documentElement.dataset.theme ?? readSaved() ?? systemTheme())

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', COLORS[theme])
  }, [theme])

  // Si la persona nunca eligió un tema, acompañamos al sistema (por ejemplo, de día a noche).
  useEffect(() => {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const onChange = () => {
      if (!readSaved()) setTheme(systemTheme())
    }
    media.addEventListener('change', onChange)
    return () => media.removeEventListener('change', onChange)
  }, [])

  const toggle = useCallback(() => {
    const next = theme === 'dark' ? 'light' : 'dark'
    setTheme(next)
    try {
      localStorage.setItem(STORAGE_KEY, next)
    } catch {
      // si no se puede guardar, el cambio igual vale para esta visita
    }
  }, [theme])

  return { theme, toggle }
}
