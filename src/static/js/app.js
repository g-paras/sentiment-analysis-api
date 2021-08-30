// this is same as the script.js but i am using a different approach
$(document).ready(function () {
  $("#form").submit(function (e) {
    e.preventDefault();

    var text = $("#text").val();
    $.post(
      "/fastapi",
      {
        text: text,
      },
      function (data, status) {
        $("#ans").html(data.sentiment);
        $("#text").val(null);
      }
    );
  });
});
