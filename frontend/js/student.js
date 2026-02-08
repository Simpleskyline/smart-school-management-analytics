checkAuth();

async function loadStudents() {
    const students = await apiCall('/students/');
    const tbody = document.getElementById('studentsTable');
    
    if (!students || students.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No students found</td></tr>';
        return;
    }
    
    tbody.innerHTML = students.map(student => `
        <tr>
            <td>${student.admission_number}</td>
            <td>${student.first_name} ${student.last_name}</td>
            <td>${student.gender}</td>
            <td>${student.guardian_name || 'N/A'}</td>
            <td><span class="badge-${student.status.toLowerCase()}">${student.status}</span></td>
            <td>
                <button class="btn-danger" onclick="deleteStudent(${student.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function showAddModal() {
    document.getElementById('addModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('addModal').style.display = 'none';
}

document.getElementById('addStudentForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    const result = await apiCall('/students/', 'POST', data);
    
    if (result) {
        alert('Student added successfully');
        closeModal();
        loadStudents();
    }
});

async function deleteStudent(id) {
    if (!confirm('Delete this student?')) return;
    
    await apiCall(`/students/${id}`, 'DELETE');
    loadStudents();
}

loadStudents();