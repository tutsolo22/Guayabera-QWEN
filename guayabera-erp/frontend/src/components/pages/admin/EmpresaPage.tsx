import React from 'react';
import { Card, Descriptions, Tag, Typography, Button } from 'antd';
import { BuildOutlined } from '@ant-design/icons';

const { Title } = Typography;

const EmpresaPage: React.FC = () => {
  return (
    <div>
      <Title level={3}>
        <BuildOutlined /> Configuración de Empresa
      </Title>

      <Card>
        <Descriptions bordered column={2}>
          <Descriptions.Item label="RFC">GUA250101ABC</Descriptions.Item>
          <Descriptions.Item label="Razón Social">
            Guayaberas Yucatecas SA de CV
          </Descriptions.Item>
          <Descriptions.Item label="Nombre Comercial">GuayaberaCAD</Descriptions.Item>
          <Descriptions.Item label="Régimen Fiscal">
            <Tag color="blue">Régimen General de Ley</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Dirección">
            Calle 60 #123, Centro, Mérida, Yucatán, 97000
          </Descriptions.Item>
          <Descriptions.Item label="Contacto">
            info@guayabera-cad.com | 999-123-4567
          </Descriptions.Item>
          <Descriptions.Item label="Estado">
            <Tag color="success">Activa</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Sitio Web">
            <a href="https://guayabera-cad.com" target="_blank" rel="noopener noreferrer">
              guayabera-cad.com
            </a>
          </Descriptions.Item>
        </Descriptions>

        <div style={{ marginTop: 24 }}>
          <Button type="primary">Editar Empresa</Button>
        </div>
      </Card>
    </div>
  );
};

export default EmpresaPage;
