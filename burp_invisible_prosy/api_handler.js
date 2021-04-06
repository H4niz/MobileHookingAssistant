'use strict';
console.log(" ------ API Handler ------")
Java.perform(function() {
	    
	    send({from: '/http', payload: '{ "name":"John", "age":30, "car":null, "class":null }'});
        
	    var op = recv('x', function(x) { // callback function
	        console.log("[ JS ] - Data receive after modified: " + x.payload);
	    });
});