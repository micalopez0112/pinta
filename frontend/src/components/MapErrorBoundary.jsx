import { Component } from 'react'

// Si el mapa falla por cualquier motivo, el resto de la página (lista, clima) sigue funcionando.
// Es una clase (así lo exige React para los error boundaries), por eso no puede usar el hook de
// idioma: los textos llegan ya traducidos como props (message y retryLabel).
export default class MapErrorBoundary extends Component {
  state = { failed: false }

  static getDerivedStateFromError() {
    return { failed: true }
  }

  componentDidCatch(error) {
    console.error('Falló el mapa:', error)
  }

  render() {
    if (!this.state.failed) return this.props.children
    return (
      <div className="notice" role="alert">
        <p>{this.props.message}</p>
        <button className="button button--small" onClick={() => this.setState({ failed: false })}>
          {this.props.retryLabel}
        </button>
      </div>
    )
  }
}
