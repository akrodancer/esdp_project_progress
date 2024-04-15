$(document).ready(function(){
    $(".owl-carousel").owlCarousel();
  });
  $('.owl-carousel').owlCarousel({
    center: true,
      loop:true,
      nav:true,
      mergeFit: true,
      responsive:{
          0:{
              items:1
          },
          778:{
              items:1
          },
          1000:{
              items:3
          }
      }
  })

  