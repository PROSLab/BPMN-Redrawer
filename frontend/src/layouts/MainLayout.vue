<template>
  <q-layout view="lHh LpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          v-if="bpmnStore.logged"
          dense
          flat
          round
          icon="menu"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title> BPMN Redrawer </q-toolbar-title>
        <q-space></q-space>
        <locale-changer></locale-changer>
        <dark-mode-changer></dark-mode-changer>
        <q-btn
          v-if="bpmnStore.logged"
          outline
          icon="logout"
          label="Logout"
          @click="logout()"
        ></q-btn>
        <q-btn
          v-else
          outline
          icon="lock"
          :label="$t('main.sign')"
          @click="signin = true"
        ></q-btn>
        <signin-component
          v-model="signin"
          @onShowSignupForm="
            signin = false;
            signup = true;
          "
          @onShowPasswordRecoveryForm="
            signin = false;
            recovery = true;
          "
        ></signin-component>
        <signup-component
          v-model="signup"
          @onShowSigninForm="
            signup = false;
            signin = true;
          "
          @onShowPasswordRecoveryForm="
            signup = false;
            recovery = true;
          "
        ></signup-component>
        <password-recovery-component
          v-model="recovery"
          @onShowSigninForm="
            recovery = false;
            signin = true;
          "
          @onShowSignupForm="
            recovery = false;
            signup = true;
          "
        ></password-recovery-component>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-if="bpmnStore.logged"
      v-model="leftDrawerOpen"
      side="left"
      behavior="desktop"
      bordered
    >
      <profile-component></profile-component>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-tabs
        align="justify"
        v-model="tab"
        inline-label
        indicator-color="secondary"
        active-bg-color="primary"
      >
        <q-route-tab
          name="home"
          default="true"
          icon="home"
          label="Home"
          :to="{ name: 'home' }"
        />
        <q-route-tab
          name="edit"
          icon="edit"
          label="Editor"
          :to="{ name: 'editor' }"
        />
      </q-tabs>
    </q-footer>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import ProfileComponent from 'src/components/ProfileComponent.vue';
import SigninComponent from 'src/components/SigninComponent.vue';
import SignupComponent from 'src/components/SignupComponent.vue';
import PasswordRecoveryComponent from 'src/components/PasswordRecoveryComponent.vue';
import { useRouter } from 'vue-router';
import { signOut } from '@firebase/auth';
import { auth } from 'src/components/utils/firebase-utils';
import { FirebaseError } from '@firebase/util';
import { useBpmnStore } from 'src/store/bpmnStore';
import LocaleChanger from 'src/components/LocaleChanger.vue';
import DarkModeChanger from 'src/components/DarkModeChanger.vue';

export default defineComponent({
  name: 'MainLayout',

  components: {
    ProfileComponent,
    SigninComponent,
    SignupComponent,
    PasswordRecoveryComponent,
    LocaleChanger,
    DarkModeChanger,
  },

  setup() {
    const $q = useQuasar();
    const router = useRouter();
    const bpmnStore = useBpmnStore();
    const signin = ref(false);
    const signup = ref(false);
    const recovery = ref(false);
    const tab = ref('home');
    const leftDrawerOpen = ref(false);
    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value;
    };
    const logout = async () => {
      await signOut(auth)
        .then(() => {
          // Reload the current page after logout
          router.go(0);
        })
        .catch((err: FirebaseError) => {
          $q.notify({ message: err.message, type: 'negative' });
        });
    };

    return {
      tab,
      leftDrawerOpen,
      toggleLeftDrawer,
      bpmnStore,
      signin,
      signup,
      recovery,
      logout,
    };
  },
});
</script>
