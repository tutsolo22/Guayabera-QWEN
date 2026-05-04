import React, { useEffect, useState } from 'react';
import { Row, Col, Statistic, Table } from 'antd';
import { UserOutlined, ShopOutlined, MoneyCollectOutlined, TeamOutlined } from '@ant-design/icons';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    tenants: 0,
    users: 0,
    licenses: 0,
    activeLicenses: 0
  });

  // Mock data for recent activity
  const recentActivity = [
    {
      key: '1',
      activity: 'Nuevo tenant creado',
      tenant: 'Empresa ABC',
      date: '2026-05-01',
    },
    {
      key: '2',
      activity: 'Licencia renovada',
      tenant: 'Cliente XYZ',
      date: '2026-04-29',
    },
    {
      key: '3',
      activity: 'Usuario registrado',
      tenant: 'Empresa DEF',
      date: '2026-04-28',
    },
  ];

  // Mock data for table columns
  const columns = [
    {
      title: 'Actividad',
      dataIndex: 'activity',
      key: 'activity',
    },
    {
      title: 'Tenant',
      dataIndex: 'tenant',
      key: 'tenant',
    },
    {
      title: 'Fecha',
      dataIndex: 'date',
      key: 'date',
    },
  ];

  // Simulate fetching stats
  useEffect(() => {
    // In a real app, this would be an API call
    setTimeout(() => {
      setStats({
        tenants: 12,
        users: 42,
        licenses: 50,
        activeLicenses: 38
      });
    }, 500);
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ color: '#1B365D', marginBottom: 24 }}>Panel de Administración</h1>
      
      <Row gutter={16}>
        <Col span={6}>
          <div style={{ padding: '20px', background: '#f0f2f5', borderRadius: '4px' }}>
            <Statistic
              title="Empresas"
              value={stats.tenants}
              prefix={<ShopOutlined />}
            />
          </div>
        </Col>
        <Col span={6}>
          <div style={{ padding: '20px', background: '#f0f2f5', borderRadius: '4px' }}>
            <Statistic
              title="Usuarios"
              value={stats.users}
              prefix={<UserOutlined />}
            />
          </div>
        </Col>
        <Col span={6}>
          <div style={{ padding: '20px', background: '#f0f2f5', borderRadius: '4px' }}>
            <Statistic
              title="Licencias"
              value={stats.licenses}
              prefix={<MoneyCollectOutlined />}
            />
          </div>
        </Col>
        <Col span={6}>
          <div style={{ padding: '20px', background: '#f0f2f5', borderRadius: '4px' }}>
            <Statistic
              title="Lic. Activas"
              value={stats.activeLicenses}
              prefix={<TeamOutlined />}
            />
          </div>
        </Col>
      </Row>

      <Row style={{ marginTop: 24 }}>
        <Col span={24}>
          <div style={{ padding: '20px', background: '#f0f2f5', borderRadius: '4px' }}>
            <h3 style={{ marginBottom: 16 }}>Actividad Reciente</h3>
            <Table 
              dataSource={recentActivity} 
              columns={columns} 
              pagination={{ pageSize: 5 }}
            />
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;