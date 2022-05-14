import { mount } from '@cypress/vue';
import Error404 from 'src/pages/Error404.vue';

describe('Error404', () => {
  it('shows a 404 error page', () => {
    mount(Error404);

    cy.get('.error-404').should('exist');
    cy.get('.error-404').should('contain', '404');
  });

  it('has a button that leads to home', () => {
    mount(Error404);

    cy.get('.q-btn').should('exist');
    cy.get('.q-btn').should('have.attr', 'href', '#/home');
  });
});
