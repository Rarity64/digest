document.getElementById('save-button').addEventListener('click', function() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const birthdate = document.getElementById('birthdate').value;
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const subscribed = document.getElementById('subscribed').checked;
    const saveButton = document.getElementById('save-button');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const userData = {
        'email' : email,
        'password' : password,
        'birthdate' : birthdate,
        'firstName' : firstName,
        'lastName' : lastName,
        'subscribed' : subscribed,
        'csrfmiddlewaretoken': csrfToken
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
});
