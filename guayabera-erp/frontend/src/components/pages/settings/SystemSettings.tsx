import React from 'react';
import { Card, Tabs, Typography } from 'antd';
import ThemeSettings from './ThemeSettings';
import LanguageSettings from './LanguageSettings';

const { Title } = Typography;

const SystemSettings: React.FC = () => {
  const items = [
    {
      key: 'theme',
      label: 'Tema y Colores',
      children: <ThemeSettings />,
    },
    {
      key: 'language',
      label: 'Idioma y Regional',
      children: <LanguageSettings />,
    },
    {
      key: 'general',
      label: 'Configuración General',
      children: (
        <Card className="dashboard-card">
          <Title level={4}>Configuración General del Sistema</Title>
          <p>Próximamente se implementará aquí la configuración general del sistema.</p>
        </Card>
      ),
    },
    {
      key: 'security',
      label: 'Seguridad',
      children: (
        <Card className="dashboard-card">
          <Title level={4}>Configuración de Seguridad</Title>
          <p>Próximamente se implementará aquí la configuración de seguridad.</p>
        </Card>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>Configuración del Sistema</Title>
      <Card className="dashboard-card">
        <Tabs defaultActiveKey="theme" items={items} />
      </Card>
    </div>
  );
};

export default SystemSettings;