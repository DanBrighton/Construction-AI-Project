document.querySelector('.bar-btn').addEventListener('click', function(event) {
    document.getElementById('userDropdown').style.display = 'flex';
    event.stopPropagation();
});

window.addEventListener('click', function() {
    document.getElementById('userDropdown').style.display = 'none';
});