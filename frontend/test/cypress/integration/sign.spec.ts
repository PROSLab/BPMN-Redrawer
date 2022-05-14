import { LocalStorage } from 'quasar';

describe('Landing', () => {
  beforeEach(() => {
    LocalStorage.clear();
    cy.visit('/');
  });

  it('shows alerts', () => {
    cy.get('.q-dialog').should('not.exist');
    cy.get('.q-btn').contains('Sign').should('exist');
    const signBtn = cy.get('.q-btn').contains('Sign');
    signBtn.click().then(() => {
      cy.get('.q-dialog').should('exist');
      cy.get('.q-dialog').within(() => {
        cy.get('div[role="alert"]').should('have.length', 0);
        cy.get('input[type="email"]').type('abc');
        cy.get('div[role="alert"]').should('have.length', 1);
        cy.get('input[type="password"]').type('def');
        cy.get('div[role="alert"]').should('have.length', 2);
        cy.get('input[type="email"]').type('email@domain.com');
        cy.get('div[role="alert"]').should('have.length', 1);
        cy.get('input[type="password"]').type('password');
        cy.get('div[role="alert"]').should('have.length', 0);
      });
    });
  });

  it('closes if signin is successful', () => {
    cy.intercept(
      'POST',
      'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword**',
      {
        fixture: '../fixtures/signin1.json',
      }
    );

    cy.intercept(
      'POST',
      'https://identitytoolkit.googleapis.com/v1/accounts:lookup**',
      {
        fixture: '../fixtures/signin2.json',
      }
    );

    const signBtn = cy.get('.q-btn').contains('Sign');
    signBtn.click().then(() => {
      cy.get('.q-dialog').within(() => {
        cy.get('input[type="email"]').type('email@domain.com');
        cy.get('input[type="password"]').type('password');
        cy.get('.q-btn')
          .contains('Sign')
          .click()
          .then(() => {
            cy.get('.q-dialog').should('not.exist');
          });
      });
    });
  });

  it('redirects to home if signin is successful', () => {
    cy.intercept(
      'POST',
      'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword**',
      {
        fixture: '../fixtures/signin1.json',
      }
    );

    cy.intercept(
      'POST',
      'https://identitytoolkit.googleapis.com/v1/accounts:lookup**',
      {
        fixture: '../fixtures/signin2.json',
      }
    );

    cy.visit('#/editor');
    const signBtn = cy.get('.q-btn').contains('Sign');
    signBtn.click().then(() => {
      cy.get('.q-dialog').within(() => {
        cy.get('input[type="email"]').type('email@domain.com');
        cy.get('input[type="password"]').type('password');
        cy.get('.q-btn')
          .contains('Sign')
          .click()
          .then(() => {
            cy.testRoute('home');
          });
      });
    });
  });
});
