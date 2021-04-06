'use strict';
console.log("\nRedirecting...");
Java.perform(function(){
	
	var li = Java.use("o.li$2");
	var ln = Java.use("o.ln");
	var lii = Java.use("o.li");
	var request = Java.use("okhttp3.RequestBody");
	
	ln.ˎ.overload('java.lang.String').implementation = function(data){
		console.log("-------------------- Data Request---------------------");
/*		console.log(data)*/
		send({from: '/http', payload: data})
		var modify_data = "None";
		var op = recv('x', function(x) {
/*			console.log("[]" + JSON.stringify(x.payload));*/
			modify_data = JSON.stringify(x.payload);
		});
		op.wait();
		console.log("------------------- Modified Data --------------------")
		console.log(modify_data);
		console.log("-------------------------------------------------------");
		var rs  = this.ˎ(modify_data);

		return rs;
	}
	ln.ˏ.overload('java.lang.String').implementation = function(data){
		console.log("-------------------- Data Response ---------------------");
/*		console.log(data)*/
		var rs = this.ˏ(data);
		console.log("-------------------- Data Response Decrypted ---------------------");
		console.log(rs);
		console.log("-------------------------------------------------------");
		console.log("\n")
		return rs;
	}
	/*
	li.onResponse.implementation = function(call, response){
		logrequest(response.request());
		logreponse(response);
		return this.onResponse(call, response);
	}
	ln.ˎ.overload('java.lang.String').implementation = function(data){
		console.log(data);
		return this.ˎ(data);
	}
	li.onResponse.implementation = function(call, response){
		console.log("============Mode Post==========");
		logrequest(response.request());
		logreponse(response);
		return this.onResponse(call, response);
	}
	ln.ˏ.overload('java.lang.String').implementation = function(data){
		console.log("mode");
		var rs = this.ˏ(data);
		console.log(rs);
		return rs;
	}
	ln.ˏ.overload("[B").implementation = function(data){
		console.log("OKIE");
		console.log("===========")
		var rs =this.ˏ(data);
		console.log(rs);
		console.log(stringFromArray(rs));
		console.log("=========")
		return rs;
	}
		
	var h_request = Java.use("okhttp3.Request");
	h_request.body.implementation = function(){
		var method = this._method.value;
        var headers = this._headers.value.toString();
        var url = this._url.value;
        var body = this._bo	y.value;
        var retval = this.body();
        console.log(method + " " + url);
        if (method == "POST") {
            console.log(body)
        }
        return retval
	}*/
	
});
function logrequest(request){
	console.log('--------------------Request---------------------')
	console.log(request.method() + ' ' + request.url().toString());
	console.log('---Headers---')
    console.log(request.headers());
}
function logreponse(response){
	console.log('\n--------------------Response--------------------')
	console.log('---HTTP Status Code: ' + response.code() + '---')
    console.log('---Protocol: ' + response.protocol().name() + '---')
    console.log('---Headers---')
    console.log(response.headers());
}
function stringFromUTF8Array(data)
  {
    const extraByteMap = [ 1, 1, 1, 1, 2, 2, 3, 0 ];
    var count = data.length;
    var str = "";
    
    for (var index = 0;index < count;)
    {
      var ch = data[index++];
      if (ch & 0x80)
      {
        var extra = extraByteMap[(ch >> 3) & 0x07];
        if (!(ch & 0x40) || !extra || ((index + extra) > count))
          return null;
        
        ch = ch & (0x3F >> extra);
        for (;extra > 0;extra -= 1)
        {
          var chx = data[index++];
          if ((chx & 0xC0) != 0x80)
            return null;
          
          ch = (ch << 6) | (chx & 0x3F);
        }
      }
      
      str += String.fromCharCode(ch);
    }
    
    return str;
  }

  function stringFromArray(data)
  {
    var count = data.length;
    var str = "";
    
    for(var index = 0; index < count; index += 1)
      str += String.fromCharCode(data[index]);
    
    return str;
  }
function logHeaders(headers){
           for(var i = 0; i < headers.size(); i++){
               var headerName = headers.name(i);
               var headerValue = headers.value(i);
               console.log(headerName + ': ' + headerValue);
           }
       }
