console.log("\nEnum Native C/C Functions");
Java.perform(function() {
	console.log("Begin Hooking\n");
	var exports = Module.enumerateExportsSync("libz.so");
	for (var i = 0; i < exports.length; i++){
		if(exports[i].name == 'rsaSignMessage')	{
			console.log(exports[i].name);
		}
		
		var text = 	'{ "filename":"NativeCFuntions.txt" , "data":"'	+ exports[i].name + '", "isencode": "False" }';
	 	var obj = JSON.parse(text);
		send(obj);
	}
});