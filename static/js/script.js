// Script for footer 

$(document).ready(function () {
    var docHeight = $(window).height();
    var footerHeight = $('.footer').height();
    var footerTop = $('.footer').position().top + footerHeight;
    if (footerTop < docHeight) {
        $('.footer').css('margin-top', (docHeight - footerTop) + 'px');
    }
});

// Script for toast 
$('.toast').toast('show').delay(3000).fadeOut('slow');

// Header jQuery remove/add effect
let prevScrollPos = window.pageYOffset;

window.onscroll = function () {
    let currentScrollPos = window.pageYOffset;
    if (prevScrollPos > currentScrollPos) {
        document.querySelector(".sticky-top").classList.remove("hidden");
    } else {
        document.querySelector(".sticky-top").classList.add("hidden");
    }
    prevScrollPos = currentScrollPos;
}