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

  var requestHome = function () {
    FB.api("/me/home", function (response) {
      console.log(response);
      for (var i = 0; i < response.data.length; i++) {
        var post = response.data[i];
        if (post.message) {
          var text = post.message;
          $.post("/summary", { text: text }, function (response) {
            console.log("Before text");
            console.log(text);
            console.log("After text");
            console.log(response);
          });
        }
      }
      //var after = response.paging.cursors.after;
      //FB.api("/me/home", { after: after }, function (response) {
      //  console.log(response);
      //});
    });
  };
});
