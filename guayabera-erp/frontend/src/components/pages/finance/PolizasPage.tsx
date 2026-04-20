import React, { useState } from 'react';
import {
  Table, Button, Modal, Form, Input, Select, DatePicker, message, Typography, Tag, Space, Descriptions, Divider
} from 'antd';
import { PlusOutlined, EyeOutlined } from '@ant-design/icons';
import {
  useGetPolizasQuery,
  useCreatePolizaMutation,
  useGetCuentasQuery,
  PolizaContable
} from '../../../services/financeApi';
import dayjs from 'dayjs';

const { Title } = Typography;
const { TextArea } = Input;

const PolizasPage: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [viewModalVisible, setViewModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [selectedPoliza, setSelectedPoliza] = useState<PolizaContable | null>(null);
  const [movimientos, setMovimientos] = useState<any[]>([]);

  const { data: polizas, isLoading } = useGetPolizasQuery();
  const { data: cuentas } = useGetCuentasQuery();
  const [createPoliza] = useCreatePolizaMutation();

  const handleAddMovimiento = () => {
    setMovimientos([
      ...movimientos,
      { cuenta_id: '', cargo: 0, abono: 0, concepto: '' }
    ]);
  };

  const handleRemoveMovimiento = (index: number) => {
    setMovimientos(movimientos.filter((_, i) => i !== index));
  };

  const handleMovimientoChange = (index: number, field: string, value: any) => {
    const newMovimientos = [...movimientos];
    newMovimientos[index] = { ...newMovimientos[index], [field]: value };
    setMovimientos(newMovimientos);
  };

  const totalCargos = movimientos.reduce((sum, m) => sum + (Number(m.cargo) || 0), 0);
  const totalAbonos = movimientos.reduce((sum, m) => sum + (Number(m.abono) || 0), 0);
  const estaCuadrada = totalCargos === totalAbonos && totalCargos > 0;

  const handleCreate = async (values: any) => {
    if (!estaCuadrada) {
      message.error('La póliza no está cuadrada. Cargos deben ser iguales a Abonos');
      return;
    }

    try {
      await createPoliza({
        tipo: values.tipo,
        fecha: values.fecha.format('YYYY-MM-DD'),
        descripcion: values.descripcion,
        movimientos: movimientos.map(m => ({
          cuenta_id: m.cuenta_id,
          cargo: Number(m.cargo) || 0,
          abono: Number(m.abono) || 0,
          concepto: m.concepto,
        })),
      }).unwrap();

      message.success('✅ Póliza creada exitosamente');
      setModalVisible(false);
      form.resetFields();
      setMovimientos([]);
    } catch (error: any) {
      message.error(error?.data?.detail || 'Error creando póliza');
    }
  };

  const columns = [
    {
      title: 'Número',
      dataIndex: 'numero',
      key: 'numero',
      width: 100,
      sorter: (a: any, b: any) => a.numero - b.numero,
      render: (num: number) => <strong>#{num}</strong>,
    },
    {
      title: 'Tipo',
      dataIndex: 'tipo',
      key: 'tipo',
      width: 120,
      render: (tipo: string) => {
        const colors: any = { diario: 'blue', ingreso: 'green', egreso: 'orange' };
        return <Tag color={colors[tipo]}>{tipo.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Fecha',
      dataIndex: 'fecha',
      key: 'fecha',
      width: 120,
      render: (fecha: string) => dayjs(fecha).format('DD/MM/YYYY'),
    },
    {
      title: 'Descripción',
      dataIndex: 'descripcion',
      key: 'descripcion',
      ellipsis: true,
    },
    {
      title: 'Estado',
      dataIndex: 'estado',
      key: 'estado',
      width: 120,
      render: (estado: string) => {
        const colors: any = {
          borrador: 'default',
          revisada: 'processing',
          aprobada: 'success',
          cancelada: 'error',
        };
        return <Tag color={colors[estado]}>{estado.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Cargos',
      dataIndex: 'total_cargos',
      key: 'total_cargos',
      width: 150,
      render: (total: number) => `$${total.toLocaleString('es-MX', { minimumFractionDigits: 2 })}`,
    },
    {
      title: 'Abonos',
      dataIndex: 'total_abonos',
      key: 'total_abonos',
      width: 150,
      render: (total: number) => `$${total.toLocaleString('es-MX', { minimumFractionDigits: 2 })}`,
    },
    {
      title: 'Acciones',
      key: 'acciones',
      width: 100,
      render: (_: any, record: PolizaContable) => (
        <Button
          icon={<EyeOutlined />}
          size="small"
          onClick={() => {
            setSelectedPoliza(record);
            setViewModalVisible(true);
          }}
        >
          Ver
        </Button>
      ),
    },
  ];

  return (
    <div>
      <div className="table-header">
        <Title level={3}>Pólizas Contables</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setModalVisible(true)}
        >
          Nueva Póliza
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={polizas || []}
        rowKey="id"
        loading={isLoading}
        pagination={{ pageSize: 20 }}
      />

      {/* Create Modal */}
      <Modal
        title="Nueva Póliza Contable"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
          setMovimientos([]);
        }}
        footer={null}
        width={900}
      >
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="tipo" label="Tipo de Póliza" rules={[{ required: true }]}>
            <Select placeholder="Selecciona el tipo">
              <Select.Option value="diario">Diario</Select.Option>
              <Select.Option value="ingreso">Ingreso</Select.Option>
              <Select.Option value="egreso">Egreso</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item name="fecha" label="Fecha" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item name="descripcion" label="Descripción" rules={[{ required: true }]}>
            <TextArea rows={2} placeholder="Descripción de la póliza" />
          </Form.Item>

          <Divider>Movimientos</Divider>

          {movimientos.map((mov, index) => (
            <Space key={index} style={{ width: '100%', marginBottom: 16 }} align="start">
              <Form.Item label="Cuenta" style={{ flex: 2 }}>
                <Select
                  value={mov.cuenta_id}
                  onChange={(value) => handleMovimientoChange(index, 'cuenta_id', value)}
                  placeholder="Selecciona cuenta"
                  showSearch
                  optionFilterProp="children"
                >
                  {cuentas?.map(c => (
                    <Select.Option key={c.id} value={c.id}>
                      {c.codigo} - {c.nombre}
                    </Select.Option>
                  ))}
                </Select>
              </Form.Item>

              <Form.Item label="Cargo" style={{ flex: 1 }}>
                <Input
                  type="number"
                  value={mov.cargo}
                  onChange={(e) => handleMovimientoChange(index, 'cargo', e.target.value)}
                  placeholder="0.00"
                  min={0}
                  step="0.01"
                />
              </Form.Item>

              <Form.Item label="Abono" style={{ flex: 1 }}>
                <Input
                  type="number"
                  value={mov.abono}
                  onChange={(e) => handleMovimientoChange(index, 'abono', e.target.value)}
                  placeholder="0.00"
                  min={0}
                  step="0.01"
                />
              </Form.Item>

              <Form.Item label="Concepto" style={{ flex: 3 }}>
                <Input
                  value={mov.concepto}
                  onChange={(e) => handleMovimientoChange(index, 'concepto', e.target.value)}
                  placeholder="Concepto del movimiento"
                />
              </Form.Item>

              <Button
                danger
                onClick={() => handleRemoveMovimiento(index)}
                style={{ marginTop: 32 }}
              >
                Eliminar
              </Button>
            </Space>
          ))}

          <Button onClick={handleAddMovimiento} style={{ marginBottom: 16 }}>
            + Agregar Movimiento
          </Button>

          <div style={{
            padding: 16,
            background: estaCuadrada ? '#f6ffed' : '#fff2f0',
            border: `1px solid ${estaCuadrada ? '#b7eb8f' : '#ffccc7'}`,
            borderRadius: 4,
            marginBottom: 16
          }}>
            <strong>Resumen:</strong> Cargos: ${totalCargos.toFixed(2)} | Abonos: ${totalAbonos.toFixed(2)}
            {estaCuadrada ? ' ✅ Cuadrada' : ' ❌ No cuadrada'}
          </div>

          <Form.Item>
            <Button type="primary" htmlType="submit" block disabled={!estaCuadrada || movimientos.length < 2}>
              Crear Póliza
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* View Modal */}
      <Modal
        title={`Póliza #${selectedPoliza?.numero}`}
        open={viewModalVisible}
        onCancel={() => setViewModalVisible(false)}
        footer={null}
        width={800}
      >
        {selectedPoliza && (
          <>
            <Descriptions bordered column={2}>
              <Descriptions.Item label="Tipo">
                <Tag>{selectedPoliza.tipo.toUpperCase()}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Fecha">
                {dayjs(selectedPoliza.fecha).format('DD/MM/YYYY')}
              </Descriptions.Item>
              <Descriptions.Item label="Estado">
                <Tag>{selectedPoliza.estado.toUpperCase()}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Cuadrada">
                {selectedPoliza.esta_cuadrada ? '✅ Sí' : '❌ No'}
              </Descriptions.Item>
            </Descriptions>

            <Divider>{selectedPoliza.descripcion}</Divider>

            <Table
              dataSource={selectedPoliza.movimientos}
              rowKey="id"
              pagination={false}
              columns={[
                { title: 'Concepto', dataIndex: 'concepto', key: 'concepto' },
                {
                  title: 'Cargo',
                  dataIndex: 'cargo',
                  key: 'cargo',
                  render: (val: number) => val > 0 ? `$${val.toFixed(2)}` : '-',
                },
                {
                  title: 'Abono',
                  dataIndex: 'abono',
                  key: 'abono',
                  render: (val: number) => val > 0 ? `$${val.toFixed(2)}` : '-',
                },
              ]}
              summary={() => (
                <Table.Summary>
                  <Table.Summary.Row>
                    <Table.Summary.Cell index={0}><strong>Totales</strong></Table.Summary.Cell>
                    <Table.Summary.Cell index={1}>
                      <strong>${selectedPoliza.total_cargos.toFixed(2)}</strong>
                    </Table.Summary.Cell>
                    <Table.Summary.Cell index={2}>
                      <strong>${selectedPoliza.total_abonos.toFixed(2)}</strong>
                    </Table.Summary.Cell>
                  </Table.Summary.Row>
                </Table.Summary>
              )}
            />
          </>
        )}
      </Modal>
    </div>
  );
};

export default PolizasPage;
