/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
// get stripe public key using jquery 
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// customer secret id
var stripe = Stripe(stripePublicKey);
// variable with the stripe public key
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
        // it turns red when the number is invalid
    }
};
var card = elements.create('card', {style: style});
// card element with style
card.mount('#card-element');


// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit by getting all the element by ID with payment-form
var form = document.getElementById('payment-form');

// checkout view will create a stripe payment
form.addEventListener('submit', function(ev) {
    //add an event listener with submit 
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        // stripe confirm a secret which return to the template as a clientSecret variable
        payment_method: {
            // using the cliente secret to confirm the cardpayment
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            // if there is any error then a message will show
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            //otherwise payment succeeded
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});