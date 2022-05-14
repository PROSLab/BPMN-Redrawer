<template>
  <q-scroll-area
    style="
      height: calc(100% - 130px);
      margin-top: 130px;
      border-right: 1px solid #ddd;
    "
  >
    <q-list padding>
      <q-item clickable v-ripple :to="{ name: 'history' }">
        <q-item-section avatar>
          <q-icon name="history" />
        </q-item-section>

        <q-item-section>{{ $t('profile.history') }}</q-item-section>
      </q-item>
      <q-item clickable v-ripple @click="deleteAccount()">
        <q-item-section avatar>
          <q-icon name="delete" />
        </q-item-section>

        <q-item-section>{{ $t('profile.delete') }}</q-item-section>
      </q-item>
    </q-list>
  </q-scroll-area>

  <q-img
    class="absolute-top"
    src="https://cdn.quasar.dev/img/material.png"
    style="height: 130px"
  >
    <div class="absolute-bottom bg-transparent">
      <q-avatar size="56px" class="q-mb-sm">
        <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
      </q-avatar>
      <div>{{ auth.currentUser?.email }}</div>
    </div>
  </q-img>
</template>

<script lang="ts">
import { deleteUser, User } from '@firebase/auth';
import { FirebaseError } from '@firebase/util';
import { useQuasar } from 'quasar';
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import { auth } from 'src/components/utils/firebase-utils';
import { i18n } from 'src/boot/i18n';

export default defineComponent({
  name: 'ProfileComponent',

  setup() {
    const $q = useQuasar();
    const router = useRouter();

    const deleteAccount = () => {
      $q.dialog({
        title: i18n.global.t('profile.title'),
        message: i18n.global.t('profile.message'),
        cancel: true,
        noBackdropDismiss: true,
      }).onOk(() => {
        deleteUser(auth.currentUser as User)
          .then(() => {
            router.go(0);
            $q.notify({
              message: i18n.global.t('profile.deleted'),
              type: 'positive',
            });
          })
          .catch((err: FirebaseError) => {
            $q.notify({
              message: err.message,
              type: 'negative',
            });
          });
      });
    };

    return {
      deleteAccount,
      auth,
    };
  },
});
</script>
