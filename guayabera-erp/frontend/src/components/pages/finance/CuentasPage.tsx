import React, { useState } from 'react';
import {
  Table, Button, Modal, Form, Input, Select, message, Typography, Tag, Space, Popconfirm, Switch
} from 'antd';
import { PlusOutlined, ImportOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import {
  useGetCuentasQuery,
  useCreateCuentaMutation,
  useImportarCatalogoSATMutation,
  CuentaContable
} from '../../../services/financeApi';

const { Title } = Typography;

const CuentasPage: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingCuenta, setEditingCuenta] = useState<CuentaContable | null>(null);

  const { data: cuentas, isLoading, refetch } = useGetCuentasQuery();
  const [createCuenta] = useCreateCuentaMutation();
  const [importarSAT, { isLoading: importing }] = useImportarCatalogoSATMutation();

  const handleImportarSAT = async () => {
    try {
      const result = await importarSAT().unwrap();
      message.success(`✅ Catálogo importado: ${result.cuentas_importadas} cuentas creadas`);
      refetch();
    } catch (error: any) {
      message.error('Error importando catálogo SAT');
    }
  };

  const handleCreate = async (values: any) => {
    try {
      await createCuenta(values).unwrap();
      message.success('Cuenta contable creada exitosamente');
      setModalVisible(false);
      form.resetFields();
      refetch();
    } catch (error: any) {
      message.error(error?.data?.detail || 'Error creando cuenta');
    }
  };

  const columns = [
    {
      title: 'Código',
      dataIndex: 'codigo',
      key: 'codigo',
      width: 150,
      sorter: (a: any, b: any) => a.codigo.localeCompare(b.codigo),
    },
    {
      title: 'Nombre',
      dataIndex: 'nombre',
      key: 'nombre',
      ellipsis: true,
    },
    {
      title: 'Nivel',
      dataIndex: 'nivel',
      key: 'nivel',
      width: 80,
      align: 'center' as const,
    },
    {
      title: 'Tipo',
      dataIndex: 'tipo',
      key: 'tipo',
      width: 120,
      render: (tipo: string) => {
        const colors: any = {
          activo: 'blue',
          pasivo: 'red',
          capital: 'purple',
          ingresos: 'green',
          costos: 'orange',
          gastos: 'volcano',
        };
        return <Tag color={colors[tipo]}>{tipo.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Naturaleza',
      dataIndex: 'naturaleza',
      key: 'naturaleza',
      width: 120,
      render: (nat: string) => (
        <Tag color={nat === 'deudora' ? 'cyan' : 'magenta'}>
          {nat?.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Mayor',
      dataIndex: 'es_cuenta_mayor',
      key: 'es_cuenta_mayor',
      width: 80,
      align: 'center' as const,
      render: (value: boolean) => value ? '✅' : '❌',
    },
    {
      title: 'Activa',
      dataIndex: 'activa',
      key: 'activa',
      width: 80,
      align: 'center' as const,
      render: (value: boolean) => <Switch checked={value} disabled size="small" />,
    },
  ];

  return (
    <div>
      <div className="table-header">
        <Title level={3}>Catálogo de Cuentas Contables</Title>
        <Space>
          <Button
            icon={<ImportOutlined />}
            onClick={handleImportarSAT}
            loading={importing}
          >
            Importar Catálogo SAT
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setModalVisible(true)}
          >
            Nueva Cuenta
          </Button>
        </Space>
      </div>

      <Table
        columns={columns}
        dataSource={cuentas || []}
        rowKey="id"
        loading={isLoading}
        pagination={{ pageSize: 20, showSizeChanger: true }}
        scroll={{ x: 1000 }}
        locale={{ emptyText: 'No hay cuentas contables. Importa el catálogo SAT para comenzar.' }}
      />

      <Modal
        title={editingCuenta ? 'Editar Cuenta' : 'Nueva Cuenta Contable'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
          setEditingCuenta(null);
        }}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreate}
        >
          <Form.Item
            name="codigo"
            label="Código"
            rules={[{ required: true, message: 'El código es obligatorio' }]}
          >
            <Input placeholder="Ej: 1101040001" />
          </Form.Item>

          <Form.Item
            name="nombre"
            label="Nombre"
            rules={[{ required: true, message: 'El nombre es obligatorio' }]}
          >
            <Input placeholder="Ej: Inventario Materia Prima" />
          </Form.Item>

          <Form.Item
            name="nivel"
            label="Nivel"
            rules={[{ required: true, message: 'El nivel es obligatorio' }]}
          >
            <Select placeholder="Selecciona el nivel">
              <Select.Option value={1}>1 - Grupo</Select.Option>
              <Select.Option value={2}>2 - Género</Select.Option>
              <Select.Option value={3}>3 - Cuenta Mayor</Select.Option>
              <Select.Option value={4}>4 - Subcuenta</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="tipo"
            label="Tipo"
            rules={[{ required: true, message: 'El tipo es obligatorio' }]}
          >
            <Select placeholder="Selecciona el tipo">
              <Select.Option value="activo">Activo</Select.Option>
              <Select.Option value="pasivo">Pasivo</Select.Option>
              <Select.Option value="capital">Capital</Select.Option>
              <Select.Option value="ingresos">Ingresos</Select.Option>
              <Select.Option value="costos">Costos</Select.Option>
              <Select.Option value="gastos">Gastos</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="naturaleza"
            label="Naturaleza"
            rules={[{ required: true, message: 'La naturaleza es obligatoria' }]}
          >
            <Select placeholder="Selecciona la naturaleza">
              <Select.Option value="deudora">Deudora</Select.Option>
              <Select.Option value="acreedora">Acreedora</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item name="descripcion" label="Descripción">
            <Input.TextArea rows={3} placeholder="Descripción opcional de la cuenta" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              {editingCuenta ? 'Actualizar' : 'Crear Cuenta'}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CuentasPage;
