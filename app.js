const form = document.getElementById('noteForm');
const notesEl = document.getElementById('notes');
const flashcardsEl = document.getElementById('flashcards');
const statusEl = document.getElementById('status');
const loadSavedBtn = document.getElementById('loadSavedBtn');
const savedEl = document.getElementById('saved');

function cardTemplate(q, a) {
  return `
    <div class="card">
      <div class="inner">
        <div class="face front"><strong>Q:</strong> ${q}</div>
        <div class="face back"><strong>A:</strong> ${a}</div>
      </div>
    </div>
  `;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const notes = notesEl.value.trim();
  if (!notes) return;
  statusEl.textContent = 'Generating flashcards...';
  flashcardsEl.innerHTML = '';
  try {
    const res = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to generate');
    data.forEach(c => {
      flashcardsEl.insertAdjacentHTML('beforeend', cardTemplate(c.question, c.answer));
    });
    statusEl.textContent = 'Done! (Saved to database)';
  } catch (err) {
    statusEl.textContent = 'Error: ' + err.message;
  }
});

loadSavedBtn.addEventListener('click', async () => {
  statusEl.textContent = 'Loading saved flashcards...';
  savedEl.innerHTML = '';
  try {
    const res = await fetch('/flashcards');
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to load saved');
    data.forEach(c => {
      savedEl.insertAdjacentHTML('beforeend', cardTemplate(c.question, c.answer));
    });
    statusEl.textContent = 'Loaded saved flashcards.';
  } catch (err) {
    statusEl.textContent = 'Error: ' + err.message;
  }
});