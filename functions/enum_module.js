Process.enumerateModules({
	onMatch: function(module){
		console.log('Module name: ' + module.name + " - " + "Base Address: " + module.base.toString());
		var text = 	'{ "filename":"Modules.txt" , "data":"'
					+ module.name + '", "isencode":"True" }';
	 	var obj = JSON.parse(text);
		send(obj);
	}, 
	onComplete: function(){}
});