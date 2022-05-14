import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getStorage } from 'firebase/storage';
import { getDatabase } from 'firebase/database';

// Non-admin Firebase config for the following services:
// - Authentication
// - Storage
// - Realtime Database
const firebaseConfig = {
  apiKey: 'AIzaSyDfegB-v-4YkiJjb8iKF4tkezdf3tprBOg',
  authDomain: 'spm-bpmn-redrawer.firebaseapp.com',
  projectId: 'spm-bpmn-redrawer',
  storageBucket: 'spm-bpmn-redrawer.appspot.com',
  databaseURL:
    'https://spm-bpmn-redrawer-default-rtdb.europe-west1.firebasedatabase.app/',
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Authentication service
export const auth = getAuth(app);
// Initialize Storage service
export const storage = getStorage(app);
export { ref as fbStorageRef } from 'firebase/storage';
// Initialize Realtime Database service
export const database = getDatabase(app);
export { ref as fbDatabaseRef } from 'firebase/database';
