$(document).ready(function () {

  // Facebook Login/Logout
  window.statusChangeCallback = function (response) {
    var $status = $("#status");
    var $button = $("#facebookLoginButton");
    var $feed = $("#feed");
    $feed.html("");
    if (response.status === LOGIN_STATUS_LOGGED_IN) {
      $status.text("");
      requestHome();
      $button.hide();
    } else if (response.status === LOGIN_STATUS_NEED_APP_LOGIN) {
      $button.show();
      $status.text("Please log into the app");
    } else {
      $button.show();
      $status.text("Please log into Facebook.");
    }
  };


  var allPosts = [];
  var parseHomeFeed = function (feed) {
    for (var i = 0; i < feed.length; i++) {
      var post = feed[i];
      allPosts.push(post);
    }
    var sentiment = window.location.hash.substr(1);

    if (sentiment.length > 0) {
      requestFilter(sentiment);
    } else {
      requestFilter();
    }
  };

  var requestHome = function () {
    $("body").addClass("loading");
    FB.api("/me/home", { limit: 50 }, function (response) {
      parseHomeFeed(response.data);
    });
  };

  var display_feed = function (posts) {
    var $feed = $("#feed");
    $feed.html("");
    $("body").removeClass("loading");
    for (i = 0; i < posts.length; i++) {
      var post = posts[i];
      var template = $('#template').html();
      Mustache.parse(template);
      var rendered = Mustache.render(template, {"author": post.author, "text": post.text, "summary": post.summary, "id":i});
      $feed.prepend(rendered);
    }
  };

  var requestFilter = function (sentiment) {
    if (!sentiment) {
      sentiment = "all";
    }

    // allPosts is a global variable
    $.post("/filter_page", { "posts": JSON.stringify(allPosts), "sentiment": sentiment }, function (response) {
      display_feed(response.posts);
    }, "json");
  };


  // Navbar Shenanigans
  $(".sentiment_filter").click(function () {
    var $this = $(this);
    var id = $this.attr("id");

    var wantedSentiment = id.split("_")[1];
    requestFilter(wantedSentiment);
  });
});
