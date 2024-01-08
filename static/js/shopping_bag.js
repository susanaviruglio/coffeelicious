    // Update quantity on click
    $('.update-link').click(function(e) {
        //update the item
        var form = $(this).prev('.update-form');
        form.submit();
    })

// Remove item and reload on click
$('.remove-item').click(function(e) {
    e.preventDefault();

    
    var csrfToken = $("[name=csrfmiddlewaretoken]").val();
    // taken from django protection which retrieve token from form

    var itemId = $(this).attr('id').split('remove_')[1];
    // take the item id from the button id
    var url = `/shopping/remove/${itemId}/`;
    // I had some issues to remove the item and the url 

    var data = {'csrfmiddlewaretoken': csrfToken};
    // I had to prepare the data for Ajax request to avoid errors

    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(response) {
            // reload the site once the item is removed 
            location.reload();
        },
        error: function(response) {
            console.error(response);
            // log console errors if the error persist
        }
    });
});