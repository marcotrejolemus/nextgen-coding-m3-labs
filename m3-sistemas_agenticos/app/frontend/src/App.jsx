import { useState } from 'react'
import FormularioEmpleado from './components/FormularioEmpleado.jsx'
import FormularioBaja from './components/FormularioBaja.jsx'
import DirectorioEmpleados from './components/DirectorioEmpleados.jsx'

function App() {
  const [refreshKey, setRefreshKey] = useState(0)
  const [panelActivo, setPanelActivo] = useState('crear')
  const [empleadoSeleccionado, setEmpleadoSeleccionado] = useState(null)
  const [mensajeOperacion, setMensajeOperacion] = useState('')

const volverACrear = () => {
  setMensajeOperacion('')
  setPanelActivo('crear')
  setEmpleadoSeleccionado(null)
}

const manejarGuardado = () => {
  setRefreshKey((anterior) => anterior + 1)

  if (panelActivo === 'editar') {
    setMensajeOperacion('Empleado actualizado correctamente')
  } else if (panelActivo === 'baja') {
    setMensajeOperacion('Empleado dado de baja correctamente')
  } else {
    setMensajeOperacion('')
  }

  setPanelActivo('crear')
  setEmpleadoSeleccionado(null)
}

  const manejarEditar = (empleado) => {
    setEmpleadoSeleccionado(empleado)
    setPanelActivo('editar')
  }

  const manejarBaja = (empleado) => {
    setEmpleadoSeleccionado(empleado)
    setPanelActivo('baja')
  }

  return (
    <div>
      <h1>Gestión de empleados</h1>
      {mensajeOperacion && (
        <p data-testid="mensaje-exito" role="status">
          {mensajeOperacion}
        </p>
      )}
      {panelActivo === 'crear' && (
        <FormularioEmpleado modo="crear" onGuardado={manejarGuardado} />
      )}
      {panelActivo === 'editar' && empleadoSeleccionado && (
        <FormularioEmpleado
          modo="editar"
          empleadoInicial={empleadoSeleccionado}
          onGuardado={manejarGuardado}
          onCancelar={volverACrear}
        />
      )}
      {panelActivo === 'baja' && empleadoSeleccionado && (
        <FormularioBaja
          empleado={empleadoSeleccionado}
          onGuardado={manejarGuardado}
          onCancelar={volverACrear}
        />
      )}
      <DirectorioEmpleados refrescar={refreshKey} onEditar={manejarEditar} onBaja={manejarBaja} />
    </div>
  )
}

export default App
