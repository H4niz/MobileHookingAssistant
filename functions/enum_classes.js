'use strict';
Java.perform(function() {
    Java.enumerateLoadedClasses({
        onMatch: function(className) {
			var text = 	'{ "filename":"Classes.txt" , "data":"'
						+ className + '", "isencode":"True" }';
		 	var obj = JSON.parse(text);
            console.log(className);
    		send(obj);       
/*            if(true)   {
                console.log(className);
                const cls = Java.use(className);
                console.log(cls[function_name].overloads); 
            } */    
        },
        onComplete: function() {}
    });
});