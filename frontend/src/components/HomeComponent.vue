<template>
  <div class="q-pa-md">
    <div style="margin: auto; text-align: center">
      <div style="font-size: 32px">{{ $t('home.welcome') }}</div>
      <div style="font-size: 18px">
        {{ $t('home.description') }}
      </div>
    </div>

    <q-file
      ref="filePicker"
      style="display: none"
      accept=".png, .jpeg, .jpg, .bmp"
      v-model="file"
      @update:model-value="loadImage(file as File)"
    ></q-file>
    <div class="q-pt-xl" style="text-align: center">
      <q-btn
        color="primary"
        icon="upload_file"
        :label="$t('home.load')"
        @click="filePicker?.pickFiles()"
      ></q-btn>
    </div>

    <q-dialog v-model="conversionDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <span class="q-ml-sm">{{ $t('home.converted') }}</span>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            icon="download"
            label="Download"
            color="primary"
            @click="downloadModel()"
          />
          <q-btn
            flat
            icon="arrow_forward"
            :label="$t('home.open')"
            color="primary"
            @click="editModel()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <div class="row justify-center q-pa-md" style="text-align: center">
      <div>
        <q-img
          :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
          sizes="(max-width: 400px) 400px, (max-height: 400px) 400px"
          fit="contain"
          position="50% 50%"
          width="400px"
          height="400px"
          placeholder-src="../assets/default-placeholder.png"
          no-spinner
          :src="(imgSrc as string)"
          @load="loadingOK"
          @error="loadingError"
          @dragover="allowDrop($event)"
          @drop="drop($event)"
        >
        </q-img>
      </div>
    </div>

    <div style="text-align: center">
      <q-checkbox
        class="q-pr-md"
        v-model="elementsEnabled"
        :label="$t('home.elements')"
      ></q-checkbox>
      <q-checkbox
        :disable="!elementsEnabled"
        class="q-pr-md"
        v-model="flowsEnabled"
        :label="$t('home.flows')"
      ></q-checkbox>
      <q-checkbox
        :disable="!elementsEnabled"
        class="q-pr-md"
        v-model="ocrEnabled"
        label="OCR"
      ></q-checkbox>
      <q-btn
        :disable="!imageLoaded"
        color="primary"
        icon-right="arrow_forward"
        :label="$t('home.convert')"
        @click="convertImage()"
      ></q-btn>
    </div>
  </div>

  <div class="q-pa-md" style="text-align: center">
    <div style="font-size: 18px">{{ $t('home.examples') }}</div>
    <div style="font-size: 14px">{{ $t('home.examplesInstruction') }}</div>
    <div class="row justify-evenly wrap">
      <div class="q-pa-sm" v-for="i in 3" :key="i">
        <q-img
          :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
          sizes="(max-width: 400px) 400px, (max-height: 400px) 400px"
          fit="contain"
          position="50% 50%"
          width="400px"
          height="400px"
          :src="require(`../assets/example${i}.png`)"
          @click="loadExampleImage(i)"
        >
        </q-img>
      </div>
    </div>
  </div>

  <div class="q-py-md" style="margin: auto; text-align: center; width: 100%">
    <div style="font-size: 18px">
      BPMN Redrawer
      <br />
      {{ $t('home.university') }}
      <br />
    </div>
    <div class="row justify-center">
      <q-img src="../assets/university-logo.png" width="173px" height="215px" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from 'vue';
import { exportFile, QFile, useQuasar } from 'quasar';
import { api } from 'src/boot/axios';
import { useRouter } from 'vue-router';
import { i18n } from 'src/boot/i18n';
import { blobToDataURL } from './utils/image-utils';
import axios from 'axios';
import { useBpmnStore } from 'src/store/bpmnStore';

