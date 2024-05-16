var filter = document.getElementById('filter');

filter.addEventListener('change', function() {
    var selectedOption = this.options[this.selectedIndex];
    sessionStorage.setItem('selectedOption', selectedOption.id);
    var selectedValue = this.value;
    if (selectedValue){
        location.href = selectedValue;
    }
});


if (sessionStorage.selectedOption){
    var options = filter.options;
    Array.from(options).forEach(function(o) {
        if(o.id === sessionStorage.selectedOption) {
            o.setAttribute('selected', null)
        }
    })
    sessionStorage.removeItem('selectedOption')
};