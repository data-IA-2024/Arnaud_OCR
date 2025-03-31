document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const errorToast = document.getElementById('error-toast');
    const errorToastBody = document.getElementById('error-toast-body');
    const errorToastInstance = new bootstrap.Toast(errorToast);
    const loginbutton = document.getElementById("connect");
  
    loginbutton.addEventListener('click', async (e) => {
        e.preventDefault();
        const formData = new URLSearchParams(new FormData(loginForm));
        console.log('do')
        try {
            const response = await fetch('/login', {
                method: 'POST',
                body: formData,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                credentials: 'include'
            });
  
            if (response.ok) {
                window.location.href = '/';
            } else {
                const error = await response.json();
                errorToastBody.textContent = `Erreur: ${error.detail}`;
                errorToastInstance.show();
            }
        } catch (error) {
            errorToastBody.textContent = "Erreur de connexion au serveur";
            errorToastInstance.show();
        }
    });
  });