<template>
  <div
    style="
      position: absolute;
      width: 100%;
      height: 100%;
      padding: 0;
      margin: 0;
      border: 0;
    "
  >
    <div class="content" id="js-drop-zone">
      <div class="message intro">
        <div class="note">
          <q-btn
            class="drop-button"
            disable
            outline
            :label="$t('editor.drop')"
          />
          /
          <q-file
            ref="filePicker"
            style="display: none"
            accept=".bpmn"
            v-model="pickedFile"
            @update:model-value="uploadDiagram()"
          ></q-file>
          <q-btn
            class="open-button"
            outline
            :label="$t('editor.open')"
            @click="filePicker?.pickFiles()"
          />
          /
          <q-btn
            class="create-button"
            outline
            :label="$t('editor.create')"
            @click="createNewDiagram"
          />
          {{ $t('editor.intro') }}
        </div>
      </div>

      <div class="message error">
        <div class="note">
          <p>Ooops, we could not display the BPMN 2.0 diagram.</p>

          <div class="details">
            <span>cause of the problem</span>
            <pre></pre>
          </div>
        </div>
      </div>

      <div class="canvas" id="js-canvas"></div>
    </div>

    <ul class="download-buttons" v-if="successfulLoadBPMN">
      <li>Download</li>
      <li>
        <q-btn icon="download" label="BPMN" outline @click="downloadAsBPMN" />
      </li>
      <li>
        <q-btn icon="download" label="SVG" outline @click="downloadAsSVG" />
      </li>
    </ul>

    <ul class="exit-button" v-if="successfulLoadBPMN">
      <q-btn icon="exit_to_app" size="16px" :to="{ name: 'home' }" flat />
    </ul>

    <div class="control-buttons row">
      <q-btn
        v-if="bpmnStore.image"
        class="show-image"
        :icon="bpmnStore.showImage ? 'image_not_supported' : 'image'"
        size="16px"
        flat
        @click="bpmnStore.showImage = !bpmnStore.showImage"
      />
      <q-separator size="2px" vertical></q-separator>
      <q-btn
        v-if="bpmnStore.modelPath && bpmnStore.imagePath"
        class="save-model"
        icon="save"
        size="16px"
        flat
        @click="saveModifiedModel()"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, Ref, onUnmounted } from 'vue';
import { debounce, useQuasar, QFile } from 'quasar';
import 'bpmn-js/dist/assets/diagram-js.css';
import 'bpmn-js/dist/assets/bpmn-font/css/bpmn-embedded.css';
import Modeler from 'bpmn-js/lib/Modeler';
import { downloadModel, sampleDiagram } from 'src/components/utils/bpmn-utils';
import { useBpmnStore } from 'src/store/bpmnStore';
import { onBeforeRouteLeave } from 'vue-router';
import { storage, fbStorageRef } from 'src/components/utils/firebase-utils';
import { uploadBytes } from 'firebase/storage';
import { i18n } from 'src/boot/i18n';

