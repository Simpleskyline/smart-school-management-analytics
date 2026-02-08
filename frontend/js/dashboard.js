checkAuth();

async function loadDashboardData() {
    const students = await apiCall('/students/');
    const teachers = await apiCall('/teachers/');
    const classes = await apiCall('/classes/');
    
    document.getElementById('totalStudents').textContent = students?.length || 0;
    document.getElementById('totalTeachers').textContent = teachers?.length || 0;
    document.getElementById('totalClasses').textContent = classes?.length || 0;
    
    const user = JSON.parse(localStorage.getItem('user'));
    document.getElementById('userName').textContent = user?.username || 'User';
    
    // Attendance Chart
    const attendanceCtx = document.getElementById('attendanceChart').getContext('2d');
    new Chart(attendanceCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            datasets: [{
                label: 'Attendance %',
                data: [95, 92, 97, 90, 94],
                borderColor: '#667eea',
                tension: 0.4
            }]
        }
    });
    
    // Fee Chart
    const feeCtx = document.getElementById('feeChart').getContext('2d');
    new Chart(feeCtx, {
        type: 'bar',
        data: {
            labels: ['Tuition', 'Transport', 'Library', 'Lab'],
            datasets: [{
                label: 'Collection (KES)',
                data: [450000, 120000, 35000, 80000],
                backgroundColor: '#27ae60'
            }]
        }
    });
}

loadDashboardData();

