// JavaScript to handle chat icon behavior
window.addEventListener('scroll', function() {
    var chatIcon = document.getElementById('chatIcon');
    if (window.scrollY > 100) { // Change 100 to the desired scroll position
      chatIcon.style.display = 'block';
    } else {
      chatIcon.style.display = 'none';
    }
  });
  