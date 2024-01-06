
// Click arrow to scroll to the top of the page, the links are from bootstrap or font awesome
$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
})




// JavaScript to sort Product items; to get source event iself
$('#sort-selector').change(function() {
    var selector = $(this); // this is for the sort selector
    var currentUrl = new URL(window.location); // the current url location

    var selectedVal = selector.val(); //value from the selected box
    if(selectedVal != "reset"){ // if reset is not apply then sort
        var sort = selectedVal.split("_")[0]; // the first item selected will be the one sorted
        var direction = selectedVal.split("_")[1]; // the second is the direction up or down

        currentUrl.searchParams.set("sort", sort); // replace parameters sort with set method
        currentUrl.searchParams.set("direction", direction); // replace parameters direction with set method

        window.location.replace(currentUrl); //replace current location for a new url
    } else { // otherwise user selected reset
        currentUrl.searchParams.delete("sort"); // delete sort parameter
        currentUrl.searchParams.delete("direction"); // delete direction parameter

        window.location.replace(currentUrl); // replace location to current location
    }
})