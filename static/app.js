const form = document.querySelector('#art-form');
const fileInput = document.querySelector('#media');
const fileLabel = document.querySelector('#file-label');
const status = document.querySelector('#status');
const message = document.querySelector('#status-message');
const percent = document.querySelector('#percent');
const bar = document.querySelector('#bar');
const result = document.querySelector('#result');

fileInput.addEventListener('change', () => {
  fileLabel.textContent = fileInput.files[0]?.name || 'Choose a video or image';
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = document.querySelector('#artify');
  button.disabled = true;
  button.textContent = 'Artifying…';
  result.classList.add('hidden');
  status.classList.remove('hidden');
  try {
    const response = await fetch('/api/jobs', { method: 'POST', body: new FormData(form) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Could not start the render.');
    await watch(data.status_url);
  } catch (error) {
    message.textContent = error.message;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Artify <span>→</span>';
  }
});

async function watch(url) {
  const response = await fetch(url);
  const job = await response.json();
  message.textContent = job.message;
  percent.textContent = `${job.progress}%`;
  bar.style.width = `${job.progress}%`;
  if (job.status === 'complete') {
    document.querySelector('#preview').src = `${job.preview_url}?t=${Date.now()}`;
    document.querySelector('#save').href = job.download_url;
    result.classList.remove('hidden');
    return;
  }
  if (job.status === 'failed') throw new Error(job.error || 'The render failed.');
  setTimeout(() => watch(url), 400);
}
