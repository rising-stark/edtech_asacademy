jQuery(window).bind('scroll', function() {
  if (jQuery(window).scrollTop() > 900) {
    jQuery('#main-nav').addClass('navbar-fixed-top');
  } else {
    jQuery('#main-nav').removeClass('navbar-fixed-top');
  }
});

jQuery(document).ready(function($) {
  "use strict";
  $('#main-nav .nav').onePageNav({
    currentClass: 'active',
    scrollOffset: 69,
  });
});

$(document).ready(function() {

  //.parallax(xPosition, speedFactor, outerHeight) options:
  //xPosition - Horizontal position of the element
  //inertia - speed to move relative to vertical scroll. Example: 0.1 is one tenth the speed of scrolling, 2 is twice the speed of scrolling
  //outerHeight (true/false) - Whether or not jQuery should use it's outerHeight option to determine when a section is in the viewport
  $('#top').parallax("50%", 0.4);
  $('#testimonial').parallax("50%", 0.4);
  $('#download').parallax("50%", 0.4);
})


$(document).ready(function() {
  $(".owl-carousel").owlCarousel({
    autoPlay: 3000,
    items: 4,
    itemsDesktop: [1199, 3],
    itemsDesktopSmall: [979, 3]
  });
});

jQuery(function($) {
  $('#download-app1').localScroll({
    duration: 1200
  });
  $('#download-app2').localScroll({
    duration: 1000
  });
});





$(window).scroll(function(){
  if($(this).scrollTop() > 100){
      $('.navbar').addClass('sticky')
  } else{
      $('.navbar').removeClass('sticky')
  }
});



function mobileMenu() {
  var x = document.getElementById("menu");
  if (x.className === "mobile-menu") {
      x.className += " responsive";
  } else {
      x.className = "mobile-menu";
  }
}

var slideIndex = 1;
showSlides(slideIndex);

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("banner");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}