import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UiState {
  theme: 'light' | 'dark';
  colorPalette: {
    primary: string;
    secondary: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
  };
  sidebarCollapsed: boolean;
}

const initialState: UiState = {
  theme: 'light',
  colorPalette: {
    primary: '#1890ff', // Azul estándar de Ant Design
    secondary: '#13c2c2', // Turquesa
    background: '#f0f2f5', // Gris claro
    surface: '#ffffff', // Blanco
    text: '#000000', // Negro
    textSecondary: '#595959', // Gris oscuro
  },
  sidebarCollapsed: false,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.theme = state.theme === 'light' ? 'dark' : 'light';
      
      // Actualizar paleta de colores según el tema
      if (state.theme === 'dark') {
        state.colorPalette = {
          primary: '#177ddc',
          secondary: '#00a896',
          background: '#0a0a0a',
          surface: '#141414',
          text: '#ffffff',
          textSecondary: '#aaaaaa',
        };
      } else {
        state.colorPalette = {
          primary: '#1890ff',
          secondary: '#13c2c2',
          background: '#f0f2f5',
          surface: '#ffffff',
          text: '#000000',
          textSecondary: '#595959',
        };
      }
    },
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
      
      // Actualizar paleta de colores según el tema
      if (action.payload === 'dark') {
        state.colorPalette = {
          primary: '#177ddc',
          secondary: '#00a896',
          background: '#0a0a0a',
          surface: '#141414',
          text: '#ffffff',
          textSecondary: '#aaaaaa',
        };
      } else {
        state.colorPalette = {
          primary: '#1890ff',
          secondary: '#13c2c2',
          background: '#f0f2f5',
          surface: '#ffffff',
          text: '#000000',
          textSecondary: '#595959',
        };
      }
    },
    setColorPalette: (state, action: PayloadAction<Partial<UiState['colorPalette']>>) => {
      state.colorPalette = {
        ...state.colorPalette,
        ...action.payload,
      };
    },
    toggleSidebar: (state) => {
      state.sidebarCollapsed = !state.sidebarCollapsed;
    },
    setSidebarCollapsed: (state, action: PayloadAction<boolean>) => {
      state.sidebarCollapsed = action.payload;
    },
  },
});

export const { 
  toggleTheme, 
  setTheme, 
  setColorPalette, 
  toggleSidebar, 
  setSidebarCollapsed 
} = uiSlice.actions;

export default uiSlice.reducer;