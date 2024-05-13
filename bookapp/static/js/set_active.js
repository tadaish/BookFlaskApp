var pages = document.querySelectorAll('.page-item');

pages.forEach(function(page) {
    page.addEventListener('click', function() {
        pages.forEach(function(item) {
            item.classList.remove('active');
        });
            this.classList.add('active');
            sessionStorage.setItem('currItem', this.id)
    });
});

var currItem = sessionStorage.currItem

if (currItem){
    var activeItem = document.getElementById(currItem)
    sessionStorage.removeItem('currItem')
    activeItem.classList.add('active')
}