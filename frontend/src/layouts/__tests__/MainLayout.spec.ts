import { mount } from '@cypress/vue';
import MainLayout from 'src/layouts/MainLayout.vue';

describe('MainLayout', () => {
  it('has not a drawer', () => {
    mount(MainLayout);
    cy.get('.q-drawer').should('not.exist');
  });

  it('has an "home" tab that leads to home', () => {
    mount(MainLayout);
    cy.get('.q-tab').eq(0).should('have.attr', 'href', '#/home');
  });

  it('has an "editor" tab that leads to editor', () => {
    mount(MainLayout);
    cy.get('.q-tab').eq(1).should('have.attr', 'href', '#/editor');
  });
});
