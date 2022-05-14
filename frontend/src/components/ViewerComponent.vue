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
    class="fill-height fill-width"
    ref="viewerDiv"
  >
    <viewer
      style="
        position: absolute;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
        border: 0;
      "
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
      class="viewer fill-height fill-width"
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
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from 'vue';
import 'viewerjs/dist/viewer.css';
import { component as Viewer } from 'v-viewer';
import { useBpmnStore } from 'src/store/bpmnStore';

export default defineComponent({
  name: 'ViewerComponent',

  components: { Viewer },

  setup() {
    const bpmnStore = useBpmnStore();
    const viewerDiv: Ref<HTMLElement | null> = ref(null);

    return {
      images: [bpmnStore.image],

      viewerDiv,

      // Handle resize
      resize() {
        viewerDiv.value?.dispatchEvent(new Event('resize', { bubbles: true }));
      },
    };
  },
});
</script>
