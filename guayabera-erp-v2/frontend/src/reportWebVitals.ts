type ReportHandler = (metric: any) => void;

const reportWebVitals = (onPerfEntry?: ReportHandler) => {
  if (onPerfEntry && typeof onPerfEntry === 'function') {
    import('web-vitals')
      .then((webVitals) => {
        // Acceder a las funciones a través del objeto webVitals
        webVitals.getCLS && webVitals.getCLS(onPerfEntry);
        webVitals.getFID && webVitals.getFID(onPerfEntry);
        webVitals.getFCP && webVitals.getFCP(onPerfEntry);
        webVitals.getLCP && webVitals.getLCP(onPerfEntry);
        webVitals.getTTFB && webVitals.getTTFB(onPerfEntry);
      })
      .catch((error) => {
        console.error('Error importing web-vitals:', error);
      });
  }
};

export default reportWebVitals;