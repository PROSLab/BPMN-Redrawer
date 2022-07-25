<template>
  <div class="absolute-full" @dragover="allowDrop($event)" @drop="drop($event)">
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
            @update:model-value="uploadDiagram(pickedFile as File)"
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
      <q-file
        ref="bpmnFilePicker"
        style="display: none"
        accept=".bpmn"
        v-model="bpmnFile"
        @update:model-value="uploadDiagram(bpmnFile as File)"
      ></q-file>
      <li>
        <q-btn
          icon="upload"
          label="BPMN"
          outline
          @click="bpmnFilePicker?.pickFiles()"
        />
      </li>
      <li>
        <q-btn icon="download" label="BPMN" outline @click="downloadAsBPMN" />
      </li>
      <li>
        <q-btn icon="download" label="SVG" outline @click="downloadAsSVG" />
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, Ref, onUnmounted } from 'vue';
import { useQuasar, QFile, exportFile } from 'quasar';
import 'bpmn-js/dist/assets/diagram-js.css';
import 'bpmn-js/dist/assets/bpmn-font/css/bpmn-embedded.css';
import Modeler from 'bpmn-js/lib/Modeler';
import { onBeforeRouteLeave } from 'vue-router';
import { i18n } from 'src/boot/i18n';
import { useBpmnStore } from 'src/store/bpmnStore';

export default defineComponent({
  name: 'EditorComponent',

  setup() {
    const $q = useQuasar();
    const bpmnStore = useBpmnStore();
    const filePicker: Ref<QFile | null> = ref(null);
    const pickedFile: Ref<File | null> = ref(null);
    const bpmnFilePicker: Ref<QFile | null> = ref(null);
    const bpmnFile: Ref<File | null> = ref(null);
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
      modeler.detach();
    });

    const allowDrop = (e: DragEvent) => {
      e.preventDefault();
    };

    const drop = async (e: DragEvent) => {
      e.preventDefault();
      const files = e.dataTransfer?.files;
      if (files?.length == 1) {
        if (files[0].name.endsWith('.bpmn')) {
          await openDiagram(await files[0].text());
        }
      }
    };

    return {
      allowDrop,
      drop,
      filePicker,
      pickedFile,
      bpmnFilePicker,
      bpmnFile,
      successfulLoadBPMN,

      async downloadAsBPMN() {
        try {
          const { xml } = await modeler.saveXML({ format: true });
          exportFile('diagram.bpmn', xml);
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
          exportFile('diagram.svg', svg);
        } catch (err) {
          $q.notify({
            message: i18n.global.t('editor.errorSaveSVG'),
            type: 'negative',
          });
        }
      },

      // When creating a new diagram, just open the default one
      createNewDiagram() {
        const sampleDiagram =
          '<?xml version="1.0" encoding="UTF-8"?><bpmn2:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xsi:schemaLocation="http://www.omg.org/spec/BPMN/20100524/MODEL BPMN20.xsd" id="sample-diagram" targetNamespace="http://bpmn.io/schema/bpmn"><bpmn2:process id="Process_1" isExecutable="false"><bpmn2:startEvent id="StartEvent_1" /></bpmn2:process><bpmndi:BPMNDiagram id="BPMNDiagram_1"><bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1"><bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1"><dc:Bounds height="36.0" width="36.0" x="412.0" y="240.0" /></bpmndi:BPMNShape></bpmndi:BPMNPlane></bpmndi:BPMNDiagram></bpmn2:definitions>';
        void openDiagram(sampleDiagram);
      },

      uploadDiagram(file: File) {
        const reader = new FileReader();
        reader.onload = (res) => {
          void openDiagram(res.target?.result as string);
        };
        reader.onerror = () => {
          $q.notify({
            message: i18n.global.t('editor.errorUpload'),
            type: 'negative',
          });
        };
        reader.readAsText(file, 'utf8');
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
