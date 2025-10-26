# Echo Server

Simple asyncio-powered TCP echo server project.

## Getting Started

Run the following commands from the `echo_server/` directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # optional; see below for manual install
```

Install development dependencies manually if no lock file is present:

```bash
pip install pytest pytest-asyncio
```

## Running the Server

```bash
python -m echo_server --host 0.0.0.0 --port 9999
```

Connect via `nc localhost 9999` and every message you send will be echoed back verbatim.

## Testing

```bash
pytest
```

This runs asynchronous round-trip tests against the in-memory server.
