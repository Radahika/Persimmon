$(document).ready(function () {
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '802564089839704',
      xfbml      : true,
      version    : 'v2.3'
    });
    FB.getLoginStatus(function (response) {
      statusChangeCallback(response);
    });
  };

  var statusChangeCallback = function (response) {
    if (response.status === "connected") {
      requestHome();
    } else if (response.status === "not_authorized") {
      document.getElementById("status").innerHTML = "Please log into the app";
    } else {
      document.getElementById("status").innerHTML = "Please log into Facebook";
    }
  };

  var checkLoginState = function () {
    FB.getLoginStatus(function (response) {
      statusChangeCallback(response);
    });
  };

  (function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  var allPosts = [];
  var parseHomeFeed = function (feed) {
    for (var i = 0; i < feed.length; i++) {
      var post = feed[i];
      allPosts.push(post);
    }
  };

  /*
  var requestNext = function (afterToken) {
    FB.api("/me/home", { after: afterToken, limit: 100 }, function (response) {
      parseHomeFeed(response.data);
    });
  };
 */

  var requestHome = function () {
    $("body").addClass("loading");
    FB.api("/me/home", { limit: 500 }, function (response) {
      parseHomeFeed(response.data);

      $.post("/filter_page", { "posts": JSON.stringify(allPosts) }, function (response) {
        function display_feed() {
            posts = response.posts
            for (i = 0; i < posts.length; i++) {
              post = posts[i]
              var template = $('#template').html();
              Mustache.parse(template);
              var rendered = Mustache.render(template, {"author": post.author, "text": post.text, "summary": post.summary, "id":i});
              $("#feed").prepend(rendered);
            }
        }
        display_feed();

      }, "json");

    });
  };

  $("div.post").click(function() {
    alert("Here")
    $(this.find(".full")).toggle( "display" );
   });
});
