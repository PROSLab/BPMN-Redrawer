<template>
  <q-dialog no-backdrop-dismiss ref="dialogRef" @hide="onDialogHide">
    <q-card bordered class="q-dialog-plugin">
      <q-card-section class="q-gutter-y-sm">
        <q-card-actions>
          <q-btn flat icon="close" color="primary" @click="onCancelClick" />
          <q-space></q-space>
          <q-icon flat name="info" size="24px" color="primary">
            <q-tooltip>
              {{ $t('access.info') }}
            </q-tooltip>
          </q-icon>
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
          <q-input
            outlined
            label="Password"
            type="password"
            lazy-rules
            v-model="v$.form.password.$model"
            :error-message="
              v$.form.password.minLength.$invalid
                ? $t('validation.minLength')
                : ''
            "
            :error="v$.form.password.$invalid && v$.form.password.$dirty"
          ></q-input>
          <q-input
            outlined
            :label="$t('access.confirm')"
            type="password"
            lazy-rules
            v-model="v$.form.confirmPassword.$model"
            :error-message="
              v$.form.confirmPassword.minLength.$invalid
                ? $t('validation.minLength')
                : v$.form.confirmPassword.sameAs.$invalid
                ? $t('validation.match')
                : ''
            "
            :error="
              v$.form.confirmPassword.$invalid && v$.form.confirmPassword.$dirty
            "
          ></q-input>
          <q-card-actions align="left">
            <q-btn
              flat
              dense
              :label="$t('access.recovery')"
              text-color="primary"
              size="12px"
              @click="$emit('onShowPasswordRecoveryForm')"
            ></q-btn>
          </q-card-actions>
          <q-card-actions align="center">
            <q-btn
              color="primary"
              :label="$t('access.signup')"
              :disable="v$.form.$invalid"
              type="submit"
            />
          </q-card-actions>
        </q-form>
        <q-card-actions align="left">
          <q-btn
            flat
            :label="$t('access.haveAccount')"
            text-color="primary"
            @click="$emit('onShowSigninForm')"
          ></q-btn>
        </q-card-actions>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import { useQuasar, QTooltip, useDialogPluginComponent } from 'quasar';
import useVuelidate from '@vuelidate/core';
import { required, email, minLength } from '@vuelidate/validators';
import { useRouter } from 'vue-router';
import {
  createUserWithEmailAndPassword,
  sendEmailVerification,
  signOut,
} from 'firebase/auth';
import { auth } from 'src/components/utils/firebase-utils';
import { FirebaseError } from '@firebase/util';
import { i18n } from 'src/boot/i18n';

export default defineComponent({
  name: 'SignupComponent',

  components: { QTooltip },

  emits: [
    ...useDialogPluginComponent.emits,
    'onShowSigninForm',
    'onShowPasswordRecoveryForm',
  ],

  setup() {
    const { dialogRef, onDialogHide, onDialogCancel } =
      useDialogPluginComponent();
    const $q = useQuasar();
    const router = useRouter();

    const state = reactive({
      form: {
        email: '',
        password: '',
        confirmPassword: '',
      },
    });

    const rules = {
      form: {
        email: { required, email },
        password: { required, minLength: minLength(6) },
        confirmPassword: {
          required,
          minLength: minLength(6),
          sameAs: (confirm: string) => confirm == state.form.password,
        },
      },
    };

    const v$ = useVuelidate(rules, state);

    const onSubmit = async () => {
      try {
        const credentials = await createUserWithEmailAndPassword(
          auth,
          state.form.email,
          state.form.password
        );
        await sendEmailVerification(credentials.user);
        // When successfully creating a new user, it is automatically
        // signed in, so let's sign him out
        await signOut(auth);

        $q.dialog({
          title: i18n.global.t('access.verifyTitle'),
          message: i18n.global.t('access.verifyMessage', {
            email: credentials.user.email,
          }),
        }).onDismiss(() => {
          dialogRef.value?.hide();
          void router.push({ name: 'home' });
        });
      } catch (err) {
        $q.notify({
          message: (err as FirebaseError).message,
          type: 'negative',
        });
      }
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
