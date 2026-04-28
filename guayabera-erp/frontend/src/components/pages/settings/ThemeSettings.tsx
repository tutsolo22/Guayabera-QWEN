import React from 'react';
import { Card, Switch, Space, Typography, Divider, ColorPicker, Flex, Segmented, Button } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../../store';
import { 
  toggleTheme, 
  setColorPalette,
  setTheme 
} from '../../../store/features/ui/uiSlice';

const { Title, Text } = Typography;

const ThemeSettings: React.FC = () => {
  const dispatch = useDispatch();
  const { theme, colorPalette } = useSelector((state: RootState) => state.ui);

  const handleThemeChange = (checked: boolean) => {
    const newTheme = checked ? 'dark' : 'light';
    dispatch(setTheme(newTheme));
  };

  const handleColorChange = (color: any, property: keyof typeof colorPalette) => {
    dispatch(setColorPalette({ [property]: color.toHexString() }));
  };

  const predefinedPalettes = {
    'default': {
      primary: '#1890ff',
      secondary: '#13c2c2',
      background: theme === 'dark' ? '#0a0a0a' : '#f0f2f5',
      surface: theme === 'dark' ? '#141414' : '#ffffff',
      text: theme === 'dark' ? '#ffffff' : '#000000',
      textSecondary: theme === 'dark' ? '#aaaaaa' : '#595959',
    },
    'turquoise': {
      primary: '#00bcd4',
      secondary: '#0097a7',
      background: theme === 'dark' ? '#0d1b2a' : '#e0f7fa',
      surface: theme === 'dark' ? '#1b263b' : '#ffffff',
      text: theme === 'dark' ? '#e0e1dd' : '#006064',
      textSecondary: theme === 'dark' ? '#92a7b0' : '#00838f',
    },
    'warm': {
      primary: '#ff9800',
      secondary: '#f57c00',
      background: theme === 'dark' ? '#202020' : '#fff8e1',
      surface: theme === 'dark' ? '#2d2d2d' : '#ffffff',
      text: theme === 'dark' ? '#ffffff' : '#e65100',
      textSecondary: theme === 'dark' ? '#cccccc' : '#f57c00',
    },
    'purple': {
      primary: '#9c27b0',
      secondary: '#7b1fa2',
      background: theme === 'dark' ? '#1a1a2e' : '#f3e5f5',
      surface: theme === 'dark' ? '#16213e' : '#ffffff',
      text: theme === 'dark' ? '#e2e2e2' : '#4a148c',
      textSecondary: theme === 'dark' ? '#a3a3c2' : '#7b1fa2',
    }
  };

  const handlePaletteSelect = (paletteName: string) => {
    const palette = predefinedPalettes[paletteName as keyof typeof predefinedPalettes];
    if (palette) {
      dispatch(setColorPalette(palette));
    }
  };

  return (
    <Card className="dashboard-card">
      <Title level={3}>Configuración de Tema</Title>
      <Divider />
      
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Flex justify="space-between" align="center">
          <div>
            <Text strong>Tema Oscuro</Text>
            <Text type="secondary" style={{ display: 'block' }}>
              Cambia entre modo claro y oscuro
            </Text>
          </div>
          <Switch
            checked={theme === 'dark'}
            onChange={handleThemeChange}
            checkedChildren="Oscuro"
            unCheckedChildren="Claro"
          />
        </Flex>
        
        <Divider>Paleta de Colores Predefinida</Divider>
        
        <Segmented
          options={[
            { label: 'Por Defecto', value: 'default' },
            { label: 'Turquesa', value: 'turquoise' },
            { label: 'Cálido', value: 'warm' },
            { label: 'Púrpura', value: 'purple' },
          ]}
          value={Object.keys(predefinedPalettes).find(key => 
            predefinedPalettes[key as keyof typeof predefinedPalettes]?.primary === colorPalette.primary
          ) || 'default'}
          onChange={handlePaletteSelect}
          style={{ marginBottom: 16 }}
        />
        
        <Divider>O Editar Individualmente</Divider>
        
        <Flex wrap gap="small">
          <div>
            <Text strong>Color Primario</Text>
            <br />
            <ColorPicker
              value={colorPalette.primary}
              onChange={(color) => handleColorChange(color, 'primary')}
              showText
              size="middle"
            />
          </div>
          
          <div>
            <Text strong>Color Secundario (Turquesa)</Text>
            <br />
            <ColorPicker
              value={colorPalette.secondary}
              onChange={(color) => handleColorChange(color, 'secondary')}
              showText
              size="middle"
            />
          </div>
          
          <div>
            <Text strong>Fondo</Text>
            <br />
            <ColorPicker
              value={colorPalette.background}
              onChange={(color) => handleColorChange(color, 'background')}
              showText
              size="middle"
            />
          </div>
          
          <div>
            <Text strong>Superficie</Text>
            <br />
            <ColorPicker
              value={colorPalette.surface}
              onChange={(color) => handleColorChange(color, 'surface')}
              showText
              size="middle"
            />
          </div>
        </Flex>
        
        <Flex wrap gap="small">
          <div>
            <Text strong>Texto Principal</Text>
            <br />
            <ColorPicker
              value={colorPalette.text}
              onChange={(color) => handleColorChange(color, 'text')}
              showText
              size="middle"
            />
          </div>
          
          <div>
            <Text strong>Texto Secundario</Text>
            <br />
            <ColorPicker
              value={colorPalette.textSecondary}
              onChange={(color) => handleColorChange(color, 'textSecondary')}
              showText
              size="middle"
            />
          </div>
        </Flex>
        
        <Divider>Previsualización</Divider>
        <div 
          style={{ 
            padding: '20px', 
            borderRadius: '8px', 
            background: colorPalette.surface, 
            border: `1px solid ${colorPalette.textSecondary}20`, // 20 is for opacity
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
          }}
        >
          <div style={{ color: colorPalette.text, fontSize: '18px', fontWeight: 'bold' }}>
            Previsualización de Colores
          </div>
          <div style={{ color: colorPalette.textSecondary, fontSize: '14px' }}>
            Este es un ejemplo de texto secundario
          </div>
          <div style={{ 
            padding: '10px', 
            borderRadius: '4px', 
            background: colorPalette.background,
            color: colorPalette.text
          }}>
            Este es un ejemplo de superficie sobre fondo
          </div>
          <Button 
            type="primary" 
            style={{ 
              background: colorPalette.primary, 
              borderColor: colorPalette.primary,
              width: 'fit-content'
            }}
          >
            Botón con color primario
          </Button>
        </div>
      </Space>
    </Card>
  );
};

export default ThemeSettings;