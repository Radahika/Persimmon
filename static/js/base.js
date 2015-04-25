$(document).ready(function () {
  // Facebook login constants
  window.LOGIN_STATUS_LOGGED_IN = "connected";
  window.LOGIN_STATUS_NEED_APP_LOGIN = "not_authorized";

  window.fbAsyncInit = function() {
    FB.init({
      appId      : '802564089839704',
      xfbml      : true,
      version    : 'v2.3'
    });
    FB.getLoginStatus(function (response) {
      if (window.statusChangeCallback) {
        window.statusChangeCallback(response);
      }
    });
  };

  window.checkLoginState = function () {
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

  // Nav Bar
  $("#logout").click(function () {
    FB.logout(function (response) {
      window.checkLoginState();
    });
  });
});
