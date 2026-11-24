import { useCallback, useEffect, useState } from 'react'

/**
 * Llama a `load(signal)` al montar (y cada vez que cambian `deps`).
 * Devuelve { status: 'loading' | 'ready' | 'error', data, reload }.
 */
export function useAsync(load, deps = []) {
  const [state, setState] = useState({ status: 'loading', data: null })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    setState((previous) => ({ status: 'loading', data: previous.data }))
    load(controller.signal).then(
      (data) => setState({ status: 'ready', data }),
      (error) => {
        if (error.name !== 'AbortError') setState({ status: 'error', data: null })
      },
    )
    return () => controller.abort()
  }, [...deps, attempt]) // eslint-disable-line react-hooks/exhaustive-deps

  const reload = useCallback(() => setAttempt((n) => n + 1), [])
  return { ...state, reload }
}
