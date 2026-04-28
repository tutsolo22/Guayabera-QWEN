import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import esES from 'antd/locale/es_ES';
import dayjs from 'dayjs';
import 'dayjs/locale/es';

import App from './App';
import { store } from './store';
import './index.css';

// Configurar dayjs en español
dayjs.locale('es');

// Aplicar el tema inicial basado en la preferencia del sistema
const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
const initialTheme = store.getState().ui.theme || (prefersDarkMode ? 'dark' : 'light');

// Actualizar el atributo data-theme en el elemento html
document.documentElement.setAttribute('data-theme', initialTheme);

// Escuchar cambios en el estado del tema
store.subscribe(() => {
  const currentTheme = store.getState().ui.theme;
  document.documentElement.setAttribute('data-theme', currentTheme);
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <ConfigProvider
          locale={esES}
          theme={{
            token: {
              colorPrimary: '#1890ff',
              borderRadius: 6,
            },
          }}
        >
          <App />
        </ConfigProvider>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>,
);
