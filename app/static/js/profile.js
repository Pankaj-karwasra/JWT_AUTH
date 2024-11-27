document.getElementById('profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;

    const response = await fetch('/api/account/profile/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ first_name: firstName, last_name: lastName })
    });

    const data = await response.json();
    if (response.ok) {
        alert('Profile updated successfully!');
    } else {
        alert('Error updating profile');
    }
});

document.getElementById('logout-btn').addEventListener('click', async () => {
    const response = await fetch('/api/account/logout/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    });

    const data = await response.json();
    if (response.ok) {
        alert('Logged out successfully!');
        window.location.href = "/login/"; // Redirect to login page
    } else {
        alert('Error logging out');
    }
});
