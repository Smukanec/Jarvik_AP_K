async function send() {
  const text = document.getElementById('input').value;
  const user = document.getElementById('user').value;
  const res = await fetch('/action_plan', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text, user})
  });
  const data = await res.json();
  addRow(data.record);
}

function addRow(rec) {
  const tbody = document.querySelector('#records tbody');
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${rec.id}</td><td>${rec.traceability}</td><td>${rec.problem}</td><td>${rec.cause}</td><td>${rec.action}</td>`;
  tbody.appendChild(tr);
}
