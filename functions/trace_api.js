'use strict';
console.log("Redirecting...");

Java.perform( function() {
	console.log("[+] Modify Requests ... ");

	var _crypto = Java.use("crypto.Crypto");

/*	console.log('[-] Using class');*/

	_crypto.rsaSignMessage.implementation = function(data,skey)	{
		console.log('[-] Insite implementation');
		console.log('[+] Data.keys(): ' + Object.keys(data));
		console.log('[+] Data raw: ' + JSON.stringify(data));
		console.log('[+] Data: ' + String.fromCharCode.apply(null, data));
		var json_data = String.fromCharCode.apply(null, data);
		console.log('[+] Skey: ' + JSON.stringify(skey));
		send({from: '/http', payload: (json_data)});
		var modify_data = "None";
		var op = recv('x', function(x) {
			modify_data =  JSON.parse(x.payload);
			console.log('[+] Modify: ' +  typeof(modify_data));
		});
		console.log("[-->] Data sent");
		console.log('========== Typeof ===========');
		console.log('Typeof skey: ' + typeof skey);
		console.log('========== Typeof ===========');

		op.wait();
		var ret = this.rsaSignMessage(modify_data, skey);
		console.log('******************* RET ******************');
		console.log(ret);
		console.log('******************* RET ******************');
		
		

		return ret;
	};
});
