/*Java.perform(function(){
  console.log("hacking");
  var IL = Java.use("o.lL");
  var equal = Java.use("okio.ByteString");
  IL.intercept.implementation = function(chain){
    console.log("Bypass SSL Pinning");
    equal.equals.implementation = function(ob){
      return true;
    }
    return this.intercept(chain);
  }
});*/

