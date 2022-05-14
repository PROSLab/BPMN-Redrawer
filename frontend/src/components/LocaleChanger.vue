<template>
  <q-select
    dense
    outlined
    dark
    :options-dark="$q.dark.mode"
    :options="$i18n.availableLocales"
    v-model="$i18n.locale"
    @update:model-value="$q.localStorage.set('locale', $event)"
  >
  </q-select>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LocaleChanger',
});
</script>
