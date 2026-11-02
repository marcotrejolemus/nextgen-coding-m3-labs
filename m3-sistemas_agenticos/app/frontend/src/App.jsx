import { useState } from 'react'
import FormularioEmpleado from './components/FormularioEmpleado.jsx'
import DirectorioEmpleados from './components/DirectorioEmpleados.jsx'

function App() {
  const [refreshKey, setRefreshKey] = useState(0)

  return (
    <div>
      <h1>Gestión de empleados</h1>
      <FormularioEmpleado onEmpleadoRegistrado={() => setRefreshKey((anterior) => anterior + 1)} />
      <DirectorioEmpleados refrescar={refreshKey} />
    </div>
  )
}

export default App
