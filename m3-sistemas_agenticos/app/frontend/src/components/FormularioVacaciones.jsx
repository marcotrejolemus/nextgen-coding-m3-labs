import { useEffect, useState } from 'react'

function FormularioVacaciones({ empleado, onCerrar }) {
  const [fechaInicio, setFechaInicio] = useState('')
  const [fechaFin, setFechaFin] = useState('')
  const [diasDisponibles, setDiasDisponibles] = useState(null)
  const [mensaje, setMensaje] = useState('')

  const cargarSaldo = () => {
    fetch(`/api/empleados/${empleado.id}/vacaciones`)
      .then((response) => response.json())
      .then((data) => setDiasDisponibles(data.dias_disponibles))
      .catch(() => setDiasDisponibles(null))
  }

  useEffect(() => {
    cargarSaldo()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [empleado.id])

  const enviarSolicitud = async (evento) => {
    evento.preventDefault()
    setMensaje('')

    const response = await fetch(`/api/empleados/${empleado.id}/vacaciones`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fecha_inicio: fechaInicio, fecha_fin: fechaFin }),
    })
    const datos = await response.json()

    if (!response.ok) {
      setMensaje(datos.detail)
      return
    }

    setMensaje(
      `Solicitud registrada: ${datos.dias_habiles} días hábiles. ` +
        `Te quedan ${datos.dias_restantes} días hábiles en ${fechaInicio.slice(0, 4)}.`
    )
    cargarSaldo()
  }

  return (
    <form onSubmit={enviarSolicitud}>
      <h3>Solicitar vacaciones de {empleado.nombre}</h3>
      <p>
        Días disponibles:{' '}
        <span data-testid="vacaciones-disponibles">
          {diasDisponibles === null ? '...' : diasDisponibles}
        </span>
      </p>
      <label>
        Fecha de inicio
        <input
          type="date"
          data-testid="vacaciones-fecha-inicio"
          value={fechaInicio}
          onChange={(evento) => setFechaInicio(evento.target.value)}
        />
      </label>
      <label>
        Fecha de fin
        <input
          type="date"
          data-testid="vacaciones-fecha-fin"
          value={fechaFin}
          onChange={(evento) => setFechaFin(evento.target.value)}
        />
      </label>
      <button type="submit" data-testid="vacaciones-enviar">
        Enviar solicitud
      </button>
      {onCerrar && (
        <button type="button" onClick={onCerrar}>
          Cerrar
        </button>
      )}
      {mensaje && <p data-testid="vacaciones-mensaje">{mensaje}</p>}
    </form>
  )
}

export default FormularioVacaciones
