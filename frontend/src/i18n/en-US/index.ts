// This is just an example,
// so you can safely delete all default props below

export default {
  home: {
    welcome: 'Welcome to BPMN Redrawer',
    description:
      'A simple application to convert a PNG image into the corresponding BPMN model',
    project: 'SPM Project',
    university: 'University of Camerino',
    load: 'Load image',
    convert: 'Convert',
    open: 'Open in Editor',
    converted: 'The image has been converted.',
    errorReading: 'Error while reading the image',
    loaded: 'Image loaded',
    errorLoading: 'Error while loading the image',
    uploading: 'Uploading... 0%',
    uploadingProgress: 'Uploading... {progress}%',
    errorUploading: 'Error while uploading: {error}',
    uploadCompleted: 'Upload completed',
    waitBackend: 'Waiting for a response from backend...',
    conversionCompleted: 'Conversion completed',
    errorConversion: 'Error during the conversion: {error}',
    examples: 'Examples',
    examplesInstruction: 'Click a model below to load the corresponding image',
  },
  main: {
    dark: 'Dark mode',
    sign: 'Sign up / Sign in',
  },
  access: {
    signin: 'Sign In',
    signup: 'Sign Up',
    recover: 'Recover Password',
    recovery: 'Forgot your password?',
    confirm: 'Confirm Password',
    noAccount: "Don't have an account?",
    haveAccount: 'Already have an account?',
    info: 'By signing up, you can access your conversion history, edit an already converted model and more!',
    notVerified: 'Email not verified',
    verifyTitle: 'Verify your account',
    verifyMessage:
      'A verification email has been sent to {email}. Please check your mailbox to verify your account before you sign in.',
  },
  password: {
    title: 'Password Recovery',
    message:
      'A password recovery link has been sent to {email}. When you receive it, click the link to open a window where you can enter a new password.',
  },
  editor: {
    drop: 'Drop',
    open: 'Open',
    create: 'Create',
    intro: 'a BPMN diagram to get started.',
    exit: 'Are you sure you want to quit? All unsaved progress will be lost.',
    errorSaveBPMN: 'Error while saving the model as BPMN',
    errorSavePNG: 'Error while saving the model as SVG',
    errorUpload: 'Error while uploading a BPMN model',
    savedChanges: 'Model changes saved successfully',
    errorSaveChanges: 'Error while saving model changes',
  },
  profile: {
    history: 'History',
    delete: 'Delete Account',
    title: 'Delete your account',
    message: 'Are you sure you want to delete your account?',
    deleted: 'Your account has been deleted',
  },
  history: {
    loading: 'Loading history...',
    title: 'Conversion History',
    conversions: 'Conversions',
    date: 'Date',
    model: 'Model',
    image: 'Image',
    open: 'Open in Editor',
    noConversions: 'No conversions done so far...',
    errorHistory: 'Error while getting the conversion history',
    errorModelImage: 'Error while retrieving the model/image',
  },
  validation: {
    email: 'Please provide a valid email address',
    minLength: 'Password must be at least 6 characters long',
    match: 'Password and Confirm Password must match',
  },
  router: {
    noAuth: "Sorry, you're not allowed to access this page. Please sign in.",
  },
};
