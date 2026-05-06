$('#auth-button').click(
    function() {
        let email = $('#email').val();
        let password = $('#password').val();
        let authButton = $('#auth-button');
        const CSRF = $('[name=csrfmiddlewaretoken]').val();
        
        if(!email) {
            alert('Введите адрес электронной почты!');
        }

        if(!password) {
            alert('Введите пароль!');
        }

        let userData = {
            'email' : email,
            'password' : password,
            'csrfmiddlewaretoken': CSRF
        }

        $.ajax({
            url: '/auth/',
            type: 'POST',
            dataType: 'json',
            data: userData,

            success: function() {
                window.location.href = '/';
            },
            error: function(xhr) {
                if(xhr.responseJSON) {
                    authButton.attr('data-bs-content', xhr.responseJSON.message);

                    let popover = bootstrap.Popover.getInstance(authButton[0]);
                    if(popover) popover.dispose();
                    popover = new bootstrap.Popover(authButton[0]);
                    popover.show();
                }
            },
        });
    }
);