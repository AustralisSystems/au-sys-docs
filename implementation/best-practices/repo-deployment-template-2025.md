# Repo Template: Deployment, Git & CI (Copy‑Ready) — 2025

**Version:** 1.0.0  •  **Last Updated:** 2026-01-03

Use this page as a *drop-in template* and checklist when creating new repositories that should follow the project's deployment, Git, CI, and supply-chain best practices.

---

## What this template contains 📦
- Minimal, copy-ready: `Dockerfile`, `Makefile`, `.env.example`, `README` snippets
- GitHub workflow stubs: `build-and-push-container.yml`, `cd-verify-and-deploy.yml`
- Checklist and quick commands to validate the repo locally

> Tip: Copy snippets into the new repo and tailor names (container registry, image name, secrets) as noted below.

---

## 1) Dockerfile (builder → runtime, wheelhouse) 🔧

Use BuildKit and split builder/runtime so build tools do not end up in the final image.

```dockerfile
# syntax=docker/dockerfile:1.7

# ---- Builder: build wheels ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.lock.txt requirements.txt /build/
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip setuptools wheel pip-tools && \
    python -m pip wheel --wheel-dir=/wheels -r requirements.lock.txt

# ---- Runtime ----
FROM python:3.12-slim
ARG SKIP_MEDIA_PACKAGES=false
ENV SKIP_MEDIA_PACKAGES=${SKIP_MEDIA_PACKAGES}
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

# Copy runtime files + install wheels
COPY --from=builder /wheels /wheels
COPY requirements.lock.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-index --find-links /wheels -r requirements.lock.txt

# App files
COPY . /app
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
CMD ["gunicorn", "main:app", "-c", "gunicorn_config.py"]
```

Notes:
- If a third-party installer must be run (e.g., Azure CLI), require a build-arg with a checksum and verify it before executing. Avoid `curl | sh` patterns.
- Consider pinning the production base image with a digest when moving to production (replace the tag with `@sha256:...`).

---

## 2) Makefile (deps & regeneration) 🧾

```makefile
.PHONY: lock-deps regen-pins

lock-deps:
	python -m pip install --upgrade pip pip-tools
	python -m piptools.scripts.compile --generate-hashes --upgrade --output-file=requirements.lock.txt requirements.in

regen-pins: lock-deps
	git add requirements.lock.txt && git commit -m "chore: regen pins" || true
```

---

## 3) .env.example (minimal) 🌐

```
# Application
MODE=sandbox
PORT=8000
# Secrets - never commit production values
REDIS_PASSWORD=changeme
LLM_PROVIDER=openai
# Azure/Registry placeholders
AZURE_CONTAINER_REGISTRY=youracr.azurecr.io
```

---

## 4) GitHub Actions: build-and-push-container.yml (stub) ⚙️

A minimal CI that builds, produces wheelhouse, SBOM, optional signing, and scans:

```yaml
name: Build and Push Container
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Static policy check
        run: grep -nE 'curl .*\|.*sh' Dockerfile || true

      - name: Build wheelhouse
        run: |
          python -m pip install pip wheel
          python -m pip download --dest wheels -r requirements.lock.txt || true
      - name: Upload wheelhouse
        uses: actions/upload-artifact@v4
        with: name: wheelhouse-${{ github.sha }}
              path: wheels

      - name: Build & push image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.REGISTRY }}/app:${{ github.sha }}

      - name: Generate SBOM
        run: docker run --rm -v /var/run/docker.sock:/var/run/docker.sock anchore/syft:latest ${{ secrets.REGISTRY }}/app:${{ github.sha }} -o spdx-json > sbom.json

      - name: Optional: Sign image (cosign)
        if: ${{ secrets.COSIGN_PRIVATE_KEY != '' }}
        run: |
          echo "${{ secrets.COSIGN_PRIVATE_KEY }}" | base64 --decode > cosign.key
          cosign sign --key cosign.key ${{ secrets.REGISTRY }}/app:${{ github.sha }}

      - name: Scan image (Trivy)
        uses: aquasecurity/trivy-action@master
        with: image-ref: ${{ secrets.REGISTRY }}/app:${{ github.sha }}
```

Replace `secrets.REGISTRY` with your registry secret (e.g., `ghcr.io/org`). Add more steps as needed (SARIF uploads, pip-audit, artifact retention).

---

## 5) GitHub Actions: cd-verify-and-deploy.yml (stub) 🔒

```yaml
name: CD - Verify & Deploy
on: push:
  tags: ['v*.*.*']
jobs:
  verify-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Verify image signature
        if: ${{ secrets.COSIGN_PUBKEY != '' }}
        run: cosign verify --key ${{ secrets.COSIGN_PUBKEY }} ${{ secrets.REGISTRY }}/app:${{ github.ref_name }}

      - name: Deploy to infra
        run: ./deploy/deploy.sh --image ${{ secrets.REGISTRY }}/app:${{ github.ref_name }}
```

Notes: Replace deploy step with your platform-specific logic (k8s helm, az webapp, VM scripts).

---

## 6) How to instantiate in a new repo (quick instructions) 🚀
1. Copy these files into the target repo: `Dockerfile`, `Makefile`, `.env.example`, and the two workflows under `.github/workflows/`.
2. Add `requirements.in` and run `make lock-deps` to generate `requirements.lock.txt`.
3. Add GitHub secrets: `REGISTRY` (host), `REGISTRY_USERNAME`, `REGISTRY_PASSWORD`, optional `COSIGN_PRIVATE_KEY`, `COSIGN_PASSWORD`, and `COSIGN_PUBKEY` (for verification).
4. Adjust workflow tags and deployment commands to your infra.
5. Confirm CI runs: wheelhouse artifact present, sbom.json uploaded, trivy passes.

---

## 7) Quick validation commands (local) 🧪
- Build: `DOCKER_BUILDKIT=1 docker build --progress=plain -t app-local .`
- Wheelhouse: `python -m pip download --dest wheels -r requirements.lock.txt`
- SBOM: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock anchore/syft:latest app-local -o spdx-json > sbom.json`
- Scan: `trivy image --severity CRITICAL,HIGH app-local`

---

## 8) Checklist before production ✓
- [ ] `requirements.lock.txt` generated with hashes
- [ ] CI produces wheelhouse, SBOM, and scans pass
- [ ] Signing keys managed in secrets and verification configured in CD
- [ ] No `curl | sh` pattern left unchecked in Dockerfile
- [ ] `.env.example` present and `.env` not committed

---

If you want, I can also produce a ready-to-commit directory (`/repo-template`) with these exact files so you can copy it into new repos; say so and I’ll create the files under `scaffolds/`.
