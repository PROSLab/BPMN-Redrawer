import { mount } from '@cypress/vue';
import MainLayout from 'src/layouts/MainLayout.vue';
import { useBpmnStore } from 'src/store/bpmnStore';

describe('MainLayout', () => {
  beforeEach(() => {
    const bpmnStore = useBpmnStore();
    bpmnStore.$reset();
  });

  it('has not a drawer if the user is not logged', () => {
    mount(MainLayout);
    cy.get('.q-drawer').should('not.exist');
  });

  it('has a drawer only if the user is logged', () => {
    const bpmnStore = useBpmnStore();
    mount(MainLayout);
    bpmnStore.logged = true;
    cy.get('.q-drawer').should('exist');
  });

  it('has a SignUp/SignIn button if the user is not logged', () => {
    mount(MainLayout);
    cy.get('.q-btn').should('contain.text', 'Sign');
  });

  it('has a Logout button if the user is logged', () => {
    const bpmnStore = useBpmnStore();
    mount(MainLayout);
    bpmnStore.logged = true;
    cy.get('.q-btn').should('contain.text', 'Logout');
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
