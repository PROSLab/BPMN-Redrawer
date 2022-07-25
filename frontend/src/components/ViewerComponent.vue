<template>
  <div
    class="absolute-full"
    ref="viewerDiv"
    @dragover="allowDrop($event)"
    @drop="drop($event)"
  >
    <viewer
      class="absolute-full viewer"
      :options="{
        inline: true,
        button: false,
        navbar: false,
        title: false,
        toolbar: false,
        tooltip: false,
        movable: true,
        zoomable: true,
        rotatable: false,
        scalable: true,
        transition: false,
        fullscreen: true,
        keyboard: false,
      }"
      :images="images"
      ref="viewer"
    >
      <template #default="scope">
        <img
          style="display: none"
          v-for="src in scope.images"
          :src="src"
          :key="src"
        />
      </template>
    </viewer>

    <q-resize-observer debounce="250" @resize="resize()"></q-resize-observer>

    <div>
      <q-file
        ref="filePicker"
        style="display: none"
        accept=".png, .jpeg, .jpg, .bmp"
        v-model="file"
        @update:model-value="loadImage(file)"
      ></q-file>
      <div class="row justify-center q-pt-md">
        <q-btn
          outline
          icon="file_upload"
          :label="$t('editor.load')"
          @click="filePicker.pickFiles()"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from 'vue';
import 'viewerjs/dist/viewer.css';
import { component as Viewer } from 'v-viewer';
import { QFile } from 'quasar';
import { blobToDataURL } from './utils/image-utils';
import { useBpmnStore } from 'src/store/bpmnStore';

export default defineComponent({
  name: 'ViewerComponent',

  components: { Viewer },

  setup() {
    const bpmnStore = useBpmnStore();
    const viewerDiv: Ref<HTMLElement | null> = ref(null);
    const filePicker: Ref<QFile | null> = ref(null);
    const file: Ref<File | null> = ref(null);
    const images = ref([bpmnStore.image]);

    const loadImage = async (file: File) => {
      const image = await blobToDataURL(new Blob([file]));
      images.value = [image];
    };

    const allowDrop = (e: DragEvent) => {
      e.preventDefault();
    };

    const drop = async (e: DragEvent) => {
      e.preventDefault();
      const files = e.dataTransfer?.files;
      if (files?.length == 1) {
        const fileType = files[0].type;
        if (
          fileType == 'image/png' ||
          fileType == 'image/jpeg' ||
          fileType == 'image/bmp'
        ) {
          await loadImage(files[0]);
        }
      }
    };

    return {
      allowDrop,
      drop,
      filePicker,
      file,
      images,
      viewerDiv,
      loadImage,

      // Handle resize
      resize() {
        viewerDiv.value?.dispatchEvent(new Event('resize', { bubbles: true }));
      },
    };
  },
});
</script>
