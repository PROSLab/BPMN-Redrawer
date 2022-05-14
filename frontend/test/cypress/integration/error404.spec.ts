describe('Error404 page tests', () => {
  beforeEach(() => {
    cy.visit('#/non-existing');
  });

  it('remains in the non-existing page but returns a 404 page', () => {
    cy.testRoute('non-existing');
    cy.get('div').should('contain.text', '404');
  });

  it('navigates to home when clicking on the button', () => {
    cy.get('.q-btn').click();
    cy.testRoute('home');
  });
});
