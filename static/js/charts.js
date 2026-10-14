// Smart Krishi Chart.js Visualizations

function initMarketPriceChart(canvasId, labels, dataPoints, cropName) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: `${cropName} (₹ / Quintal)`,
        data: dataPoints,
        borderColor: '#1e7e34',
        backgroundColor: 'rgba(30, 126, 52, 0.08)',
        fill: true,
        tension: 0.35,
        pointBackgroundColor: '#1e7e34',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: { font: { weight: 'bold' } }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return ` Price: ₹${context.parsed.y.toLocaleString('en-IN')}`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: '#eef2ee' },
          ticks: {
            callback: function(value) {
              return '₹' + value.toLocaleString('en-IN');
            }
          }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });
}

function initWeatherChart(canvasId, labels, maxTemps, minTemps, rainProbs) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          type: 'line',
          label: 'Max Temp (°C)',
          data: maxTemps,
          borderColor: '#e65100',
          backgroundColor: '#e65100',
          yAxisID: 'yTemp',
          tension: 0.3,
          pointRadius: 4
        },
        {
          type: 'line',
          label: 'Min Temp (°C)',
          data: minTemps,
          borderColor: '#0288d1',
          backgroundColor: '#0288d1',
          yAxisID: 'yTemp',
          tension: 0.3,
          pointRadius: 4
        },
        {
          type: 'bar',
          label: 'Rain Probability (%)',
          data: rainProbs,
          backgroundColor: 'rgba(46, 125, 50, 0.45)',
          borderColor: '#2e7d32',
          borderWidth: 1,
          borderRadius: 4,
          yAxisID: 'yRain'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' }
      },
      scales: {
        yTemp: {
          type: 'linear',
          position: 'left',
          title: { display: true, text: 'Temperature (°C)' },
          grid: { color: '#f0f4f0' }
        },
        yRain: {
          type: 'linear',
          position: 'right',
          min: 0,
          max: 100,
          title: { display: true, text: 'Rain %' },
          grid: { display: false }
        }
      }
    }
  });
}

function initExpenseChart(canvasId, costs) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Seeds', 'Fertilizer', 'Pesticide', 'Irrigation', 'Machinery', 'Labor'],
      datasets: [{
        data: [
          costs.seed,
          costs.fertilizer,
          costs.pesticide,
          costs.irrigation,
          costs.machinery,
          costs.labor
        ],
        backgroundColor: [
          '#81c784',
          '#4caf50',
          '#ffb74d',
          '#4fc3f7',
          '#ba68c8',
          '#e57373'
        ],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              return ` ₹${ctx.parsed.toLocaleString('en-IN')}`;
            }
          }
        }
      }
    }
  });
}
