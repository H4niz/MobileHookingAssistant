function getContext() {
  return Java.use('android.app.ActivityThread').currentApplication().getApplicationContext().getContentResolver();
}                                         
function logAndroidId() {
  console.log('Android ID: ', Java.use('android.provider.Settings$Secure').getString(getContext(), 'android_id'));
}

Java.perform(logAndroidId);