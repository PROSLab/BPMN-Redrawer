<template>
  <q-dialog no-backdrop-dismiss ref="dialogRef" @hide="onDialogHide">
    <q-card bordered class="q-dialog-plugin">
      <q-card-section class="q-gutter-y-sm">
        <q-card-actions align="left">
          <q-btn flat icon="close" color="primary" @click="onCancelClick" />
        </q-card-actions>
        <div class="row justify-center">
          <div style="font-size: 32px">BPMN Redrawer</div>
        </div>
        <q-form @submit.prevent="onSubmit">
          <q-input
            outlined
            label="Email"
            type="email"
            lazy-rules
            v-model="v$.form.email.$model"
            :error-message="
              v$.form.email.email.$invalid ? $t('validation.email') : ''
            "
            :error="v$.form.email.$invalid && v$.form.email.$dirty"
          ></q-input>
          <q-card-actions align="center">
            <q-btn
              color="primary"
              :label="$t('access.recover')"
              :disable="v$.form.$invalid"
              type="submit"
            />
          </q-card-actions>
        </q-form>
        <q-card-actions vertical align="left">
          <q-btn
            flat
            :label="$t('access.haveAccount')"
            text-color="primary"
            @click="$emit('onShowSigninForm')"
          ></q-btn>
          <q-separator></q-separator>
          <q-btn
            flat
            :label="$t('access.noAccount')"
            text-color="primary"
            @click="$emit('onShowSignupForm')"
          ></q-btn>
        </q-card-actions>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import { useQuasar, useDialogPluginComponent } from 'quasar';
import useVuelidate from '@vuelidate/core';
import { required, email } from '@vuelidate/validators';
import { useRouter } from 'vue-router';
import { sendPasswordResetEmail } from '@firebase/auth';
import { auth } from 'src/components/utils/firebase-utils';
import { FirebaseError } from '@firebase/util';
import { i18n } from 'src/boot/i18n';

export default defineComponent({
  name: 'PasswordRecoveryComponent',

  emits: [
    ...useDialogPluginComponent.emits,
    'onShowSigninForm',
    'onShowSignupForm',
  ],

  setup() {
    const { dialogRef, onDialogHide, onDialogCancel } =
      useDialogPluginComponent();
    const $q = useQuasar();
    const router = useRouter();

    const state = reactive({
      form: {
        email: '',
      },
    });

    const rules = {
      form: {
        email: { required, email },
      },
    };

    const v$ = useVuelidate(rules, state);

    const onSubmit = async () => {
      await sendPasswordResetEmail(auth, state.form.email)
        .then(() => {
          $q.dialog({
            title: i18n.global.t('password.title'),
            message: i18n.global.t('password.message', {
              email: state.form.email,
            }),
          }).onDismiss(() => {
            router.go(0);
          });
        })
        .catch((err: FirebaseError) => {
          $q.notify({
            message: err.message,
            type: 'negative',
          });
        });
    };

    return {
      dialogRef,
      onDialogHide,
      onCancelClick: onDialogCancel,
      v$,
      onSubmit,
    };
  },
});
</script>
