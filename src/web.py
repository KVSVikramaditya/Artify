"""Local Flask application for Artify."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

from .config import RenderConfig
from .media import SUPPORTED_EXTENSIONS, render_media


@dataclass
class RenderJob:
    id: str
    input_path: Path
    status: str = "queued"
    message: str = "Waiting to start"
    completed: int = 0
    total: int = 1
    output_path: Path | None = None
    error: str | None = None
    created_at: float = field(default_factory=time.time)

    @property
    def percent(self) -> int:
        return min(100, round(self.completed / max(self.total, 1) * 100))


class JobStore:
    def __init__(self, base: Path) -> None:
        self.uploads = base / "uploads"
        self.results = base / "results"
        self.uploads.mkdir(parents=True, exist_ok=True)
        self.results.mkdir(parents=True, exist_ok=True)
        self.jobs: dict[str, RenderJob] = {}
        self.lock = threading.Lock()

    def add(self, input_path: Path) -> RenderJob:
        job = RenderJob(id=uuid.uuid4().hex, input_path=input_path)
        with self.lock:
            self.jobs[job.id] = job
        return job

    def get(self, job_id: str) -> RenderJob | None:
        with self.lock:
            return self.jobs.get(job_id)


def create_app(runtime_dir: Path | None = None) -> Flask:
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024
    base = (runtime_dir or Path.cwd() / ".artify").resolve()
    store = JobStore(base)

    @app.get("/")
    def index():
        return render_template("index.html", accepted=sorted(SUPPORTED_EXTENSIONS))

    @app.post("/api/jobs")
    def create_job():
        upload = request.files.get("media")
        if not upload or not upload.filename:
            return jsonify(error="Choose a video or image first."), 400
        filename = secure_filename(upload.filename)
        extension = Path(filename).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            return jsonify(error="That file type is not supported yet."), 400
        upload_path = store.uploads / f"{uuid.uuid4().hex}_{filename}"
        upload.save(upload_path)
        job = store.add(upload_path)
        options = {
            "width": int(request.form.get("width", 140)),
            "fps": float(request.form.get("fps", 10)),
            "font_size": int(request.form.get("font_size", 8)),
            "contrast": float(request.form.get("contrast", 1.1)),
            "saturation": float(request.form.get("saturation", 1.1)),
        }
        threading.Thread(target=_run_job, args=(store, job, options), daemon=True).start()
        return jsonify(id=job.id, status_url=url_for("job_status", job_id=job.id))

    @app.get("/api/jobs/<job_id>")
    def job_status(job_id: str):
        job = store.get(job_id)
        if not job:
            return jsonify(error="Render job not found."), 404
        payload = {"id": job.id, "status": job.status, "message": job.message, "progress": job.percent, "error": job.error}
        if job.output_path:
            payload["preview_url"] = url_for("preview", job_id=job.id)
            payload["download_url"] = url_for("download", job_id=job.id)
        return jsonify(payload)

    @app.get("/api/jobs/<job_id>/preview")
    def preview(job_id: str):
        job = store.get(job_id)
        if not job or not job.output_path:
            return "Not ready", 404
        return send_file(job.output_path)

    @app.get("/api/jobs/<job_id>/download")
    def download(job_id: str):
        job = store.get(job_id)
        if not job or not job.output_path:
            return "Not ready", 404
        return send_file(job.output_path, as_attachment=True, download_name=job.output_path.name)

    return app


def _run_job(store: JobStore, job: RenderJob, options: dict[str, int | float]) -> None:
    job.status = "rendering"
    job.message = "Starting renderer"
    extension = ".png" if job.input_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp"} else ".gif"
    output = store.results / f"artify-{job.id}{extension}"
    config = RenderConfig(input_path=job.input_path, output_path=output, **options)

    def update(done: int, total: int, message: str) -> None:
        job.completed, job.total, job.message = done, total, message

    try:
        job.output_path = render_media(config, update)
        job.status, job.message, job.completed, job.total = "complete", "Your character art is ready.", 1, 1
    except Exception as exc:  # Keep errors visible to the local user, not hidden in a worker thread.
        job.status, job.error, job.message = "failed", str(exc), "Rendering could not finish."
