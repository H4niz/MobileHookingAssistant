'use strict';
console.log(" ------ [JS] ------")
Java.perform(function() {
        console.log("[ JS ] - Sending data to python..")	
	    send({from: '/http', payload: '{ "name":"John", "age":30, "car":null, "class":null }'});

	    var op = recv('x', function(x) { // callback function
	        console.log("[ JS ] - Data receive after modified: " + x.payload);
	    });
});