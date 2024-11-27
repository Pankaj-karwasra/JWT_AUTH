document.getElementById('reset-password-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (newPassword !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    const response = await fetch('/api/account/reset-password/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password: newPassword })
    });

    const data = await response.json();
    if (response.ok) {
        alert('Password reset successfully!');
        window.location.href = "/login/"; 
    } else {
        alert('Error resetting password');
    }
});
