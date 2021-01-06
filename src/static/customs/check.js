// Verificar codigos de productos
$(document).ready(function() {
    // $('form').on('submit', function(event){ 
    //     $ajax({
    //         data:{
    //             // name: $('#productName').val(),
    //             code: $('#productCode').val()
    //         },
    //         // type: 'POST',
    //         url: '/nuevo_producto'
    //     })
    //     .done(function(data){
    //         if(data.error){
    //             $('#errorAlert').text(data.error).show();
    //             $('#successAlert').hide();
    //         }
    //         else{
    //             $('#successAlert').text(data.name).show();
    //             $('#errorAlert').hide();
    //         }

    //     });

    //     event.preventDefault();

    // });

    $('form').on('submit', function(e) {
     
    //  $('#loading').show();
     var productCode = $('#productCode').val();
     var productName = $('#productName').val();
     var productPriceSale = $('#productPriceSale').val();
      
    //  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;
      
     if(productName != "" && productPriceSale != "") {
        $.ajax({
            // method: "POST",
            url: '/nuevo_producto',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({'productCode': productCode, 'productName': productName, 'productPriceSale': productPriceSale}),
            dataType: "json",
            success: function(data) {
            //  $('#signupform').hide();
            //  $('#loading').hide();
            //  $('#msg').html('<span style="color: green;">You are registered successfully</span>');
            },statusCode: {
             409 : function() {
            //   $('#loading').hide();
              $('#msg').html('<span style="color: red;">Codigo ya existen en el sistema, ingrese nuevo codigo.</span>');
             }
            },
            error: function(err) {
             console.log(err);
            }
           });
     } else {
    //   $('#loading').hide();
      $('#msg').html('<span style="color: red;">El nombre y precio de producto son requeridos.</span>');
     }
    });
   });