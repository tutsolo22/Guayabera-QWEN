import React, { useState } from 'react';
import { Card, Form, Input, Button, message, Typography, Alert } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { loginStart, loginSuccess, loginFailure } from '../../../store/features/auth/authSlice';
import { useLoginMutation } from '../../../services/authApi';
import { RootState } from '../../../store';

const { Title, Text } = Typography;

const LoginPage: React.FC = () => {
  const [form] = Form.useForm();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [login, { isLoading }] = useLoginMutation();
  const error = useSelector((state: RootState) => state.auth.error);

  const onFinish = async (values: { username: string; password: string }) => {
    try {
      dispatch(loginStart());
      const result = await login(values).unwrap();
      dispatch(loginSuccess({ user: result.user, token: result.access_token }));
      message.success('¡Bienvenido a GuayaberaERP!');
      navigate('/dashboard');
    } catch (err: any) {
      dispatch(loginFailure(err?.data?.detail || 'Error de autenticación'));
      message.error('Usuario o contraseña incorrectos');
    }
  };

  return (
    <div className="login-container">
      <Card className="login-card">
        <div className="login-logo">
          <Title level={2}>🧵 GuayaberaERP</Title>
          <Text type="secondary">Sistema ERP Textil especializado</Text>
        </div>

        {error && (
          <Alert
            message="Error de autenticación"
            description={error}
            type="error"
            showIcon
            style={{ marginBottom: 24 }}
          />
        )}

        <Form
          form={form}
          name="login"
          onFinish={onFinish}
          size="large"
          autoComplete="off"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Por favor ingresa tu usuario' }]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="Usuario o email"
              autoFocus
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Por favor ingresa tu contraseña' }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Contraseña"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={isLoading}
              block
              style={{ height: 40, fontSize: 16 }}
            >
              Iniciar Sesión
            </Button>
          </Form.Item>
        </Form>

        <div style={{ textAlign: 'center', marginTop: 16 }}>
          <Text type="secondary" style={{ fontSize: 12 }}>
            Para pruebas usa: admin / admin123456
          </Text>
        </div>
      </Card>
    </div>
  );
};

export default LoginPage;