export default defineComponent({
  name: 'EditorComponent',

  setup() {
    const $q = useQuasar();
    const bpmnStore = useBpmnStore();
    const filePicker: Ref<QFile | null> = ref(null);
    const pickedFile: Ref<File | null> = ref(null);
    const successfulLoadBPMN = ref(false);

    let container: HTMLElement | null;
    let modeler: Modeler;

    async function openDiagram(xml: string) {
      try {
        await modeler.importXML(xml);
        container?.classList.remove('with-error');
        container?.classList.add('with-diagram');
        successfulLoadBPMN.value = true;
      } catch (err) {
        container?.classList.remove('with-diagram');
        container?.classList.add('with-error');
        const errorNode = container?.querySelectorAll('.error pre')[0];
        (errorNode as Element).textContent = (err as Error).message;
        successfulLoadBPMN.value = false;
      }
    }

    function registerFileDrop(callback: (xml: string) => Promise<void>) {
      function handleFileSelect(e: Event) {
        e.stopPropagation();
        e.preventDefault();

        const file = (e as DragEvent).dataTransfer?.files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
          const xml = e.target?.result;
          void callback(xml as string);
        };
        try {
          reader.readAsText(file as File);
        } catch (err) {
          console.error(err);
        }
      }

      function handleDragOver(e: Event) {
        e.stopPropagation();
        e.preventDefault();

        ((e as DragEvent).dataTransfer as DataTransfer).dropEffect = 'copy';
      }

      container
        ?.getElementsByClassName('message intro')[0]
        .addEventListener('dragover', handleDragOver, false);
      container
        ?.getElementsByClassName('message intro')[0]
        .addEventListener('drop', handleFileSelect, false);
    }

    // Ask for confirmation before leaving the editor
    onBeforeRouteLeave((_to, _from, next) => {
      if (!successfulLoadBPMN.value) {
        next();
        return;
      }
      $q.dialog({
        message: i18n.global.t('editor.exit'),
        cancel: true,
      })
        .onOk(() => {
          bpmnStore.$patch({
            model: null,
            image: null,
            modelPath: null,
            imagePath: null,
          });
          next();
        })
        .onCancel(() => next(false));
    });

    onMounted(() => {
      container = document.getElementById('js-drop-zone');
      modeler = new Modeler({
        container: '#js-canvas',
        // Enable bpmn-js keyboard shortcuts
        keyboard: { bindTo: document },
      });
      // Save changes to bpmn model
      modeler.on(
        'commandStack.changed',
        debounce(() => {
          void modeler.saveXML({ format: true }).then((data) => {
            bpmnStore.model = data.xml;
          });
        }, 500)
      );
      if (!window.FileList || !window.FileReader) {
        $q.notify({
          message:
            'Looks like you use an older browser that does not support drag and drop. Try using Chrome, Firefox or the Internet Explorer > 10.',
          type: 'negative',
        });
      } else {
        registerFileDrop(openDiagram);
      }

      if (bpmnStore.model) {
        void openDiagram(bpmnStore.model);
      }
    });

    // Detach the bpmn-js modeler from parent when changing page
    onUnmounted(() => {
      modeler.off('commandStack.changed');
      modeler.detach();
    });

    return {
      filePicker,
      pickedFile,
      successfulLoadBPMN,
      bpmnStore,

      async downloadAsBPMN() {
        try {
          const { xml } = await modeler.saveXML({ format: true });
          downloadModel('diagram.bpmn', xml);
        } catch (err) {
          $q.notify({
            message: i18n.global.t('editor.errorSaveBPMN'),
            type: 'negative',
          });
        }
      },

      async downloadAsSVG() {
        try {
          const { svg } = await modeler.saveSVG();
          downloadModel('diagram.svg', svg);
        } catch (err) {
          $q.notify({
            message: i18n.global.t('editor.errorSaveSVG'),
            type: 'negative',
          });
        }
      },

      // When creating a new diagram, just open the default one
      createNewDiagram() {
        void openDiagram(sampleDiagram);
      },

      uploadDiagram() {
        const fileValue = pickedFile?.value;
        const reader = new FileReader();
        // Accept only .bpmn files
        if (fileValue?.name.match(/\.bpmn$/i)) {
          reader.onload = (res) => {
            void openDiagram(res.target?.result as string);
          };
          reader.onerror = () => {
            $q.notify({
              message: i18n.global.t('editor.errorUpload'),
              type: 'negative',
            });
          };
          reader.readAsText(fileValue, 'utf8');
        }
      },

      saveModifiedModel() {
        const modelStorageRef = fbStorageRef(
          storage,
          bpmnStore.modelPath as string
        );
        modeler
          .saveXML({ format: true })
          .then((xmlRes) => {
            // Overwrite the model on Firebase
            uploadBytes(modelStorageRef, new TextEncoder().encode(xmlRes.xml))
              .then(() => {
                $q.notify({
                  message: i18n.global.t('editor.savedChanges'),
                  type: 'positive',
                });
              })
              .catch(() => {
                $q.notify({
                  message: i18n.global.t('editor.errorSaveChanges'),
                  type: 'negative',
                });
              });
          })
          .catch(() => {
            $q.notify({
              message: i18n.global.t('editor.errorSaveChanges'),
              type: 'negative',
            });
          });
      },
    };
  },
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}
body,
html {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 12px;
  height: 100%;
  padding: 0;
  margin: 0;
}
a:link {
  text-decoration: none;
}
.content,
.content > div {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.content > .message {
  text-align: center;
  display: table;
  font-size: 16px;
}
.content > .message .note {
  vertical-align: middle;
  text-align: center;
  display: table-cell;
}
.content .error .details {
  max-width: 500px;
  font-size: 12px;
  margin: 20px auto;
  text-align: left;
}
.content .error pre {
  border: solid 1px #ccc;
  background: #eee;
  padding: 10px;
}
.content:not(.with-error) .error,
.content.with-error .intro,
.content.with-diagram .intro {
  display: none;
}
.content .canvas,
.content.with-error .canvas {
  visibility: hidden;
}
.content.with-diagram .canvas {
  visibility: visible;
}
.control-buttons {
  position: absolute;
  transform: translateX(-50%);
  top: 10px;
  left: 50%;
  border: 1px solid #cccccc;
  border-radius: 2px;
}
.exit-button {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0;
  margin: 0;
  border: 1px solid #cccccc;
  border-radius: 2px;
}
.download-buttons {
  position: absolute;
  bottom: 10px;
  left: 75px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.download-buttons > li {
  display: inline-block;
  margin-right: 10px;
}
.download-buttons > li > a {
  background: #ddd;
  border: solid 1px #666;
  display: inline-block;
  padding: 5px;
}
.download-buttons a {
  opacity: 0.3;
}
.download-buttons a.active {
  opacity: 1;
}
</style>
