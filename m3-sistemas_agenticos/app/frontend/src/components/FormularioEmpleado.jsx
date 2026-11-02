import { useEffect, useState } from 'react'

const VALORES_INICIALES = {
  nombre: '',
  correo: '',
  puesto: '',
  departamento: '',
  fecha_ingreso: '',
}

function FormularioEmpleado({ onEmpleadoRegistrado }) {
  const [valores, setValores] = useState(VALORES_INICIALES)
  const [departamentos, setDepartamentos] = useState([])
  const [mensajeExito, setMensajeExito] = useState('')
  const [mensajeError, setMensajeError] = useState('')

  useEffect(() => {
    fetch('/api/departamentos')
      .then((response) => response.json())
      .then((data) => setDepartamentos(data))
      .catch(() => setDepartamentos([]))
  }, [])

  const actualizarCampo = (campo) => (evento) => {
    setValores((anteriores) => ({ ...anteriores, [campo]: evento.target.value }))
  }

  const enviarFormulario = async (evento) => {
    evento.preventDefault()
    setMensajeExito('')
    setMensajeError('')

    const response = await fetch('/api/empleados', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(valores),
    })
    const datos = await response.json()

    if (!response.ok) {
      setMensajeError(datos.detail)
      return
    }

    setMensajeExito(`Empleado registrado con número ${datos.numero_empleado}`)
    setValores(VALORES_INICIALES)
    onEmpleadoRegistrado?.()
  }

  return (
    <form onSubmit={enviarFormulario}>
      <label>
        Nombre
        <input
          data-testid="empleado-nombre"
          value={valores.nombre}
          onChange={actualizarCampo('nombre')}
        />
      </label>
      <label>
        Correo
        <input
          data-testid="empleado-correo"
          value={valores.correo}
          onChange={actualizarCampo('correo')}
        />
      </label>
      <label>
        Puesto
        <input
          data-testid="empleado-puesto"
          value={valores.puesto}
          onChange={actualizarCampo('puesto')}
        />
      </label>
      <label>
        Departamento
        <select
          data-testid="empleado-departamento"
          value={valores.departamento}
          onChange={actualizarCampo('departamento')}
        >
          <option value="">Selecciona un departamento</option>
          {departamentos.map((departamento) => (
            <option key={departamento} value={departamento}>
              {departamento}
            </option>
          ))}
        </select>
      </label>
      <label>
        Fecha de ingreso
        <input
          type="date"
          data-testid="empleado-fecha-ingreso"
          value={valores.fecha_ingreso}
          onChange={actualizarCampo('fecha_ingreso')}
        />
      </label>
      <button type="submit" data-testid="empleado-guardar">
        Guardar
      </button>
      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  )
}

export default FormularioEmpleado
