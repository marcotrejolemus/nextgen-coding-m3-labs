import { useEffect, useState } from 'react'

const ESTADO_TEXTO = {
  activo: 'Activo',
  baja: 'Baja',
}

function DirectorioEmpleados({ refrescar, onEditar, onBaja }) {
  const [empleados, setEmpleados] = useState([])
  const [departamentos, setDepartamentos] = useState([])
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')
  const [busqueda, setBusqueda] = useState('')
  const [departamentoFiltro, setDepartamentoFiltro] = useState('')

  useEffect(() => {
    fetch('/api/departamentos')
      .then((response) => response.json())
      .then((data) => setDepartamentos(data))
      .catch(() => setDepartamentos([]))
  }, [])

  useEffect(() => {
    const parametros = new URLSearchParams()
    if (busqueda) parametros.set('busqueda', busqueda)
    if (departamentoFiltro) parametros.set('departamento', departamentoFiltro)

    setCargando(true)
    fetch(`/api/empleados?${parametros.toString()}`)
      .then((response) => {
        if (!response.ok) throw new Error('error')
        return response.json()
      })
      .then((data) => {
        setEmpleados(data)
        setError('')
      })
      .catch(() => setError('No se pudo cargar el directorio de empleados'))
      .finally(() => setCargando(false))
  }, [busqueda, departamentoFiltro, refrescar])

  return (
    <div>
      <h2>Directorio de empleados</h2>
      <input
        data-testid="buscar-empleados"
        placeholder="Buscar por nombre o correo"
        value={busqueda}
        onChange={(evento) => setBusqueda(evento.target.value)}
      />
      <select
        data-testid="filtro-departamento"
        value={departamentoFiltro}
        onChange={(evento) => setDepartamentoFiltro(evento.target.value)}
      >
        <option value="">Todos los departamentos</option>
        {departamentos.map((departamento) => (
          <option key={departamento} value={departamento}>
            {departamento}
          </option>
        ))}
      </select>

      {cargando && <p>Cargando...</p>}
      {error && <p data-testid="mensaje-error">{error}</p>}

      {empleados.length === 0 && !cargando && !error ? (
        <p data-testid="sin-resultados">No se encontraron resultados</p>
      ) : (
        <table data-testid="tabla-empleados">
          <thead>
            <tr>
              <th>Número</th>
              <th>Nombre</th>
              <th>Puesto</th>
              <th>Departamento</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empleados.map((empleado) => (
              <tr key={empleado.id} data-testid={`fila-empleado-${empleado.id}`}>
                <td data-testid={`numero-empleado-${empleado.id}`}>{empleado.numero_empleado}</td>
                <td>{empleado.nombre}</td>
                <td>{empleado.puesto}</td>
                <td>{empleado.departamento}</td>
                <td data-testid={`estado-empleado-${empleado.id}`}>
                  {ESTADO_TEXTO[empleado.estado] ?? empleado.estado}
                </td>
                <td>
                  <button
                    data-testid={`editar-empleado-${empleado.id}`}
                    onClick={() => onEditar?.(empleado)}
                  >
                    Editar
                  </button>
                  <button
                    data-testid={`baja-empleado-${empleado.id}`}
                    onClick={() => onBaja?.(empleado)}
                  >
                    Dar de baja
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default DirectorioEmpleados
