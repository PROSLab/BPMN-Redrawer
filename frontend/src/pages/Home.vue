<template>
  <q-page>
    <home-component></home-component>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import HomeComponent from 'src/components/HomeComponent.vue';

export default defineComponent({
  name: 'PageHome',

  components: { HomeComponent },
});
</script>
