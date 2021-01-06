var decimal = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;
var password = document.getElementById('validation2');

function CheckPassword(elem) {
    if(elem.value.length > 0){
        if(elem.value.match(decimal)){
            document.getElementById('alert').innerText = "";
        }else{
            document.getElementById('alert').innerText = "Debe contener letra mayuscula, minuscula, un numero y un caracter";
        }
    }else{
        document.getElementById('alert').innerText = "Ingrese contraseña";
    }
}