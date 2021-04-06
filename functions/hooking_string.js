Java.perform(function () {
    // Function to hook is defined here
    const StringBuilder = Java.use('java.lang.StringBuilder');
    const StringBuffer = Java.use('java.lang.StringBuffer');

    StringBuilder.toString.implementation = function () {
            var result = this.toString();
      var text =  '{ "filename":"StringBuilder.txt" , "data":"'
            + result + '", "isencode":"False" }';
      var obj = JSON.parse(text);
      send(obj);

            console.log('StringBuilder \t=> ' + result);
            return result;
    };

    StringBuffer.toString.implementation = function () {
            var result = this.toString();
      var text =  '{ "filename":"StringBuffer.txt" , "data":"'
            + result + '", "isencode":"False" }';
      var obj = JSON.parse(text);
      send(obj);

            console.log('StringBuffer \t=> ' + result);
            return result;
    };
});