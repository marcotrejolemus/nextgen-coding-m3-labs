import { useEffect, useState } from 'react'

const VALORES_INICIALES = {
  nombre: '',
  correo: '',
  puesto: '',
  departamento: '',
  fecha_ingreso: '',
}

function FormularioEmpleado({ modo = 'crear', empleadoInicial, onGuardado, onCancelar }) {
  const esEdicion = modo === 'editar'
  const [valores, setValores] = useState(
    esEdicion && empleadoInicial ? { ...VALORES_INICIALES, ...empleadoInicial } : VALORES_INICIALES
  )
  const [departamentos, setDepartamentos] = useState([])
  const [mensajeExito, setMensajeExito] = useState('')
  const [mensajeError, setMensajeError] = useState('')

  useEffect(() => {
    fetch('/api/departamentos')
      .then((response) => response.json())
      .then((data) => setDepartamentos(data))
      .catch(() => setDepartamentos([]))
  }, [])

  useEffect(() => {
    if (esEdicion && empleadoInicial) {
      setValores({ ...VALORES_INICIALES, ...empleadoInicial })
    }
  }, [esEdicion, empleadoInicial])

  const actualizarCampo = (campo) => (evento) => {
    setValores((anteriores) => ({ ...anteriores, [campo]: evento.target.value }))
  }

  const enviarFormulario = async (evento) => {
    evento.preventDefault()
    setMensajeExito('')
    setMensajeError('')

    const url = esEdicion ? `/api/empleados/${empleadoInicial.id}` : '/api/empleados'
    const body = esEdicion
      ? { puesto: valores.puesto, departamento: valores.departamento }
      : valores

    const response = await fetch(url, {
      method: esEdicion ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    const datos = await response.json()

    if (!response.ok) {
      setMensajeError(datos.detail)
      return
    }

    setMensajeExito(
      esEdicion
        ? 'Empleado actualizado correctamente'
        : `Empleado registrado con número ${datos.numero_empleado}`
    )
    if (!esEdicion) {
      setValores(VALORES_INICIALES)
    }
    onGuardado?.(datos)
  }

  return (
    <form onSubmit={enviarFormulario}>
      <label>
        Nombre
        <input
          data-testid="empleado-nombre"
          value={valores.nombre}
          onChange={actualizarCampo('nombre')}
          disabled={esEdicion}
        />
      </label>
      <label>
        Correo
        <input
          data-testid="empleado-correo"
          value={valores.correo}
          onChange={actualizarCampo('correo')}
          disabled={esEdicion}
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
          disabled={esEdicion}
        />
      </label>
      <button type="submit" data-testid="empleado-guardar">
        Guardar
      </button>
      {esEdicion && onCancelar && (
        <button type="button" onClick={onCancelar}>
          Cancelar
        </button>
      )}
      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  )
}

export default FormularioEmpleado
