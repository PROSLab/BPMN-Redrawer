import pyrebase

# firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyDfegB-v-4YkiJjb8iKF4tkezdf3tprBOg",
    "authDomain": "spm-bpmn-redrawer.firebaseapp.com",
    "projectId": "spm-bpmn-redrawer",
    "storageBucket": "spm-bpmn-redrawer.appspot.com",
    "databaseURL": "https://spm-bpmn-redrawer-default-rtdb.europe-west1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
database = firebase.database()
auth = firebase.auth()
