import React, { useState, useEffect, useRef } from 'react';
import { Card, Row, Col, Button, Space, Typography, Input, List, Avatar, Divider, Tag, Modal, Form, Select, InputNumber } from 'antd';
import { 
  RobotOutlined, 
  SendOutlined, 
  MessageOutlined, 
  BookOutlined, 
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  UserOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

interface AISession {
  id: string;
  titulo: string;
  ultimaInteraccion: string;
  activa: boolean;
}

interface AIMessage {
  id: string;
  contenido: string;
  emisor: 'usuario' | 'ia';
  fecha: string;
}

interface AIKnowledge {
  id: string;
  titulo: string;
  categoria: string;
  prioridad: number;
}

const AIAssistant: React.FC = () => {
  const [sessions, setSessions] = useState<AISession[]>([
    { id: '1', titulo: 'Consulta sobre nómina', ultimaInteraccion: '2023-04-15 10:30', activa: true },
    { id: '2', titulo: 'Configuración de inventario', ultimaInteraccion: '2023-04-14 15:45', activa: true },
    { id: '3', titulo: 'Reporte de ventas mensuales', ultimaInteraccion: '2023-04-12 09:20', activa: false },
  ]);
  
  const [messages, setMessages] = useState<AIMessage[]>([
    { id: '1', contenido: 'Hola, ¿cómo puedo ayudarte hoy?', emisor: 'ia', fecha: '2023-04-15 10:30' },
    { id: '2', contenido: 'Necesito saber cómo generar el reporte de nómina', emisor: 'usuario', fecha: '2023-04-15 10:31' },
    { id: '3', contenido: 'Para generar el reporte de nómina, ve al módulo de Recursos Humanos > Nómina > Reportes > Generar Reporte Mensual', emisor: 'ia', fecha: '2023-04-15 10:32' },
  ]);
  
  const [knowledgeBase, setKnowledgeBase] = useState<AIKnowledge[]>([
    { id: '1', titulo: 'Generar reporte de nómina', categoria: 'rh', prioridad: 8 },
    { id: '2', titulo: 'Configurar productos textiles', categoria: 'inventario', prioridad: 6 },
    { id: '3', titulo: 'Crear órdenes de producción', categoria: 'produccion', prioridad: 9 },
    { id: '4', titulo: 'Facturación electrónica CFDI', categoria: 'ventas', prioridad: 7 },
  ]);
  
  const [inputText, setInputText] = useState('');
  const [activeSession, setActiveSession] = useState('1');
  const [knowledgeModalVisible, setKnowledgeModalVisible] = useState(false);
  const [knowledgeForm] = Form.useForm();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = () => {
    if (!inputText.trim()) return;
    
    const newMessage: AIMessage = {
      id: (messages.length + 1).toString(),
      contenido: inputText,
      emisor: 'usuario',
      fecha: new Date().toLocaleString()
    };
    
    setMessages([...messages, newMessage]);
    setInputText('');
    
    // Simulate AI response after a delay
    setTimeout(() => {
      const aiResponse: AIMessage = {
        id: (messages.length + 2).toString(),
        contenido: `Entiendo que preguntaste: "${inputText}". Esta es una respuesta simulada del asistente de IA. En una implementación real, aquí se procesaría la pregunta y se devolvería una respuesta inteligente.`,
        emisor: 'ia',
        fecha: new Date().toLocaleString()
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  const handleCreateSession = () => {
    const newSession: AISession = {
      id: (sessions.length + 1).toString(),
      titulo: `Nueva sesión ${sessions.length + 1}`,
      ultimaInteraccion: new Date().toLocaleString(),
      activa: true
    };
    setSessions([newSession, ...sessions]);
    setActiveSession(newSession.id);
    setMessages([]);
  };

  const handleSelectSession = (sessionId: string) => {
    setActiveSession(sessionId);
    // In a real implementation, we would load the messages for this session
  };

  const handleCreateKnowledge = async () => {
    try {
      const values = await knowledgeForm.validateFields();
      
      const newKnowledge: AIKnowledge = {
        id: (knowledgeBase.length + 1).toString(),
        titulo: values.titulo,
        categoria: values.categoria,
        prioridad: values.prioridad
      };
      
      setKnowledgeBase([newKnowledge, ...knowledgeBase]);
      setKnowledgeModalVisible(false);
      knowledgeForm.resetFields();
      
      // Show success message
    } catch (error) {
      console.error('Error al crear conocimiento:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><RobotOutlined /> Asistente de IA</Title>
          <Paragraph>
            Tu asistente virtual para resolver dudas y guiar en el uso del sistema ERP
          </Paragraph>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCreateSession}>
            Nueva Conversación
          </Button>
          <Button icon={<BookOutlined />} onClick={() => setKnowledgeModalVisible(true)}>
            Base de Conocimiento
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ flex: 1, overflow: 'hidden' }}>
        <Col span={6} style={{ height: '100%' }}>
          <Card 
            title="Historial de Conversaciones" 
            style={{ height: '100%', display: 'flex', flexDirection: 'column' }}
          >
            <div style={{ overflowY: 'auto', flex: 1 }}>
              <List
                dataSource={sessions}
                renderItem={item => (
                  <List.Item 
                    onClick={() => handleSelectSession(item.id)}
                    style={{ 
                      cursor: 'pointer',
                      backgroundColor: activeSession === item.id ? '#e6f7ff' : 'transparent'
                    }}
                  >
                    <List.Item.Meta
                      title={item.titulo}
                      description={
                        <div>
                          <div>{item.ultimaInteraccion}</div>
                          <Tag color={item.activa ? 'green' : 'default'}>
                            {item.activa ? 'Activa' : 'Cerrada'}
                          </Tag>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            </div>
          </Card>
        </Col>

        <Col span={12} style={{ height: '100%' }}>
          <Card 
            title="Conversación" 
            style={{ height: '100%', display: 'flex', flexDirection: 'column' }}
          >
            <div 
              style={{ 
                flex: 1, 
                overflowY: 'auto', 
                padding: '16px 0',
                maxHeight: 'calc(100vh - 250px)'
              }}
            >
              <List
                dataSource={messages}
                renderItem={item => (
                  <List.Item 
                    style={{ 
                      textAlign: item.emisor === 'usuario' ? 'right' : 'left',
                      flexDirection: item.emisor === 'usuario' ? 'row-reverse' : 'row'
                    }}
                  >
                    <List.Item.Meta
                      avatar={
                        <Avatar 
                          style={{ backgroundColor: item.emisor === 'usuario' ? '#1890ff' : '#52c41a' }}
                          icon={item.emisor === 'usuario' ? <UserOutlined /> : <RobotOutlined />}
                        />
                      }
                      title={
                        <div>
                          <Text strong>{item.emisor === 'usuario' ? 'Tú' : 'Asistente de IA'}</Text>
                          <Text type="secondary" style={{ marginLeft: 8, fontSize: '12px' }}>
                            {item.fecha}
                          </Text>
                        </div>
                      }
                      description={
                        <div 
                          style={{
                            backgroundColor: item.emisor === 'usuario' ? '#e6f7ff' : '#f6ffed',
                            padding: '8px 12px',
                            borderRadius: '8px',
                            maxWidth: '80%',
                            display: 'inline-block',
                            textAlign: 'left'
                          }}
                        >
                          {item.contenido}
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
              <div ref={messagesEndRef} />
            </div>
            
            <Divider style={{ margin: '12px 0' }} />
            
            <div style={{ display: 'flex', gap: '8px' }}>
              <TextArea
                placeholder="Escribe tu pregunta aquí..."
                value={inputText}
                onChange={e => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                autoSize={{ minRows: 1, maxRows: 4 }}
                style={{ flex: 1 }}
              />
              <Button 
                type="primary" 
                icon={<SendOutlined />} 
                onClick={handleSendMessage}
                disabled={!inputText.trim()}
              >
                Enviar
              </Button>
            </div>
          </Card>
        </Col>

        <Col span={6} style={{ height: '100%' }}>
          <Card title="Base de Conocimiento" style={{ height: '100%' }}>
            <div style={{ overflowY: 'auto', maxHeight: 'calc(100vh - 200px)' }}>
              <List
                dataSource={knowledgeBase}
                renderItem={item => (
                  <List.Item 
                    actions={[
                      <Button type="text" icon={<EditOutlined />} />,
                      <Button type="text" icon={<DeleteOutlined />} danger />
                    ]}
                  >
                    <List.Item.Meta
                      title={item.titulo}
                      description={
                        <div>
                          <Tag color="blue">{item.categoria}</Tag>
                          <Tag color={item.prioridad > 7 ? 'red' : item.prioridad > 4 ? 'orange' : 'green'}>
                            Prioridad: {item.prioridad}
                          </Tag>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            </div>
          </Card>
        </Col>
      </Row>

      <Modal
        title="Agregar al Conocimiento del Asistente"
        open={knowledgeModalVisible}
        onCancel={() => {
          setKnowledgeModalVisible(false);
          knowledgeForm.resetFields();
        }}
        footer={null}
        width={600}
      >
        <Form
          form={knowledgeForm}
          layout="vertical"
          onFinish={handleCreateKnowledge}
        >
          <Form.Item 
            name="titulo" 
            label="Título del Conocimiento" 
            rules={[{ required: true, message: 'Por favor ingrese el título' }]}
          >
            <Input placeholder="Ej: Procedimiento para generar nómina" />
          </Form.Item>
          
          <Form.Item 
            name="categoria" 
            label="Categoría" 
            rules={[{ required: true, message: 'Por favor seleccione una categoría' }]}
          >
            <Select placeholder="Seleccione la categoría">
              <Option value="rh">Recursos Humanos</Option>
              <Option value="ventas">Ventas</Option>
              <Option value="inventario">Inventario</Option>
              <Option value="produccion">Producción</Option>
              <Option value="finanzas">Finanzas</Option>
              <Option value="facturacion">Facturación</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Form.Item 
            name="prioridad" 
            label="Prioridad" 
            rules={[{ required: true, message: 'Por favor seleccione una prioridad' }]}
          >
            <InputNumber 
              min={1} 
              max={10} 
              placeholder="Del 1 al 10"
              style={{ width: '100%' }}
            />
          </Form.Item>
          
          <Form.Item name="contenido" label="Contenido">
            <TextArea 
              placeholder="Detalle el procedimiento o información relevante" 
              rows={4} 
            />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setKnowledgeModalVisible(false);
                knowledgeForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Agregar al Conocimiento
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default AIAssistant;