import { useState } from 'react'

function FormularioBaja({ empleado, onGuardado, onCancelar }) {
  const [fechaBaja, setFechaBaja] = useState('')
  const [mensajeExito, setMensajeExito] = useState('')
  const [mensajeError, setMensajeError] = useState('')

  const confirmarBaja = async (evento) => {
    evento.preventDefault()
    setMensajeExito('')
    setMensajeError('')

    const response = await fetch(`/api/empleados/${empleado.id}/baja`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fecha_baja: fechaBaja }),
    })
    const datos = await response.json()

    if (!response.ok) {
      setMensajeError(datos.detail)
      return
    }

    setMensajeExito('Empleado dado de baja correctamente')
    onGuardado?.(datos)
  }

  return (
    <form onSubmit={confirmarBaja}>
      <label>
        Fecha de baja
        <input
          type="date"
          data-testid="empleado-fecha-baja"
          value={fechaBaja}
          onChange={(evento) => setFechaBaja(evento.target.value)}
        />
      </label>
      <button type="submit" data-testid="confirmar-baja">
        Confirmar baja
      </button>
      {onCancelar && (
        <button type="button" onClick={onCancelar}>
          Cancelar
        </button>
      )}
      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  )
}

export default FormularioBaja
