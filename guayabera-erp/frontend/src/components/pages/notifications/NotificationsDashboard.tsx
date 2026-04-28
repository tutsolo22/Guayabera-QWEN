import React, { useState } from 'react';
import { Card, Row, Col, Statistic, Button, Typography, List, Tag, Badge, Alert } from 'antd';
import { 
  NotificationOutlined, 
  BellOutlined, 
  MailOutlined, 
  CheckOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const NotificationsDashboard: React.FC = () => {
  const [notifications, setNotifications] = useState([
    { id: '1', titulo: 'Pedido completado', descripcion: 'El pedido #PED-001 ha sido completado y está listo para envío', tipo: 'info', fecha: '2023-04-01 10:30', leido: false },
    { id: '2', titulo: 'Factura generada', descripcion: 'La factura #FAC-001 ha sido generada y timbrada correctamente', tipo: 'success', fecha: '2023-04-01 11:45', leido: true },
    { id: '3', titulo: 'Bajo stock', descripcion: 'El producto "Camisa Lino Azul" tiene bajo nivel de stock', tipo: 'warning', fecha: '2023-04-02 09:15', leido: false },
    { id: '4', titulo: 'Pago recibido', descripcion: 'Se ha registrado el pago del cliente "Tienda Yucateca"', tipo: 'success', fecha: '2023-04-02 14:20', leido: true },
    { id: '5', titulo: 'Recordatorio', descripcion: 'Recordatorio: Reunión de planeación semanal hoy a las 3pm', tipo: 'info', fecha: '2023-04-02 15:00', leido: false },
  ]);

  const marcarTodasComoLeidas = () => {
    setNotifications(notifications.map(n => ({ ...n, leido: true })));
  };

  const notificationTypes = {
    info: { color: '#1890ff', icon: <BellOutlined /> },
    success: { color: '#52c41a', icon: <CheckCircleOutlined /> },
    warning: { color: '#faad14', icon: <NotificationOutlined /> },
    error: { color: '#ff4d4f', icon: <MailOutlined /> }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Notificaciones</Title>
          <Text>
            Centro de notificaciones y alertas del sistema
          </Text>
        </div>
        <Button icon={<CheckOutlined />} onClick={marcarTodasComoLeidas}>
          Marcar todas como leídas
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar notificaciones internas y externas del sistema."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Notificaciones" 
              value={notifications.length} 
              prefix={<NotificationOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="No Leídas" 
              value={notifications.filter(n => !n.leido).length} 
              prefix={<BellOutlined />} 
              valueStyle={{ color: '#fa8c16' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Hoy" 
              value={3} 
              prefix={<CheckCircleOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Este Mes" 
              value={86} 
              prefix={<NotificationOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <List
          itemLayout="horizontal"
          dataSource={notifications}
          renderItem={notification => (
            <List.Item 
              style={{ 
                backgroundColor: notification.leido ? '#fafafa' : '#e6f7ff',
                borderLeft: notification.leido ? 'none' : '3px solid #1890ff',
                padding: '12px 16px'
              }}
            >
              <List.Item.Meta
                avatar={
                  <Badge dot={!notification.leido}>
                    <div 
                      style={{ 
                        width: 40, 
                        height: 40, 
                        borderRadius: '50%', 
                        backgroundColor: notificationTypes[notification.tipo as keyof typeof notificationTypes]?.color || '#1890ff',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                    >
                      {notificationTypes[notification.tipo as keyof typeof notificationTypes]?.icon || <NotificationOutlined style={{ color: 'white' }} />}
                    </div>
                  </Badge>
                }
                title={
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>{notification.titulo}</span>
                    <span style={{ color: '#aaa', fontSize: '12px' }}>{notification.fecha}</span>
                  </div>
                }
                description={notification.descripcion}
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default NotificationsDashboard;