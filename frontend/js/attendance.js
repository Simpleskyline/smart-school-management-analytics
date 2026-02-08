checkAuth();

let attendanceData = [];

async function loadClasses() {
    const classes = await apiCall('/classes/');
    const select = document.getElementById('classSelect');
    
    select.innerHTML = '<option value="">Select Class</option>' + 
        (classes || []).map(c => `<option value="${c.id}">${c.class_name} ${c.section || ''}</option>`).join('');
}

async function loadStudentsForAttendance() {
    const classId = document.getElementById('classSelect').value;
    const date = document.getElementById('attendanceDate').value;
    
    if (!classId || !date) {
        alert('Please select class and date');
        return;
    }
    
    const students = await apiCall(`/students/`);
    const tbody = document.getElementById('attendanceTable');
    
    tbody.innerHTML = (students || []).map((student, index) => `
        <tr>
            <td>${student.first_name} ${student.last_name}</td>
            <td>${student.admission_number}</td>
            <td>
                <select id="status_${student.id}">
                    <option value="Present">Present</option>
                    <option value="Absent">Absent</option>
                    <option value="Late">Late</option>
                </select>
            </td>
            <td><input type="text" id="remarks_${student.id}" placeholder="Remarks"></td>
        </tr>
    `).join('');
    
    attendanceData = students;
}

async function saveAttendance() {
    const classId = document.getElementById('classSelect').value;
    const date = document.getElementById('attendanceDate').value;
    
    for (const student of attendanceData) {
        const status = document.getElementById(`status_${student.id}`).value;
        const remarks = document.getElementById(`remarks_${student.id}`).value;
        
        await apiCall('/attendance/mark', 'POST', {
            student_id: student.id,
            class_id: classId,
            date,
            status,
            remarks
        });
    }
    
    alert('Attendance saved successfully');
}

document.getElementById('attendanceDate').valueAsDate = new Date();
loadClasses();