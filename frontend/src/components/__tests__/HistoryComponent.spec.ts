import { api } from 'src/boot/axios';
import { mount } from '@cypress/vue';
import HistoryComponent from 'src/components/HistoryComponent.vue';

describe('HistoryComponent', () => {
  it.skip('remains loading in case of error', () => {
    cy.intercept(
      'GET',
      `${api.defaults.baseURL as string}/conversions/ric`,
      (req) => {
        req.destroy();
      }
    ).as('getData');

    const wrapper = mount(HistoryComponent);

    wrapper.get('.q-inner-loading').should('exist');
    wrapper.get('.q-inner-loading').should('be.visible');
    cy.wait('@getData');
    wrapper.get('.q-inner-loading').should('exist');
    wrapper.get('.q-inner-loading').should('be.visible');
  });

  it.skip('stops loading after receiving data', () => {
    cy.intercept('GET', `${api.defaults.baseURL as string}/conversions/ric`, {
      fixture: 'history_2_entries_different_records.json',
    }).as('getData');

    const wrapper = mount(HistoryComponent);

    wrapper.get('.q-inner-loading').should('exist');
    cy.wait('@getData');
    wrapper.get('.q-inner-loading').should('not.exist');
  });
});
