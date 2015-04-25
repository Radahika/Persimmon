$(document).ready(function () {
  $("#navbar_summarizer").addClass("active");

  // Summarizer Form
  $("#summarizerForm").submit(function (event) {
    event.preventDefault();

    $.ajax("/summary", {
      method: "POST",
      data: {
        text: $("#unsummarizedText").val()
      },
      success: function (data) {
        $("#summary").text(data);
      },
      error: function (xhr, textStatus, error) {
        console.log("Error in fetching summary: " + textStatus);
      }
    });
  });

  // Navbar
  $(".sentiment_filter").click(function () {
    var $this = $(this);
    var id = $this.attr("id");

    var wantedSentiment = id.split("_")[1];

    window.location.href = "/#"+wantedSentiment;
  });
});
