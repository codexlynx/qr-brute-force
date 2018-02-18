function get(endpoint, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(this.responseText);
        }
    }
    xhttp.open("GET", endpoint, true);
    xhttp.send();
}

var qrcode = new QRCode("qrcode");
get("/interval", function(interval){
    setInterval(function(){
        get("/word", function(word){
             document.getElementById("sequence").value = word;
             qrcode.makeCode(word);
        });
    }, parseInt(interval));
});
