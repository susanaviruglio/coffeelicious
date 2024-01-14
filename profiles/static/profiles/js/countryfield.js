let getCountryValue = $('#id_default_country').val();
//get the value of the country field
if(!getCountryValue) {
    // color default
    $('#id_default_country').css('color', '#414042');

}
$('#id_default_country').change(function() {
    getCountryValue = $(this).val();
    // everytime the box changes it gets its value
    if(!getCountryValue) {
        $(this).css('color', '#414042');
        // if country is not selected then is this color :#414042
    } else {
        $(this).css('color', '#000');
        // otherwise when the country field is selected, the color would be black
    }
});