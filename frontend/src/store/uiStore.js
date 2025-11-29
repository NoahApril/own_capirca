import { create } from 'zustand';

export const useUIStore = create((set) => ({
  theme: 'dark',
  sidebarCollapsed: false,
  currentServiceId: null,
  
  toggleTheme: () => set((state) => ({
    theme: state.theme === 'dark' ? 'light' : 'dark'
  })),
  
  toggleSidebar: () => set((state) => ({
    sidebarCollapsed: !state.sidebarCollapsed
  })),
  
  setCurrentService: (id) => set({ currentServiceId: id }),
}));
