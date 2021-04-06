'use strict';
setImmediate(function() {
  send("hooking started");
  Java.perform(function() {
  var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
  var SSLContext = Java.use('javax.net.ssl.SSLContext');
  var class_root = Java.use("com.scottyab.rootbeer.b");
  var br = Java.use("br.com.classapp.RNSensitiveInfo.RNSensitiveInfoModule");
  class_root.hU.implementation = function(){
    var rs = this.hU();
    console.log("[*] hU: "+rs);
    return false;
  }
  br.decrypt.overload('java.lang.String').implementation = function(x1){
    var rs = this.decrypt(x1);
    console.log("[*] decrypt: "+x1+" --> "+rs);
    return rs;
  }
  var TrustManager = Java.registerClass({
      name: 'com.sensepost.test.TrustManager',
      implements: [X509TrustManager],
      methods: {
          checkClientTrusted: function (chain, authType) {
          },
          checkServerTrusted: function (chain, authType) {
          },
          getAcceptedIssuers: function () {
              return [];
          }
      }
  });
  // Prepare the TrustManagers array to pass to SSLContext.init()
  var TrustManagers = [TrustManager.$new()];
  send("Custom, Empty TrustManager ready");
  // Override the init method, specifying our new TrustManager
  SSLContext.init.implementation = function (keyManager, trustManager, secureRandom) {
      send("Overriding SSLContext.init() with the custom TrustManager");
      this.init.call(this, keyManager, TrustManagers, secureRandom);
  };
  });
});