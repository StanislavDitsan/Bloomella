// Script for toast 
$('.toast').toast('show');

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