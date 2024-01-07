/**
 * The use is able to purchase items from 1 to 99 by using the arrows next to the number, 
 * if they want to add more than 99 automatically it will change back.
 */

    // function to handle the value of items from 1 to 99
    function handleEnableDisable(itemId) {
        var currentValue = parseInt($(`#id_qty_${itemId}`).val());
        // current value is the id of input number
        var minusDisabled = currentValue < 2;
        // minimum value must be less than 2, so 1
        var plusDisabled = currentValue > 98;
        // maximum value must be more than 98, so 99
        $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
        // prop method to disable the buttons and set them true or false
        $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
    }

    // call enabling/disabling of all the inputs when the page loads
    var allQtyInputs = $('.qty_input');
    // using a for loop to iterate all the inputs
    for(var i = 0; i < allQtyInputs.length; i++){
        var itemId = $(allQtyInputs[i]).data('item_id');
        handleEnableDisable(itemId);
    }

    // Check enable/disable every time the input is changed
    $('.qty_input').change(function() {
        var itemId = $(this).data('item_id');
        // to ensure that changes the values 
        handleEnableDisable(itemId);
        // and passed the id to the enable and disable
    });

    // Increment quantity
    $('.increment-qty').click(function(e) {
       e.preventDefault();
       var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
       //to find the closest input group class
       var currentValue = parseInt($(closestInput).val());
       // get the current value with the parseInt method
       $(closestInput).val(currentValue + 1);
       // take away one to the current value
       var itemId = $(this).data('item_id');
       // call the function everytime is clicked by using the data method
       handleEnableDisable(itemId);
       // and passed the id to the enable and disable
    });

    // Decrement quantity
    $('.decrement-qty').click(function(e) {
       e.preventDefault();
       var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
       //to find the closest input group class
       var currentValue = parseInt($(closestInput).val());
       // get the current value with the parseInt method
       $(closestInput).val(currentValue - 1);
       // adding 1 to the current value
       var itemId = $(this).data('item_id');
       // call the function everytime is clicked by using the data method
       handleEnableDisable(itemId);
       // and passed the id to the enable and disable
    });
