let token = localStorage.getItem('token');

function showLoginForm() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}

function showDashboard() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
    updateSensorData();
}

document.getElementById('login').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            localStorage.setItem('token', token);
            showDashboard();
        } else {
            alert('Login failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('adjustFans').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/adjust_fans', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('fanStatus').textContent = `Fan speed adjusted to ${data.speed}%`;
        } else {
            alert('Failed to adjust fan speed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

async function updateSensorData() {
    try {
        const response = await fetch('/api/sensor_data', {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const data = await response.json();
            updateCharts(data);
        } else {
            console.error('Failed to fetch sensor data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateCharts(data) {
    // Implement chart updating logic here
    // You can use a library like Chart.js for this
    console.log('Updating charts with data:', data);
}

// Check if user is logged in
if (token) {
    showDashboard();
} else {
    showLoginForm();
}

// Update sensor data every 30 seconds
setInterval(updateSensorData, 30000);
