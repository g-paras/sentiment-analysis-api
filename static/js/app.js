// this is same as the script.js but i am using a different approach
$(document).ready(function () {

    $("#text").keyup(function () {

        var text = $("#text").val();
        $.post('/fastapi', {
            text : text
        }, function (data, status) {
            $("#ans").html(data.sentiment);
        });

    });

});