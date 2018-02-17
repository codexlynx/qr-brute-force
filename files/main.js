function get(enpoint, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(this.responseText);
        }
    }
    xhttp.open("GET", enpoint, true);
    xhttp.send();
}

var qrcode = new QRCode("qrcode");
setInterval(function(){
    get('/word', function(word){
         document.getElementById("sequence").innerHTML = word;
         qrcode.makeCode(word);
    });
}, 1000);