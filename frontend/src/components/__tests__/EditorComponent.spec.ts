import { mount } from '@cypress/vue';
import EditorComponent from 'src/components/EditorComponent.vue';
import { useBpmnStore } from 'src/store/bpmnStore';

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

  it('has an "exit" button that leads to home', () => {
    mount(EditorComponent);

    cy.get('.create-button').click();
    cy.get('.exit-button > .q-btn').should('have.attr', 'href', '#/home');
  });

  it('opens the bpmn-js editor', () => {
    const bpmnStore = useBpmnStore();

    cy.fixture('test-model.bpmn')
      .then((res) => {
        bpmnStore.model = res as string;
      })
      .fixture('test-image.png')
      .then((res) => {
        bpmnStore.image = res as string;
      });

    mount(EditorComponent);

    cy.get('.download-buttons').should('exist');
  });

  it('has the show image and the save model buttons', () => {
    const bpmnStore = useBpmnStore();
    const modelPath = 'test-model.bpmn';
    const imagePath = 'test-image.png';

    cy.fixture(modelPath)
      .then((res) => {
        bpmnStore.model = res as string;
        bpmnStore.modelPath = modelPath;
      })
      .fixture(imagePath)
      .then((res) => {
        bpmnStore.image = res as string;
        bpmnStore.imagePath = imagePath;
      });

    mount(EditorComponent);

    ['.control-buttons', '.show-image', '.save-model'].forEach((b) => {
      cy.get(b).should('exist');
      cy.get(b).should('be.visible');
    });
  });
});
