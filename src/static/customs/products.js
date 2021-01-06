$(document).ready(function(){
    $("#completa_compra").click(function(){
        let nFila = $("#tablaProductos tr").length;

        if(nFila < 2){

        }else{
            $("#form_compra").submit();
        }
    });

});

function buscarProducto(e, tagCode, code){
    var enterKey = 13;

    if(code != ''){
        if(e.which == enterKey){
            $.ajax({
                url:'/buscarPorCodigo/'+code,
                dataType: 'json',
                success: function(resultado){
                    if(resultado==0){
                        $(tagCode).val('');
                        document.getElementById('resultado_error').innerText = "";
                    }else{
                        
                        if(resultado.existe){
                            $("#id_producto").val(resultado.datos.idProductos);
                            $("#name").val(resultado.datos.nombre);
                            $("#cantidad").val(1);
                            $("#price").val(resultado.datos.precio_compra);
                            $("#product_subtotal").val(resultado.datos.precio_compra);
                            $("#cantidad").focus();
                            document.getElementById('resultado_error').innerText = "";
                        }else{
                            $("#id_producto").val('');
                            $("#name").val('');
                            $("#cantidad").val('');
                            $("#price").val('');
                            $("#product_subtotal").val('');
                            $("#resultado_error").html(resultado.error);
                            document.getElementById('resultado_error').innerText = "El producto no existe";
                        }
                    }
                }
            });
        }
    }
}

function calculate(){
    var cantidad = document.getElementById('cantidad').value;
    var precio = document.getElementById('price').value;
    var subtotal = document.getElementById('product_subtotal');
    var resultado = cantidad * precio;
    subtotal.value = resultado;
}

// cargar valores de las variables con los ids de inputs
function agregarProducto(id_producto, cantidad, id_compra){
    
    if(id_producto != null && id_producto != 0 && cantidad > 0){
        $.ajax({
            url:'/temporalCompra/'+ id_producto +'/'+cantidad+'/'+id_compra,
            success: function(resultado){
                if(resultado==0){

                }else{

                    var resultado = resultado;
                    if(resultado.error == ""){
                        // var tax = 0.15
                        // var total_tax = (resultado.total * tax).toFixed(2)
                        // var compra_total = (total_tax + resultado.total).toFixed(2)
                        $("#tablaProductos tbody").empty();
                        $("#tablaProductos tbody").append(resultado.datos);
                        // $("#subtotal").val(resultado.total);
                        // $("#impuesto").val(total_tax);
                        $("#total").val(resultado.total);
                        $("#id_producto").val('');
                        $("#code").val('');
                        $("#name").val('');
                        $("#cantidad").val('');
                        $("#price").val('');
                        $("#product_subtotal").val('');
                        $("#code").focus();
                    }

                }
            }
        });
    }
}

function eliminaProducto(id_producto, id_compra){
    $.ajax({
        url: '/eliminar/'+id_producto+'/'+id_compra,
        success: function(resultado){
            if(resultado==0){
                document.getElementById('resultado_error').innerText = "";
            }else{
                var resultado = resultado;
                $("#tablaProductos tbody").empty();
                $("#tablaProductos tbody").append(resultado.datos);
                $("#total").val(resultado.total);
            }
        }
    });
}

// cargar valores de las variables con los ids de inputs
function ventaAgrega(id_producto, cantidad, id_compra){
    
    if(id_producto != null && id_producto != 0 && cantidad > 0){
        $.ajax({
            url:'/temporalVenta/'+ id_producto +'/'+cantidad+'/'+id_compra,
            success: function(resultado){
                if(resultado==0){

                }else{

                    var resultado = resultado;
                    if(resultado.error == ""){
                        // var tax = 0.15
                        // var total_tax = (resultado.total * tax).toFixed(2)
                        // var compra_total = (total_tax + resultado.total).toFixed(2)
                        $("#tablaProductos tbody").empty();
                        $("#tablaProductos tbody").append(resultado.datos);
                        // $("#subtotal").val(resultado.total);
                        // $("#impuesto").val(total_tax);
                        $("#total").val(resultado.total);
                        $("#id_producto").val('');
                        $("#code").val('');
                        $("#name").val('');
                        $("#cantidad").val('');
                        $("#price").val('');
                        $("#product_subtotal").val('');
                        $("#code").focus();
                    }

                }
            }
        });
    }
}