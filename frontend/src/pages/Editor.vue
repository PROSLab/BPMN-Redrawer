<template>
  <q-page>
    <q-splitter
      v-if="bpmnStore.showImage"
      v-model="splitterModel"
      :limits="[0, 100]"
      style="
        position: absolute;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
        border: 0;
      "
    >
      <template v-slot:before>
        <editor-component></editor-component>
      </template>
      <template v-slot:separator>
        <q-avatar
          color="primary"
          text-color="white"
          size="40px"
          icon="drag_indicator"
        />
      </template>
      <template v-slot:after>
        <viewer-component></viewer-component>
      </template>
    </q-splitter>

    <editor-component v-else></editor-component>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import EditorComponent from 'src/components/EditorComponent.vue';
import ViewerComponent from 'src/components/ViewerComponent.vue';
import { useBpmnStore } from 'src/store/bpmnStore';

export default defineComponent({
  name: 'PageEditor',

  components: { EditorComponent, ViewerComponent },

  setup() {
    const bpmnStore = useBpmnStore();
    // Use a splitter to manage the size of the editor and the image viewer
    const splitterModel = ref(50);

    // Show the image viewer only if the store contains the image
    bpmnStore.showImage = bpmnStore.image != null;

    return {
      splitterModel,
      bpmnStore,
    };
  },
});
</script>
