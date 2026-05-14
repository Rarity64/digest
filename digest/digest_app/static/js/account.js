$('#save-button').click(
    function() {
        let email = $('#email').val();
        let password = $('#password').val();
        let birthdate = $('#birthdate').val();
        let firstName = $('#first-name').val();
        let lastName = $('#last-name').val();
        let subscribed = $('#subscribed').prop('checked');
        console.log($('#subscribed'));
        let saveButton = $('#save-button');

        const CSRF = $('[name=csrfmiddlewaretoken]').val();

        let userData = {
            'email' : email,
            'password' : password,
            'birthdate' : birthdate,
            'firstName' : firstName,
            'lastName' : lastName,
            'subscribed' : subscribed,
            'csrfmiddlewaretoken': CSRF
        }

        $.ajax({
            url: '/account/',
            type: 'POST',
            dataType: 'json',
            data: userData,

            success: 
                function(data) {
                    saveButton.attr('data-bs-content', data.message);

                    let popover = bootstrap.Popover.getInstance(saveButton[0]);
                    if(popover) popover.dispose();
                    popover = new bootstrap.Popover(saveButton[0]);
                    popover.show();
                },
        });
    }
);
