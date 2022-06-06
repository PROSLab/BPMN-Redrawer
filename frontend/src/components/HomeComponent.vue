<template>
  <div class="q-pa-md">
    <div style="margin: auto; text-align: center">
      <div style="font-size: 32px">{{ $t('home.welcome') }}</div>
      <div style="font-size: 18px">
        {{ $t('home.description') }}
      </div>
    </div>

    <div style="text-align: center">
      <q-checkbox
        class="q-pr-md"
        v-model="thumbnailsEnabled"
        :label="$t('home.thumbnails')"
      ></q-checkbox>
      <q-checkbox
        class="q-pr-md"
        v-model="batchEnabled"
        :label="$t('home.batch')"
      ></q-checkbox>
    </div>

    <div class="row justify-center q-pa-md" style="text-align: center">
      <div>
        <q-uploader
          ref="uploader"
          style="
            width: 600px;
            max-width: 600px;
            height: 400px;
            max-height: 400px;
          "
          :url="api.defaults.baseURL + '/convert'"
          :no-thumbnails="!thumbnailsEnabled"
          :batch="batchEnabled"
          bordered
          multiple
          accept=".png, .jpeg, .jpg, .bmp"
          :form-fields="[
            { name: 'elements', value: elementsEnabled },
            { name: 'flows', value: flowsEnabled },
            { name: 'ocr', value: ocrEnabled },
          ]"
          @added="(files) => onAdded(files)"
          @removed="(files) => onRemoved(files)"
          @uploaded="(info) => onUploaded(info)"
        >
          <template v-slot:header="scope">
            <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
              <q-btn
                v-if="scope.queuedFiles.length > 0"
                icon="clear_all"
                @click="scope.removeQueuedFiles"
                round
                dense
                flat
              >
                <q-tooltip>{{ $t('uploader.clearAll') }}</q-tooltip>
              </q-btn>
              <q-btn
                v-if="scope.uploadedFiles.length > 0"
                icon="done_all"
                @click="scope.removeUploadedFiles"
                round
                dense
                flat
              >
                <q-tooltip>{{ $t('uploader.doneAll') }}</q-tooltip>
              </q-btn>
              <q-btn
                v-if="scope.uploadedFiles.length > 0"
                icon="download"
                @click="onDownloadModels()"
                round
                dense
                flat
              >
                <q-tooltip>{{ $t('uploader.download') }}</q-tooltip>
              </q-btn>
              <q-spinner v-if="scope.isUploading" class="q-uploader__spinner" />
              <div class="col">
                <div class="q-uploader__title">{{ $t('uploader.title') }}</div>
                <div class="q-uploader__subtitle">
                  {{ scope.uploadSizeLabel }} / {{ scope.uploadProgressLabel }}
                </div>
              </div>
              <q-btn
                v-if="scope.canAddFiles"
                type="a"
                icon="add_box"
                round
                dense
                flat
              >
                <q-uploader-add-trigger />
                <q-tooltip>{{ $t('uploader.pickFiles') }}</q-tooltip>
              </q-btn>
              <q-btn
                v-if="scope.canUpload"
                icon="cloud_upload"
                @click="scope.upload"
                round
                dense
                flat
              >
                <q-tooltip>{{ $t('uploader.uploadFiles') }}</q-tooltip>
              </q-btn>

              <q-btn
                v-if="scope.isUploading"
                icon="clear"
                @click="scope.abort"
                round
                dense
                flat
              >
                <q-tooltip>{{ $t('uploader.abortUpload') }}</q-tooltip>
              </q-btn>
            </div>
          </template>
          <template v-slot:list="scope">
            <q-list separator>
              <q-item v-for="file in scope.files" :key="file.__key">
                <q-item-section>
                  <div
                    :class="
                      'q-uploader__file relative-position' +
                      (thumbnailsEnabled && file.__img !== void 0
                        ? ' q-uploader__file--img'
                        : '') +
                      (file.__status === 'failed'
                        ? ' q-uploader__file--failed'
                        : file.__status === 'uploaded'
                        ? ' q-uploader__file--uploaded'
                        : '')
                    "
                    :style="
                      thumbnailsEnabled && file.__img !== void 0
                        ? 'background-image: url(' + file.__img.src + ')'
                        : null
                    "
                  >
                    <div
                      class="q-uploader__file-header row flex-center no-wrap"
                    >
                      <q-icon
                        v-if="file.__status === 'failed'"
                        class="q-uploader__file-status"
                        name="warning"
                        color="negative"
                      >
                      </q-icon>
                      <div class="q-uploader__file-header-content col">
                        <div class="q-uploader__title">{{ file.name }}</div>
                        <div
                          class="q-uploader__subtitle row items-center no-wrap"
                        >
                          {{ file.__sizeLabel + ' / ' + file.__progressLabel }}
                        </div>
                      </div>

                      <q-circular-progress
                        v-if="file.__status === 'uploading'"
                        :value="file.__progress"
                        :min="0"
                        :max="1"
                        :indeterminate="file.__progress === 0"
                      >
                      </q-circular-progress>
                      <q-btn
                        v-else
                        round
                        dense
                        flat
                        :icon="file.__status === 'uploaded' ? 'done' : 'clear'"
                        @click="scope.removeFile(file)"
                      >
                      </q-btn>
                    </div>
                  </div>
                </q-item-section>
                <q-item-section side class="q-gutter-sm">
                  <q-btn
                    :disabled="results.get(file.name) == ''"
                    icon="edit"
                    color="primary"
                    @click="onEdit(file)"
                  ></q-btn>
                  <q-btn
                    :disabled="results.get(file.name) == ''"
                    icon="download"
                    color="primary"
                    @click="onDownload(file)"
                  ></q-btn>
                </q-item-section>
              </q-item>
            </q-list>
          </template>
        </q-uploader>
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
import { exportFile, QUploader, useQuasar } from 'quasar';
import { api } from 'src/boot/axios';
import JSZip from 'jszip';
import { useRouter } from 'vue-router';
import { i18n } from 'src/boot/i18n';
import { blobToDataURL } from './utils/image-utils';

