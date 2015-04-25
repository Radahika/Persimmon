$(document).ready(function () {
  $("#summarizerForm").submit(function (event) {
    event.preventDefault();

    $.ajax("/summary", {
      method: "POST",
      data: {
        text: $("#unsummarizedText").val()
      },
      success: function (data) {
        console.log(data);
      },
      error: function (xhr, textStatus, error) {
        console.log("Error in fetching summary: " + textStatus);
      }
    });
  });
});
