<template>
  <q-toggle
    class="q-mr-md"
    :label="$t('main.dark')"
    color="white"
    v-model="$q.dark.mode"
    @update:model-value="
      $q.dark.set($event);
      $q.localStorage.set('dark', $event);
    "
  ></q-toggle>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'DarkModeChanger',
});
</script>
