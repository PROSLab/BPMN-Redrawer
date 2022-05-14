import { boot } from 'quasar/wrappers';
import { createPinia } from 'pinia';

// Create Pinia instance to manage stores for state management
const pinia = createPinia();

export default boot(({ app }) => {
  app.use(pinia);
});

export { pinia };
