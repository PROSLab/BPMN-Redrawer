import { defineStore } from 'pinia';

// Pinia store for state management
export const useBpmnStore = defineStore('bpmn', {
  state: () => ({
    model: null as string | null,
    image: null as string | null,
  }),
});
