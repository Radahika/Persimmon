var gulp = require("gulp"),
  run = require("gulp-run"),
  browserify = require("browserify"),
  jshint = require("gulp-jshint"),
  browserSync = require("browser-sync"),
  source = require("vinyl-source-stream"),
  buffer = require("vinyl-buffer"),
  reactify = require("reactify"),
  reload = browserSync.reload;

// Running Bower

gulp.task("bower", function () {
  run ("bower install").exec();
})

// Validation

.task("lint", function () {
  return gulp.src(package.paths.js)
  .pipe(jshint())
  .pipe(jshint.reporter("default"));
})

// JS compilation

.task("js", function () {
  return browserify(package.paths.app)
  .transform(reactify)
  .bundle()
  .pipe(source(package.dest.app))
  .pipe(gulp.dest(package.dest.dist));
})

.task("serve", ["bower", "lint", "js"], function () {
  return gulp.watch([
    package.paths.js, package.paths.jsx, package.paths.html
  ], [
    "lint", "js"
  ]);
})

.task("default", function () {
  gulp.start("serve");
});




