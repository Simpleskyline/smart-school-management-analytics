checkAuth();

async function loadFees() {
    const students = await apiCall('/students/');
    const feesTable = document.getElementById('feesTable');
    
    if (!students) return;
    
    let allFees = [];
    for (const student of students) {
        const fees = await apiCall(`/fees/student/${student.id}`);
        if (fees) {
            allFees = allFees.concat(fees.map(f => ({
                ...f,
                student_name: `${student.first_name} ${student.last_name}`
            })));
        }
    }
    
    feesTable.innerHTML = allFees.length ? allFees.map(fee => `
        <tr>
            <td>${fee.student_name}</td>
            <td>${fee.fee_type}</td>
            <td>KES ${fee.amount}</td>
            <td>${fee.due_date}</td>
            <td><span class="badge-${fee.status.toLowerCase()}">${fee.status}</span></td>
            <td>
                <button class="btn-primary" onclick="recordPayment(${fee.id})">Record Payment</button>
            </td>
        </tr>
    `).join('') : '<tr><td colspan="6">No fees found</td></tr>';
}

async function recordPayment(feeId) {
    const amount = prompt('Enter payment amount:');
    if (!amount) return;
    
    await apiCall('/fees/payment', 'POST', {
        fee_id: feeId,
        amount_paid: parseFloat(amount),
        payment_date: new Date().toISOString().split('T')[0],
        payment_method: 'Cash'
    });
    
    alert('Payment recorded');
    loadFees();
}

loadFees();