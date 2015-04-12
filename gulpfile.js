var gulp = require("gulp"),
  run = require("gulp-run"),
  browserify = require("browserify"),
  jshint = require("gulp-jshint"),
  browserSync = require("browser-sync"),
  source = require("vinyl-source-stream"),
  buffer = require("vinyl-buffer"),
  reactify = require("reactify"),
  reload = browserSync.reload;

var jsPath = "website/static/app"
// Running Bower

gulp.task("bower", function () {
  run ("bower install").exec();
})


.task("serve", ["bower"], function () {
})

.task("default", function () {
  gulp.start("serve");
});




