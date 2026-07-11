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

    const body = new URLSearchParams(userData);

    fetch('/account/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body
    })
        .then(response => response.json())
        .then(data => {
            saveButton.setAttribute('data-bs-content', data.message);

            let popover = bootstrap.Popover.getInstance(saveButton);
            if (popover) popover.dispose();
            popover = new bootstrap.Popover(saveButton);
            popover.show();
        })
        .catch(error => {
            console.error('Ошибка при сохранении:', error);
        });
});
