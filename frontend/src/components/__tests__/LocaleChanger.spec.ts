import { mount } from '@cypress/vue';
import { LocalStorage } from 'quasar';
import { i18n } from 'src/boot/i18n';
import LocaleChanger from 'src/components/LocaleChanger.vue';

describe('LocaleChanger', () => {
  beforeEach(() => {
    LocalStorage.clear();
    i18n.global.locale = 'en-US';
  });

  it('it is localized to english at boot', () => {
    mount(LocaleChanger);
    assert(i18n.global.locale == 'en-US');
  });

  it('it changes locale', () => {
    mount(LocaleChanger);
    assert(i18n.global.locale == 'en-US');
    cy.get('.q-menu').should('not.exist');
    cy.get('.q-select')
      .click()
      .then(() => {
        cy.get('.q-menu').should('exist');
        cy.get('.q-item')
          .last()
          .click()
          .then(() => {
            assert(i18n.global.locale == 'it-IT');
            cy.get('.q-menu').should('not.exist');
            cy.get('.q-select')
              .click()
              .then(() => {
                cy.get('.q-menu').should('exist');
                cy.get('.q-item')
                  .first()
                  .click()
                  .then(() => {
                    assert(i18n.global.locale == 'en-US');
                  });
              });
          });
      });
  });

  it('it creates a LocalStorage key', () => {
    mount(LocaleChanger);
    assert(LocalStorage.isEmpty());
    cy.get('.q-select')
      .click()
      .then(() => {
        assert(LocalStorage.isEmpty());
        cy.get('.q-item')
          .last()
          .click()
          .then(() => {
            assert(!LocalStorage.isEmpty());
          });
      });
  });

  it('it changes LocalStorage locale', () => {
    mount(LocaleChanger);
    assert(LocalStorage.isEmpty());
    cy.get('.q-select')
      .click()
      .then(() => {
        assert(LocalStorage.isEmpty());
        cy.get('.q-item')
          .last()
          .click()
          .then(() => {
            assert(!LocalStorage.isEmpty());
            assert(LocalStorage.has('locale'));
            assert(
              (LocalStorage.getItem('locale')?.valueOf() as string) == 'it-IT'
            );
            cy.get('.q-select')
              .click()
              .then(() => {
                assert(
                  (LocalStorage.getItem('locale')?.valueOf() as string) ==
                    'it-IT'
                );
                cy.get('.q-item')
                  .first()
                  .click()
                  .then(() => {
                    assert(
                      (LocalStorage.getItem('locale')?.valueOf() as string) ==
                        'en-US'
                    );
                  });
              });
          });
      });
  });
});
