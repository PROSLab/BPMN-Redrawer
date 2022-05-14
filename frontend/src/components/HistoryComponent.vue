<template>
  <q-inner-loading :showing="loading">
    <q-spinner-gears size="50px" color="primary" />
    {{ $t('history.loading') }}
  </q-inner-loading>

  <div class="row justify-center">
    <div style="font-size: 32px">{{ $t('history.title') }}</div>
  </div>

  <q-timeline
    class="q-pl-md"
    layout="comfortable"
    side="right"
    color="secondary"
    v-if="!loading && timelineEntries.length != 0"
  >
    <q-timeline-entry
      side="right"
      v-for="t in timelineEntries"
      :key="t[0]"
      :title="'# ' + $t('history.conversions') + ': ' + t[1].length"
      :subtitle="t[0]"
    >
      <div v-for="e in t[1]" :key="e.id">
        {{ $t('history.date') }}: {{ e.timestamp }}
        <br />
        {{ $t('history.model') }}: {{ e.modelId }}
        <br />
        {{ $t('history.image') }}: {{ e.imageId }}
        <div class="q-pb-md">
          <q-btn
            color="primary"
            :label="$t('history.open')"
            @click="openInEditor(e)"
          ></q-btn>
        </div>
      </div>
    </q-timeline-entry>
  </q-timeline>

  <div v-else class="row justify-center">{{ $t('history.noConversions') }}</div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from 'vue';
import {
  storage,
  fbStorageRef,
  auth,
  fbDatabaseRef,
  database,
} from 'src/components/utils/firebase-utils';
import { getBytes } from 'firebase/storage';
import { useBpmnStore } from 'src/store/bpmnStore';
import { useQuasar } from 'quasar';
import { useRouter } from 'vue-router';
import { blobToDataURL } from 'src/components/utils/image-utils';
import { get as databaseGet } from 'firebase/database';
import { i18n } from 'src/boot/i18n';

export default defineComponent({
  name: 'HistoryComponent',

  setup() {
    const $q = useQuasar();
    const router = useRouter();
    const bpmnStore = useBpmnStore();
    const loading = ref(true);
    interface ConversionRecord {
      image_id: string;
      model_id: string;
    }
    interface TimelineEntry {
      imageId: string;
      modelId: string;
      timestamp: string;
      id: string;
    }
    const timelineEntries: Ref<[string, TimelineEntry[]][]> = ref([]);

    const databaseRef = fbDatabaseRef(database, auth.currentUser?.uid);

    // Get user conversion history from a Realtime Database query
    databaseGet(databaseRef)
      .then((res) => {
        if (!res.exists()) {
          loading.value = false;
          return;
        }
        const map = new Map<string, TimelineEntry[]>();
        const val = res.val() as { [index: string]: ConversionRecord };
        // Convert query result into a more appropriate data structure for the timeline
        Object.keys(val).forEach((cr) => {
          const timestamp = Number.parseInt(cr);
          const date = new Date(timestamp).toDateString();
          const entry: TimelineEntry = {
            imageId: val[cr].image_id,
            modelId: val[cr].model_id,
            timestamp: new Date(timestamp).toString(),
            id: `${auth.currentUser?.uid as string}@${timestamp}`,
          };
          if (map.has(date)) {
            map.get(date)?.push(entry);
          } else {
            map.set(date, [entry]);
          }
        });
        timelineEntries.value = Array.from(map.entries()).sort(
          (a, b) => new Date(b[0]).getTime() - new Date(a[0]).getTime()
        );
        timelineEntries.value.forEach((v) => v[1].reverse());
        loading.value = false;
      })
      .catch(() => {
        $q.notify({
          message: i18n.global.t('history.errorHistory'),
          type: 'negative',
        });
      });

    function openInEditor(entry: TimelineEntry) {
      const modelPath = `/models/${auth.currentUser?.uid as string}/${
        entry.modelId
      }`;
      const imagePath = `/images/${auth.currentUser?.uid as string}/${
        entry.imageId
      }`;
      const modelStorageRef = fbStorageRef(storage, modelPath);
      const imageStorageRef = fbStorageRef(storage, imagePath);
      const modelPromise = getBytes(modelStorageRef);
      const imagePromise = getBytes(imageStorageRef);
      $q.loading.show();
      // Retrieve model and original image
      Promise.all([modelPromise, imagePromise])
        .then((res) => {
          const decoder = new TextDecoder();
          const decodedModel = decoder.decode(res[0]);
          void blobToDataURL(new Blob([res[1]])).then((decodedImage) => {
            // Update the store and navigate to the editor
            bpmnStore.$patch({
              model: decodedModel,
              image: decodedImage,
              modelPath: modelPath,
              imagePath: imagePath,
            });
            void router.push({ name: 'editor' });
          });
        })
        .catch(() => {
          $q.notify({
            message: i18n.global.t('history.errorModelImage'),
            type: 'negative',
          });
        })
        .finally(() => $q.loading.hide());
    }

    return {
      loading,
      timelineEntries,
      openInEditor,
    };
  },
});
</script>
