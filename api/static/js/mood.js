const prev = document.getElementById('prev-btn');
const next = document.getElementById('next-btn');
const list = document.getElementById('item-list');

const itemWidth = 450;
const padding = 10;
let autoScrollInterval;

function startAutoScroll(direction) {
  stopAutoScroll(); // Stop existing interval to avoid overlaps
  autoScrollInterval = setInterval(() => {
    // Smaller increment for smoother scrolling
    list.scrollLeft += direction * 15; // Adjust the number for speed control
  }, 20); // A shorter interval for a smoother transition
}

function stopAutoScroll() {
  clearInterval(autoScrollInterval);
}

// Event listeners for buttons
prev.addEventListener('click', () => {
  list.scrollLeft -= itemWidth + padding;
});

next.addEventListener('click', () => {
  list.scrollLeft += itemWidth + padding;
});

// Event listeners for auto-scroll on hover
list.addEventListener('mouseenter', (event) => {
  const listRect = list.getBoundingClientRect();
  const relativeX = event.clientX - listRect.left;

  // Check if the mouse is in the left or right half of the list
  if (relativeX < listRect.width / 2) {
    startAutoScroll(-1); // Scrolls to the left
  } else {
    startAutoScroll(1); // Scrolls to the right
  }
});

list.addEventListener('mouseleave', stopAutoScroll);

/*

//share button

document.getElementById("share").addEventListener("click", function(event) {
  event.preventDefault(); // Prevents the default behavior of the anchor link
  // Hide the share icon
  document.getElementById("share").style.display = "none";

  // Show the other SVGs
  document.getElementById("facebook").classList.toggle("hidden");
  document.getElementById("twitter_x").classList.toggle("hidden");
  
});

*/
