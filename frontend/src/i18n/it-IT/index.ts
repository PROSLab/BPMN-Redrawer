// This is just an example,
// so you can safely delete all default props below

export default {
  home: {
    welcome: 'Benvenuti a BPMN Redrawer',
    description:
      "Una semplice applicazione per convertire un'immagine PNG nel relativo modello BPMN",
    project: 'Progetto SPM',
    university: 'Università di Camerino',
    load: 'Carica immagine',
    convert: 'Converti',
    open: "Apri nell' Editor",
    converted: "L'immagine è stata convertita.",
    errorReading: "Errore durante la lettura dell'immagine",
    loaded: 'Immagine caricata',
    errorLoading: "Errore durante il caricamento dell'immagine",
    uploading: 'Caricando... 0%',
    uploadingProgress: 'Caricando... {progress}%',
    errorUploading: 'Errore durante il caricamento: {error}',
    uploadCompleted: 'Caricamento completato',
    waitBackend: 'Attendendo una risposta dal backend...',
    conversionCompleted: 'Conversione completata',
    errorConversion: 'Errore durante la conversione: {error}',
  },
  main: {
    dark: 'Modalità scura',
    sign: 'Registrati / Accedi',
  },
  access: {
    signin: 'Accedi',
    signup: 'Registrati',
    recover: 'Recupera Password',
    recovery: 'Hai dimenticato la password?',
    confirm: 'Conferma Password',
    noAccount: 'Non hai un account?',
    haveAccount: 'Hai già un account?',
    info: 'Registrandoti, potrai accedere alla cronologia delle tue conversioni, modificare un modello già convertito e molto altro!',
    notVerified: 'Email non verificata',
    verifyTitle: 'Verifica il tuo account',
    verifyMessage:
      "Un'email di verifica è stata inviata a {email}. Per favora controlla la tua casella di posta per verificare il tuo account prima di accedere.",
  },
  password: {
    title: 'Recupero Password',
    message:
      'Un link per il recupero della password è stato inviato a {email}. Una volta ricevuto, clicca il link per aprire una finestra dove puoi inserire una nuova password.',
  },
  editor: {
    drop: 'Rilascia',
    open: 'Apri',
    create: 'Crea',
    intro: 'un diagramma BPMN per iniziare.',
    exit: 'Sei sicuro di voler uscire? Tutti i progressi non salvati andranno persi.',
    errorSaveBPMN: 'Errore durante il salvataggio del modello come BPMN',
    errorSavePNG: 'Errore durante il salvataggio del modello come SVG',
    errorUpload: 'Errore durante il caricamento del modello BPMN',
    savedChanges: 'Modifiche al modello salvate con successo',
    errorSaveChanges:
      'Errore durante il salvataggio delle modifiche al modello',
  },
  profile: {
    history: 'Cronologia',
    delete: 'Cancella Account',
    title: 'Cancella il tuo account',
    message: 'Sei sicuro di voler cancellare il tuo account?',
    deleted: 'Il tuo account è stato cancellato',
  },
  history: {
    loading: 'Caricando la cronologia...',
    title: 'Cronologia Conversioni',
    conversions: 'Conversioni',
    date: 'Data',
    model: 'Modello',
    image: 'Immagine',
    open: "Apri nell' Editor",
    noConversions: 'Ancora nessuna conversione effettuata...',
    errorHistory:
      'Errore durante il recupero della cronologia delle conversioni',
    errorModelImage: 'Errore durante il recupero del modello/immagine',
  },
  validation: {
    email: 'Fornisci un indirizzo email valido',
    minLength: 'La Password deve essere lunga almeno 6 caratteri',
    match: 'Password e Conferma Password devono corrispondere',
  },
  router: {
    noAuth:
      "Non hai il permesso di visualizzare questa pagina. Per favore effettua l'accesso.",
  },
};
