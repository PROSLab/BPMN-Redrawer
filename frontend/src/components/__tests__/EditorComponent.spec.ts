import { mount } from '@cypress/vue';
import EditorComponent from 'src/components/EditorComponent.vue';

describe('EditorComponent', () => {
  it('has different buttons to load a diagram', () => {
    mount(EditorComponent);

    cy.get('.drop-button').should('exist');
    cy.get('.open-button').should('exist');
    cy.get('.create-button').should('exist');
  });

  it("doesn't show the editor when launching it without data", () => {
    mount(EditorComponent);

    const hiddenClasses = ['.canvas', '.djs-palette'];
    hiddenClasses.forEach((c) => void cy.get(c).should('not.be.visible'));
    const nonExistingClasses = ['.exit-button', '.download-buttons'];
    nonExistingClasses.forEach((c) => void cy.get(c).should('not.exist'));
  });
});
