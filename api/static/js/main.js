const itemList = document.getElementById('item-list');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const items = itemList.querySelectorAll('item');

let scrollingInterval;
let scrollDirection = 1; // 1 for scrolling right, -1 for scrolling left

function startScrolling() {
  scrollingInterval = setInterval(() => {
    itemList.scrollLeft += scrollDirection * 15; // Adjust the scrolling speed as needed
  }, 10); // Adjust the interval for smoother scrolling
}

function stopScrolling() {
  clearInterval(scrollingInterval);
}

itemList.addEventListener('mouseenter', stopScrolling);
itemList.addEventListener('mouseleave', startScrolling);

prevBtn.addEventListener('mouseenter', () => {
  scrollDirection = -1; // Set direction to left when hovering over prev-btn
});

prevBtn.addEventListener('mouseleave', () => {
  scrollDirection = 1; // Set direction back to right when not hovering over prev-btn
});

nextBtn.addEventListener('mouseenter', () => {
  scrollDirection = 1; // Set direction to right when hovering over next-btn
});

function checkScrollPosition() {
  const scrollPosition = itemList.scrollLeft;
  const itemWidth = items[0].offsetWidth;
  const itemListWidth = itemList.scrollWidth;

  if (scrollDirection === 1 && scrollPosition >= itemListWidth - itemList.offsetWidth) {
    itemList.scrollTo({ left: 0, behavior: 'auto' });
  } else if (scrollDirection === -1 && scrollPosition <= 0) {
    itemList.scrollTo({ left: itemListWidth - itemWidth, behavior: 'auto' });
  }
}

function startScrollingOnLoad() {
  startScrolling();
}

window.onload = startScrollingOnLoad;

itemList.addEventListener('scroll', checkScrollPosition);
