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
      @update:model-value="loadImage()"
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
            @click="downloadModel('diagram.bpmn', conversionResult)"
          />
          <q-btn
            flat
            icon="arrow_forward"
            :label="$t('home.open')"
            color="primary"
            :to="{ name: 'editor' }"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <div class="q-pa-md" style="text-align: center">
      <q-img
        style="border: 3px black solid; margin: auto"
        sizes="(max-width: 400px) 400px, (max-height: 400px) 400px"
        fit="contain"
        position="50% 50%"
        width="400px"
        height="400px"
        placeholder-src="../assets/default-placeholder.png"
        no-spinner
        :src="imgSrc"
        @load="loadingOK"
        @error="loadingError"
      >
      </q-img>
    </div>

    <div style="text-align: center">
      <q-checkbox class="q-pr-md" v-model="ocrEnabled" label="OCR"></q-checkbox>
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
          style="border: 3px black solid; margin: auto"
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

  <div class="q-pt-md" style="margin: auto; text-align: center; width: 100%">
    <div style="font-size: 18px">
      BPMN Redrawer
      <br />
      {{ $t('home.project') }} @ {{ $t('home.university') }}
      <br />
    </div>
    <div class="row justify-center">
      <div
        v-for="email in [
          'alessandro.antinori@studenti.unicam.it',
          'riccardo.coltrinari@studenti.unicam.it',
          'marco.scarpetta@studenti.unicam.it',
        ]"
        :key="email"
      >
        <q-btn
          icon="email"
          flat
          type="a"
          :href="'mailto:' + email"
          :label="email"
          text-color="primary"
        ></q-btn>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from 'vue';
import { QFile, useQuasar } from 'quasar';
import { downloadModel } from 'src/components/utils/bpmn-utils';
import {
  storage,
  fbStorageRef,
  auth,
} from 'src/components/utils/firebase-utils';
import { uploadBytesResumable, UploadTask } from 'firebase/storage';
import { api } from 'src/boot/axios';
import { useBpmnStore } from 'src/store/bpmnStore';
import { blobToDataURL } from 'src/components/utils/image-utils';
import { i18n } from 'src/boot/i18n';

export default defineComponent({
  name: 'HomeComponent',

  setup() {
    const $q = useQuasar();
    const bpmnStore = useBpmnStore();
    const filePicker: Ref<QFile | null> = ref(null);
    const file: Ref<File | null> = ref(null);
    const imgSrc: Ref<string | ArrayBuffer | null | undefined> = ref(null);
    const imageFilename = ref('');
    const conversionDialog: Ref<boolean> = ref(false);
    const conversionResult: Ref<string | null> = ref(null);
    const imageLoaded = ref(false);
    const ocrEnabled = ref(true);
    interface ConversionResult {
      model_id?: string;
      image_id?: string;
      xml: string;
    }

    async function loadImage() {
      // Read file from computer
      await blobToDataURL(file?.value as File)
        .then((result) => {
          imgSrc.value = result;
          imageFilename.value = file.value?.name as string;
          imageLoaded.value = true;
        })
        .catch(() => {
          imgSrc.value = null;
          imageLoaded.value = false;
          $q.notify({
            message: i18n.global.t('home.errorReading'),
            type: 'negative',
          });
        });
    }

    function loadExampleImage(i: number) {
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      imgSrc.value = require(`../assets/example${i}.png`) as string;
      imageLoaded.value = true;
      imageFilename.value = `example${i}.png`;
    }

    function loadingOK() {
      $q.notify({
        message: i18n.global.t('home.loaded'),
        type: 'positive',
      });
    }

    function loadingError() {
      imgSrc.value = null;
      imageLoaded.value = false;
      $q.notify({
        message: i18n.global.t('home.errorLoading'),
        type: 'negative',
      });
    }

    function removeExtension(name: string, extension: string) {
      return name.endsWith('.' + extension)
        ? name.substring(0, name.lastIndexOf('.'))
        : name;
    }

    function getExtension(name: string) {
      return name.split('.').pop() as string;
    }

    async function convertImage() {
      // Use imageName to send the path to backend for conversion
      // Use fullImageName to store the image on Firebase Storage
      const extension = getExtension(imageFilename.value);
      const imageBaseName = removeExtension(imageFilename.value, extension);
      const imageName =
        imageBaseName +
        '-at-' +
        new Date().getTime().toString() +
        '.' +
        extension;
      const fullImageName = bpmnStore.logged
        ? `images/${auth.currentUser?.uid as string}/${imageName}`
        : `anon/${imageName}`;

      const storageRef = fbStorageRef(storage, fullImageName);

      const uploadTask: UploadTask = uploadBytesResumable(
        storageRef,
        await (await fetch(imgSrc.value as string)).blob()
      );

      const uploadDialog = $q.dialog({
        message: i18n.global.t('home.uploading'),
        progress: true,
        persistent: true,
        ok: false,
        cancel: true,
      });
      uploadDialog.onCancel(() => uploadTask.cancel());

      uploadTask.on(
        'state_changed',
        (snapshot) => {
          const progress = Math.floor(
            (snapshot.bytesTransferred / snapshot.totalBytes) * 100
          );
          uploadDialog.update({
            message: i18n.global.t('home.uploadingProgress', {
              progress: progress,
            }),
          });
        },
        (error) => {
          uploadDialog.hide();
          $q.notify({
            message: i18n.global.t('home.errorUploading', {
              error: error.message,
            }),
            type: 'negative',
          });
        },
        () => {
          uploadDialog.hide();
          $q.notify({
            message: i18n.global.t('home.uploadCompleted'),
            type: 'positive',
          });

          const resultDialog = $q.dialog({
            message: i18n.global.t('home.waitBackend'),
            progress: false,
            persistent: true,
            ok: false,
            cancel: true,
          });

          // Call backend API for conversion
          api
            .post('/convert', {
              imagePath: imageName,
              ocr: ocrEnabled.value,
            })
            .then((res) => {
              const resultData = res.data as ConversionResult;
              conversionResult.value = resultData.xml;
              // Update store according to whether the user is logged in or not
              bpmnStore.$patch({
                model: conversionResult.value,
                image: imgSrc.value as string,
                modelPath: resultData.model_id
                  ? '/models/' +
                    (auth.currentUser?.uid as string) +
                    '/' +
                    resultData.model_id
                  : null,
                imagePath: resultData.image_id
                  ? '/images/' +
                    (auth.currentUser?.uid as string) +
                    '/' +
                    resultData.image_id
                  : null,
              });
              resultDialog.hide();
              conversionDialog.value = true;
              $q.notify({
                message: i18n.global.t('home.conversionCompleted'),
                type: 'positive',
              });
            })
            .catch((err) => {
              resultDialog.hide();
              $q.notify({
                message: i18n.global.t('home.errorConversion', { error: err }),
                type: 'negative',
              });
            });
        }
      );
    }

    return {
      tab: ref('from_computer'),
      imgSrc,
      loadImage,
      loadExampleImage,
      filePicker,
      file,
      imageLoaded,
      loadingOK,
      loadingError,
      convertImage,
      conversionDialog,
      downloadModel,
      conversionResult,
      ocrEnabled,
    };
  },
});
</script>
