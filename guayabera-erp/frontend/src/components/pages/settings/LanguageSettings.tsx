import React from 'react';
import { Card, Select, Space, Typography } from 'antd';

const { Title, Text } = Typography;
const { Option } = Select;

const LanguageSettings: React.FC = () => {
  return (
    <Card className="dashboard-card">
      <Title level={3}>Idioma</Title>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div>
          <Text strong>Seleccionar Idioma</Text>
          <br />
          <Select defaultValue="es" style={{ width: 200, marginTop: 8 }}>
            <Option value="es">Español</Option>
            <Option value="en">English</Option>
            <Option value="fr">Français</Option>
            <Option value="de">Deutsch</Option>
          </Select>
        </div>
        
        <div>
          <Text strong>Formato de Fecha</Text>
          <br />
          <Select defaultValue="dd/mm/yyyy" style={{ width: 200, marginTop: 8 }}>
            <Option value="dd/mm/yyyy">DD/MM/YYYY (Ej: 25/12/2023)</Option>
            <Option value="mm/dd/yyyy">MM/DD/YYYY (Ej: 12/25/2023)</Option>
            <Option value="yyyy-mm-dd">YYYY-MM-DD (Ej: 2023-12-25)</Option>
          </Select>
        </div>
        
        <div>
          <Text strong>Formato de Números</Text>
          <br />
          <Select defaultValue="es-MX" style={{ width: 200, marginTop: 8 }}>
            <Option value="es-MX">Español (México) 1,234.56</Option>
            <Option value="en-US">English (US) 1,234.56</Option>
            <Option value="de-DE">Deutsch (Alemania) 1.234,56</Option>
          </Select>
        </div>
      </Space>
    </Card>
  );
};

export default LanguageSettings;