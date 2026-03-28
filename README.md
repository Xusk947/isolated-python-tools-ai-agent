# isolated-python-tools-ai-agent

Container image used by Croki `python_executor` to run Python code in an isolated sandbox and report generated artifacts.

## What This Image Contains

- A small Python sandbox server listening on a Unix socket.
- Automatic artifact hooks:
  - `matplotlib.pyplot.show()` saves PNG files into `/workspace`
  - `PIL.Image.Image.show()` saves PNG files into `/workspace`
  - `plotly` `Figure.show()` saves an HTML file into `/workspace`

## Build and Publish (GitHub Actions)

This repository is intended to be published to GitHub Container Registry (GHCR) via Actions.
See `.github/workflows/docker-publish.yml`.

## Using from Croki

Set the sandbox image name used by the tools service:

- `PYTHON_SANDBOX_IMAGE=ghcr.io/xusk947/isolated-python-tools-ai-agent:latest`

or directly:

- `CROKI_PYEXEC_SANDBOX_IMAGE=ghcr.io/xusk947/isolated-python-tools-ai-agent:latest`

Then restart the `tool-service`.
