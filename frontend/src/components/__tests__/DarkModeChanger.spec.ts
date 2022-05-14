import { mount } from '@cypress/vue';
import { LocalStorage, Dark } from 'quasar';
import DarkModeChanger from 'src/components/DarkModeChanger.vue';

describe('DarkModeChanger', () => {
  beforeEach(() => {
    LocalStorage.clear();
    Dark.set(false);
  });

  it('it is not dark at boot', () => {
    mount(DarkModeChanger);
    assert(!Dark.isActive.valueOf());
  });

  it('it toggles dark mode', () => {
    mount(DarkModeChanger);
    assert(!Dark.isActive.valueOf());
    cy.get('.q-toggle')
      .click()
      .then(() => {
        assert(Dark.isActive.valueOf());
      });
    cy.get('.q-toggle')
      .click()
      .then(() => {
        assert(!Dark.isActive.valueOf());
      });
  });

  it('it creates a LocalStorage key', () => {
    mount(DarkModeChanger);
    assert(LocalStorage.isEmpty());
    cy.get('.q-toggle')
      .click()
      .then(() => {
        assert(!LocalStorage.isEmpty());
      });
  });

  it('it toggles LocalStorage dark mode', () => {
    mount(DarkModeChanger);
    assert(LocalStorage.isEmpty());
    cy.get('.q-toggle')
      .click()
      .then(() => {
        assert(!LocalStorage.isEmpty());
        assert(LocalStorage.has('dark'));
        assert((LocalStorage.getItem('dark')?.valueOf() as boolean) == true);
        cy.get('.q-toggle')
          .click()
          .then(() => {
            assert(LocalStorage.has('dark'));
            assert(
              (LocalStorage.getItem('dark')?.valueOf() as boolean) == false
            );
          });
      });
  });
});
