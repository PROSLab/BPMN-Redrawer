import { boot } from 'quasar/wrappers';
import { LocalStorage, Dark } from 'quasar';
import { i18n } from 'src/boot/i18n';

export default boot(() => {
  if (LocalStorage.has('dark')) {
    try {
      // Set dark mode back to what it was last time
      const dark = LocalStorage.getItem('dark') as boolean;
      Dark.set(dark);
    } catch {}
  }
  if (LocalStorage.has('locale')) {
    try {
      // Set locale back to what it was last time
      const locale = LocalStorage.getItem('locale') as string;
      i18n.global.locale = locale;
    } catch {}
  }
});
