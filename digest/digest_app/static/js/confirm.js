$('#confirm-button').click(
    function() {
        let emailCode = $('#email-code').val();
        let confirmButton = $('#confirm-button');

        confirmButton.prop('disabled', true);
        confirmButton.prop('hidden', true);
        $('.confirm').append(`
            <div id="confirm-spinner" class="spinner-border mt-2" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `)

        const CSRF = $('[name=csrfmiddlewaretoken]').val();
        
        let userData = {
            'email-code' : emailCode,
            'csrfmiddlewaretoken': CSRF
        }

        $.ajax({
            url: '/confirm/',
            type: 'POST',
            dataType: 'json',
            data: userData,

            success: function(data) {
                window.location.href = '/';
            },

            error: function(xhr) {
                if(xhr.responseJSON) {
                    $('#confirm-spinner').remove();
                    confirmButton.val(xhr.responseJSON.message);
                    confirmButton.css('background-color', 'red');
                }
            }   
        });
    }
);