export default defineComponent({
  name: 'HomeComponent',

  setup() {
    const $q = useQuasar();
    const router = useRouter();
    const uploader: Ref<QUploader | null> = ref(null);
    const thumbnailsEnabled = ref(true);
    const batchEnabled = ref(true);
    const elementsEnabled = ref(true);
    const flowsEnabled = ref(true);
    const ocrEnabled = ref(true);
    interface ConversionResult {
      image: string;
      model: string;
    }
    const results: Ref<Map<string, string>> = ref(new Map([]));

    async function loadExampleImage(i: number) {
      uploader.value?.reset();
      const imageName = `example${i}.png`;
      const blob = await (
        await fetch(
          // eslint-disable-next-line @typescript-eslint/no-var-requires
          require('../assets/' + imageName) as string
        )
      ).blob();
      uploader.value?.addFiles([
        new File([blob], imageName, { type: blob.type }),
      ]);
    }

    function onAdded(files: File[]) {
      files.forEach((f) => {
        results.value.set(f.name, '');
      });
    }

    function onRemoved(files: File[]) {
      files.forEach((f) => {
        results.value.delete(f.name);
      });
    }

    async function onEdit(file: File) {
      const image = await blobToDataURL(new Blob([file]));
      const model = results.value.get(file.name);
      $q.dialog({
        message: i18n.global.t('editor.exit'),
        cancel: true,
      }).onOk(() => {
        void router.push({
          name: 'editor',
          params: { image: image, model: model },
        });
      });
    }

    function onDownload(file: File) {
      exportFile(
        file.name.substring(0, file.name.lastIndexOf('.')) + '.bpmn',
        results.value.get(file.name) as string,
        {
          mimeType: 'text/xml',
          encoding: 'utf-8',
        }
      );
    }

    function onUploaded(info: { _: File[]; xhr: XMLHttpRequest }) {
      (JSON.parse(info.xhr.response as string) as ConversionResult[]).forEach(
        (cr) => {
          results.value.set(cr.image, cr.model);
        }
      );
    }

    async function onDownloadModels() {
      const zip = new JSZip();
      [...results.value.entries()].forEach((e) => {
        if (e[1] != '') {
          zip.file(e[0] + '.bpmn', e[1]);
        }
      });
      const res = await zip.generateAsync({ type: 'blob' });
      exportFile('bpmn_models.zip', res);
    }

    return {
      api,
      uploader,
      results,
      onAdded,
      onRemoved,
      onEdit,
      onDownload,
      onUploaded,
      onDownloadModels,
      loadExampleImage,
      thumbnailsEnabled,
      batchEnabled,
      elementsEnabled,
      flowsEnabled,
      ocrEnabled,
    };
  },
});
</script>