export default defineComponent({
  name: 'HomeComponent',

  setup() {
    const $q = useQuasar();
    const router = useRouter();
    const filePicker: Ref<QFile | null> = ref(null);
    const file: Ref<File | null> = ref(null);
    const imageFile: Ref<File | null> = ref(null);
    const imgSrc: Ref<string | null> = ref(null);
    const conversionDialog: Ref<boolean> = ref(false);
    const conversionResult: Ref<string | null> = ref(null);
    const imageLoaded = ref(false);
    const elementsEnabled = ref(true);
    const flowsEnabled = ref(true);
    const ocrEnabled = ref(true);

    const allowDrop = (e: DragEvent) => {
      e.preventDefault();
    };

    const drop = async (e: DragEvent) => {
      e.preventDefault();
      const files = (e.dataTransfer as DataTransfer).files;
      if (files.length != 1) {
        return;
      }
      const file = files[0];
      if (
        file.name.endsWith('.png') ||
        file.name.endsWith('.jpeg') ||
        file.name.endsWith('.jpg') ||
        file.name.endsWith('.bmp')
      ) {
        await loadImage(file);
      }
    };

    const loadExampleImage = async (i: number) => {
      const blob = await (
        await fetch(
          // eslint-disable-next-line @typescript-eslint/no-var-requires
          require(`../assets/example${i}.png`) as string
        )
      ).blob();
      await loadImage(new File([blob], `example${i}.png`));
    };

    const loadImage = async (fileToLoad: File) => {
      await blobToDataURL(fileToLoad)
        .then((result) => {
          imgSrc.value = result;
          imageLoaded.value = true;
          imageFile.value = fileToLoad;
        })
        .catch(() => {
          imgSrc.value = null;
          imageLoaded.value = false;
          $q.notify({
            message: i18n.global.t('home.errorReading'),
            type: 'negative',
          });
          imageFile.value = null;
        });
      file.value = null;
    };

    const loadingOK = () => {
      $q.notify({
        message: i18n.global.t('home.loaded'),
        type: 'positive',
      });
    };

    const loadingError = () => {
      imgSrc.value = null;
      imageLoaded.value = false;
      $q.notify({
        message: i18n.global.t('home.errorLoading'),
        type: 'negative',
      });
      file.value = null;
      imageFile.value = null;
    };

    const editModel = async () => {
      const bpmnStore = useBpmnStore();
      const image = await blobToDataURL(new Blob([imageFile.value as File]));
      const model = conversionResult.value;
      bpmnStore.image = image;
      bpmnStore.model = model;
      await router.push({
        name: 'editor',
      });
    };

    const downloadModel = () => {
      exportFile(
        (imageFile.value?.name as string) + '.bpmn',
        conversionResult.value as string,
        {
          mimeType: 'text/xml',
          encoding: 'utf-8',
        }
      );
    };

    const convertImage = async () => {
      const formData = new FormData();
      formData.append('image', imageFile.value as File);
      formData.append('elements', String(elementsEnabled.value));
      formData.append('flows', String(flowsEnabled.value));
      formData.append('ocr', String(ocrEnabled.value));
      const source = axios.CancelToken.source();
      const uploadDialog = $q
        .dialog({
          message: i18n.global.t('home.uploading'),
          progress: true,
          persistent: true,
          ok: false,
          cancel: true,
        })
        .onCancel(() => {
          source.cancel();
        });

      await api
        .post<string>('/convert', formData, {
          cancelToken: source.token,
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (progressEvent: ProgressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            );
            uploadDialog.update({
              message:
                progress == 100
                  ? i18n.global.t('home.waitingForConversion')
                  : i18n.global.t('home.uploadingProgress', {
                      progress: progress,
                    }),
            });
          },
        })
        .then((res) => {
          uploadDialog.hide();
          conversionResult.value = res.data;
          conversionDialog.value = true;
        })
        .catch(() => {
          uploadDialog.hide();
          $q.notify({
            message: i18n.global.t('home.errorUploading'),
            type: 'negative',
          });
        });
    };

    return {
      api,
      allowDrop,
      drop,
      imgSrc,
      filePicker,
      file,
      imageFile,
      imageLoaded,
      loadingOK,
      loadingError,
      editModel,
      downloadModel,
      loadImage,
      loadExampleImage,
      convertImage,
      conversionDialog,
      elementsEnabled,
      flowsEnabled,
      ocrEnabled,
    };
  },
});
</script>
