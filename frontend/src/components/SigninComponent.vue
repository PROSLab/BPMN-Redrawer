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
          >
          </q-input>
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
          >
          </q-input>
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
              :label="$t('access.signin')"
              type="submit"
              :disable="v$.form.$invalid"
            />
          </q-card-actions>
        </q-form>
        <q-card-actions align="left">
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
import { useQuasar, QTooltip, useDialogPluginComponent } from 'quasar';
import useVuelidate from '@vuelidate/core';
import { required, email, minLength } from '@vuelidate/validators';
import { useRouter } from 'vue-router';
import { signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { auth } from 'src/components/utils/firebase-utils';
import { FirebaseError } from '@firebase/util';
import { useBpmnStore } from 'src/store/bpmnStore';
import { i18n } from 'src/boot/i18n';

export default defineComponent({
  name: 'SigninComponent',

  components: { QTooltip },

  emits: [
    ...useDialogPluginComponent.emits,
    'onShowSignupForm',
    'onShowPasswordRecoveryForm',
  ],

  setup() {
    const { dialogRef, onDialogHide, onDialogCancel } =
      useDialogPluginComponent();
    const $q = useQuasar();
    const router = useRouter();
    const bpmnStore = useBpmnStore();

    const rules = {
      form: {
        email: { required, email },
        password: { required, minLength: minLength(6) },
      },
    };
    const state = reactive({
      form: {
        email: '',
        password: '',
      },
    });

    const v$ = useVuelidate(rules, state);

    const onSubmit = async () => {
      try {
        const credentials = await signInWithEmailAndPassword(
          auth,
          state.form.email,
          state.form.password
        );

        // Let the user log in only if its email is verified
        if (!credentials.user.emailVerified) {
          await signOut(auth);
          $q.notify({
            message: i18n.global.t('access.notVerified'),
            type: 'negative',
          });
        } else {
          bpmnStore.logged = true;
          dialogRef.value?.hide();
          await router.push({ name: 'home' });
        }
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
