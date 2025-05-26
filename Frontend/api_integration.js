/**
 * Script para integrar la página DISPOSITIVOS.html con la API de PythonAnywhere
 * Este archivo debe incluirse al final de DISPOSITIVOS.html
 */

// Cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
  // Obtener la URL base (útil para PythonAnywhere)
  const API_BASE_URL = window.location.origin;

  // Sobrescribir la función fetchSensorData para usar la API real
  window.fetchSensorData = function() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    showNotification('Cargando datos de sensores...');

    // Hacer la petición a la API real
    fetch(`${API_BASE_URL}/api/sensores/fechas?start=${startDate}&end=${endDate}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Error en la respuesta de la API');
        }
        return response.json();
      })
      .then(result => {
        if (result.success && result.data.length > 0) {
          // Actualizar los datos globales
          sensorData = result.data;
          updateUI();
        } else {
          showNotification('No se encontraron datos para el rango seleccionado. Mostrando datos simulados.');
          simulateSensorData();
        }
      })
      .catch(error => {
        console.error('Error al obtener datos:', error);
        showNotification('Error al obtener datos. Usando datos simulados.');
        simulateSensorData();
      });
  };

  // Función para cargar los datos más recientes
  window.loadLatestData = function() {
    fetch(`${API_BASE_URL}/api/sensores/ultimo`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Error al obtener el último registro');
        }
        return response.json();
      })
      .then(result => {
        if (result.success) {
          // Actualizar los valores en tiempo real
          const data = result.data;

          document.getElementById('tempValue').textContent = `${parseFloat(data.Temperatura).toFixed(1)}°C`;
          document.getElementById('humValue').textContent = `${parseFloat(data.Humedad).toFixed(1)}%`;
          document.getElementById('rainValue').textContent = data.EstadoLluvia || calcularLluvia(data.Lluvia);
          document.getElementById('lightValue').textContent = data.EstadoLuz || calcularLuz(data.Luz);
          document.getElementById('windValue').textContent = `${parseFloat(data.Viento).toFixed(1)} km/h`;

          // Actualizar estado del dispositivo
          const deviceStatus = document.getElementById('deviceStatus');
          const deviceStatusText = document.getElementById('deviceStatusText');
          const lastUpdate = document.getElementById('lastUpdate');

          deviceStatus.className = 'status-indicator online';
          deviceStatusText.textContent = 'Conectado - Enviando datos';
          lastUpdate.textContent = `Actualizado ${formatTimeAgo(new Date())}`;

          showNotification('Datos actualizados correctamente');
        }
      })
      .catch(error => {
        console.error('Error al obtener último registro:', error);
        showNotification('Error al obtener datos actuales');

        // Cambiar estado del dispositivo a offline
        const deviceStatus = document.getElementById('deviceStatus');
        const deviceStatusText = document.getElementById('deviceStatusText');

        deviceStatus.className = 'status-indicator offline';
        deviceStatusText.textContent = 'Desconectado - Error al obtener datos';
      });
  };

  // Mejorar la función exportDataToCSV para incluir estados interpretados
  window.exportDataToCSV = function() {
    if (sensorData.length === 0) {
      showNotification('No hay datos para exportar');
      return;
    }

    let csvContent = 'data:text/csv;charset=utf-8,';

    // Agregar encabezados
    csvContent += 'Fecha,Hora,Temperatura,Humedad,Lluvia,Estado Lluvia,Luz,Estado Luz,Viento\n';

    // Agregar datos
    sensorData.forEach(record => {
      const estadoLluvia = record.EstadoLluvia || calcularLluvia(record.Lluvia);
      const estadoLuz = record.EstadoLuz || calcularLuz(record.Luz);
      csvContent += `${record.Fecha},${record.Hora},${parseFloat(record.Temperatura).toFixed(1)},${parseFloat(record.Humedad).toFixed(1)},${record.Lluvia},${estadoLluvia},${record.Luz},${estadoLuz},${parseFloat(record.Viento).toFixed(1)}\n`;
    });

    // Crear el enlace para descargar
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `sensor_data_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);

    // Descargar
    link.click();

    // Limpiar
    document.body.removeChild(link);

    showNotification('Datos exportados correctamente');
  };

  // Añadir un botón de actualización
  const addRefreshButton = function() {
    const refreshBtn = document.createElement('button');
    refreshBtn.className = 'btn btn-info d-block ml-2';
    refreshBtn.innerHTML = '<i class="fas fa-sync-alt mr-1"></i>Actualizar ahora';
    refreshBtn.addEventListener('click', loadLatestData);

    // Agregar el botón después del botón de exportar
    const exportBtn = document.getElementById('exportDataBtn');
    if (exportBtn && exportBtn.parentNode) {
      exportBtn.parentNode.appendChild(refreshBtn);
    }
  };

  // Inicializar
  addRefreshButton();
  loadLatestData();

  // Configurar intervalo para actualizar automáticamente (cada 2 minutos)
  setInterval(loadLatestData, 120000);
});