import { LocalStorage } from 'quasar';

describe('Landing', () => {
  beforeEach(() => {
    LocalStorage.clear();
    cy.visit('/');
  });

  it('includes "BPMN" in the title', () => {
    cy.title().should('include', 'BPMN');
  });

  it('shows a placeholder image', () => {
    cy.fixture('placeholder.png').then((placeholder: string) => {
      cy.get('.q-img__image')
        .eq(1)
        .should('have.attr', 'src')
        .and('contain', placeholder);
    });
  });

  it('has a tab for home and for the editor', () => {
    const homeTab = cy.get('.q-tab').first();
    homeTab.should('have.attr', 'href', '#/home');
    cy.testRoute('home');
    const editorTab = cy.get('.q-tab').last();
    editorTab.should('have.attr', 'href', '#/editor');
    editorTab.click().then(() => {
      cy.testRoute('editor');
      const newHomeTab = cy.get('.q-tab').first();
      newHomeTab.click().then(() => {
        cy.testRoute('home');
      });
    });
  });

  it('has support for different locales', () => {
    cy.get('div').should('contain', 'Welcome');
    cy.get('div').should('not.contain', 'Benvenuti');
    cy.get('.q-menu').should('not.exist');
    cy.get('.q-select')
      .click()
      .then(() => {
        cy.get('.q-menu').should('exist');
        cy.get('.q-item')
          .first()
          .click()
          .then(() => {
            cy.get('div').should('contain', 'Welcome');
            cy.get('div').should('not.contain', 'Benvenuti');
            cy.get('.q-select')
              .click()
              .then(() => {
                cy.get('.q-item')
                  .last()
                  .click()
                  .then(() => {
                    cy.get('div').should('contain', 'Benvenuti');
                    cy.get('div').should('not.contain', 'Welcome');
                  });
              });
          });
      });
  });

  it('has support for dark mode', () => {
    cy.get('div').contains('Welcome').should('have.color', 'black');
    cy.get('.q-toggle').click();
    cy.get('div').contains('Welcome').should('have.color', 'white');
  });

  it('should remember locale and dark mode preferences', () => {
    assert(LocalStorage.isEmpty());
    cy.reload();
    assert(LocalStorage.isEmpty());
    cy.get('.q-select')
      .click()
      .then(() => {
        cy.get('.q-item')
          .last()
          .click()
          .then(() => {
            assert(!LocalStorage.isEmpty());
            assert(LocalStorage.getLength() == 1);
            assert(LocalStorage.has('locale'));
            assert((LocalStorage.getItem('locale') as string) == 'it-IT');
            cy.get('.q-toggle')
              .click()
              .then(() => {
                assert(LocalStorage.getLength() == 2);
                assert(LocalStorage.has('dark'));
                assert((LocalStorage.getItem('dark') as boolean) == true);
                cy.get('div')
                  .contains('BPMN Redrawer')
                  .should('have.color', 'white');
                cy.reload().then(() => {
                  assert((LocalStorage.getItem('locale') as string) == 'it-IT');
                  assert((LocalStorage.getItem('dark') as boolean) == true);
                  cy.get('div').should('contain', 'Benvenuti');
                  cy.get('div')
                    .contains('BPMN Redrawer')
                    .should('have.color', 'white');
                });
              });
          });
      });
  });
});
