/* window.onload = function() {
    startScrolling;
} */

document.addEventListener('readystatechange', (event) => {
    if (document.readyState === 'complete') {
        startScrolling();
    }
});

/* document.addEventListener('DOMContentLoaded', (event) => {
    startScrolling();
}); */

const itemList = document.getElementById('item-list');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
// const items = itemList.querySelectorAll('.item');

let scrollingInterval;
let scrollDirection = 1; // 1 for scrolling right, -1 for scrolling left

function startScrolling() {
    if (scrollingInterval) return; // Prevent multiple intervals
    scrollingInterval = setInterval(() => {
	itemList.scrollLeft += scrollDirection * 10; // Adjust the scrolling speed as needed
    }, 50); // Adjust the interval for smoother scrolling
}

/* function stopScrolling() {
    clearInterval(scrollingInterval);
    scrollingInterval = null; // Clear the interval reference
} */

function stopScrolling() {
    if (scrollingInterval) {
        clearInterval(scrollingInterval);
        scrollingInterval = null; // Clear the interval reference
    }
}

// window.onload = startScrolling;

// Stop scrolling when the mouse enters the item list
itemList.addEventListener('mouseenter', stopScrolling);

// Resume scrolling when the mouse leaves the item list
itemList.addEventListener('mouseleave', () => {
    scrollDirection = 1; // Ensure direction is set to right when resuming
    startScrolling();
});

// Change direction and start scrolling left when hovering over the prev button
prevBtn.addEventListener('mouseenter', () => {
    scrollDirection = -1; // Set direction to left when hovering over prev-btn
    startScrolling(); // Start scrolling immediately
});

// Resume scrolling to the right when the mouse leaves the prev button
prevBtn.addEventListener('mouseleave', () => {
    scrollDirection = 1; // Set direction back to right when not hovering over prev-btn
    startScrolling(); // Start scrolling immediately
});


// Change direction and start scrolling right when hovering over the next button
nextBtn.addEventListener('mouseenter', () => {
    scrollDirection = 1; // Set direction to right when hovering over next-btn
    startScrolling(); // Start scrolling immediately
});



// Stop any ongoing scrolling and manually scroll left when the prev button is clicked
prevBtn.addEventListener('click', () => {
    stopScrolling(); // Stop scrolling before manual scroll
    itemList.scrollBy({
	left: -500, // Scroll left by 500 px, adjust as needed
	behavior: 'smooth' // Add smooth scrolling behavior
    });
});

// Stop any ongoing scrolling and manually scroll right when the next button is clicked
nextBtn.addEventListener('click', () => {
    stopScrolling(); // Stop scrolling before manual scroll
    itemList.scrollBy({
	left: 500, // Scroll right by 500 px, adjust as needed
	behavior: 'smooth' // Add smooth scrolling behavior
  });
});
