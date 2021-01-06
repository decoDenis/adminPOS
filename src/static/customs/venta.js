$(function(){
    $("#cliente").autocomplete({
        source: function(request, response) {
            $.getJSON("{{url_for('autocompleteData')}}",{
                term: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                response(data.returnData); // matching_results from jsonify
            });
        },
        minLenght: 3,
        select: function(event,ui){
            event.preventDefault();
            $("#id_cliente").value(ui.item.id)
            $("#cliente").value(ui.item.value)
        }
    });

});

$(function(){
    $("#codigo").autocomplete({
        source:'/autocompleteData',
        minLenght: 3,
        select: function(event, ui){
            event.preventDefault();
            $("#codigo").val(ui.item.nombre);
        }
    });

});

