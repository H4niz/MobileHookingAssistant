'use strict';

function enumMethods(targetClass)
{
	var hook = Java.use('crypto.Crypto');
	var ownMethods = hook.class.getDeclaredMethods();
	hook.$dispose;

	return ownMethods;
};

Java.Perform( function() {
	enumMethods("a");
});