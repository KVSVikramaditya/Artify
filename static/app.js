const form = document.querySelector('#art-form');
const fileInput = document.querySelector('#media');
const fileLabel = document.querySelector('#file-label');
const status = document.querySelector('#status');
const message = document.querySelector('#status-message');
const percent = document.querySelector('#percent');
const bar = document.querySelector('#bar');
const result = document.querySelector('#result');
const controls = {
  width: { input: document.querySelector('#width'), output: document.querySelector('#detail-output'), format: value => value },
  fps: { input: document.querySelector('#fps'), output: document.querySelector('#motion-output'), format: value => `${value} fps` },
  contrast: { input: document.querySelector('#contrast'), output: document.querySelector('#contrast-output'), format: value => value < 1 ? 'Soft' : value > 1.2 ? 'Bold' : 'Balanced' },
};

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  fileLabel.textContent = file?.name || 'Add a video or image';
  document.querySelector('#format-note').textContent = file ? 'Ready to Artify' : 'Video or image';
});

Object.values(controls).forEach(({ input, output, format }) => {
  input.addEventListener('input', () => { output.textContent = format(input.value); });
});

document.querySelector('#reset').addEventListener('click', () => {
  controls.width.input.value = 140;
  controls.fps.input.value = 10;
  controls.contrast.input.value = 1.1;
  Object.values(controls).forEach(({ input, output, format }) => { output.textContent = format(input.value); });
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = document.querySelector('#artify');
  button.disabled = true;
  button.innerHTML = '<span>Creating your Artify…</span><span class="arrow">→</span>';
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
    button.innerHTML = '<span>Artify</span><span class="arrow">→</span>';
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
