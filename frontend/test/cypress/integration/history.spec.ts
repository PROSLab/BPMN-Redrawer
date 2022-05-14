describe('History tests', () => {
  beforeEach(function () {
    cy.visit('#/');
  });

  it.skip('displays 0 entries', () => {
    cy.intercept('GET', '**/conversions/ric', []);
    cy.visit('#/history');
    cy.get('.q-timeline__entry').should('have.length', 0);
  });

  it.skip('displays 1 entry with 1 record', () => {
    cy.intercept('GET', '**/conversions/ric', {
      fixture: '../fixtures/history_1_entry_1_record.json',
    });
    cy.visit('#/history');
    cy.get('.q-timeline__entry').as('entries');
    cy.get('@entries').should('have.length', 1);
    cy.get('.q-timeline__entry > .q-timeline__content > div').should(
      'have.length',
      1
    );
  });

  it.skip('displays 1 entry with 2 records', () => {
    cy.intercept('GET', '**/conversions/ric', {
      fixture: '../fixtures/history_1_entry_2_records.json',
    });
    cy.visit('#/history');
    cy.get('.q-timeline__entry').as('entries');
    cy.get('@entries').should('have.length', 1);
    cy.get('@entries')
      .find('.q-timeline__content > div')
      .should('have.length', 2);
  });

  it.skip('displays 2 entries with 1 record each', () => {
    cy.intercept('GET', '**/conversions/ric', {
      fixture: '../fixtures/history_2_entries_1_record.json',
    });
    cy.visit('#/history');
    cy.get('.q-timeline__entry').as('entries');
    cy.get('@entries').should('have.length', 2);
    cy.get('@entries').each((e) =>
      expect(e.find('.q-timeline__content > div')).to.have.length(1)
    );
  });

  it.skip('displays 2 entries with different number of records', () => {
    cy.intercept('GET', '**/conversions/ric', {
      fixture: '../fixtures/history_2_entries_different_records.json',
    });
    cy.visit('#/history');
    cy.get('.q-timeline__entry').as('entries');
    cy.get('@entries').should('have.length', 2);
    cy.get('@entries')
      .first()
      .find('.q-timeline__content > div')
      .should('have.length', 2);
    cy.get('@entries')
      .last()
      .find('.q-timeline__content > div')
      .should('have.length', 1);
  });

  it.skip('opens the editor', () => {
    cy.intercept('GET', '**/conversions/ric', {
      fixture: '../fixtures/history_1_entry_1_record.json',
    });
    cy.intercept('GET', '**bpmn?alt=media', {
      fixture: '../fixtures/test-model.bpmn',
    });
    cy.intercept('GET', '**png?alt=media', {
      fixture: '../fixtures/test-image.png',
    });
    cy.visit('#/history');
    cy.get('.q-timeline__entry .q-btn').click();
    cy.testRoute('editor');
  });
});
