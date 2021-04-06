'use strict';
Java.perform(function(){
	console.log("-------------Kiosk");
	var companion = Java.use("wee.vietinbank.kiosk.data.model.Device");
	companion.getPrivateKey.implementation = function(){
		var rs = this.getPrivateKey();
		console.log("Privatekey: "+rs);
		return rs;
	}
});