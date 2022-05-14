import { defineStore } from 'pinia';

// Pinia store for state management
export const useBpmnStore = defineStore('bpmn', {
  state: () => ({
    model: null as string | null,
    image: null as string | null,
    modelPath: null as string | null,
    imagePath: null as string | null,
    showImage: false,
    logged: false,
  }),
});
