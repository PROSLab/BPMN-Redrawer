<template>
  <q-page>
    <history-component></history-component>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import HistoryComponent from 'src/components/HistoryComponent.vue';

export default defineComponent({
  name: 'PageHistory',

  components: { HistoryComponent },
});
</script>
