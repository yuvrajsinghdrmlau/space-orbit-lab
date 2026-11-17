# Space Orbit Lab

A focused Python/Streamlit project for simulating an ideal two-body orbit around Earth or Mars. It is the space module extracted from Virtual Universe Lab so it can evolve independently.

## Live application

**[Launch Space Orbit Lab](https://space-orbit-lab.streamlit.app/)**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://space-orbit-lab.streamlit.app/)

The hosted application is deployed from `main` on Streamlit Community Cloud. New commits to that branch are deployed automatically.

## What it does

- Integrates a three-dimensional orbit with SciPy's DOP853 solver.
- Supports Earth and Mars reference constants.
- Accepts altitude, duration, inclination, and a circular-speed multiplier.
- Stops if the trajectory contacts the body's surface.
- Reports energy and angular-momentum drift as numerical checks.
- Provides a browser UI and a JSON-producing CLI.

## Quick start

Python 3.12 is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On macOS/Linux, use `.venv/bin/python` in place of `.venv\Scripts\python.exe`.

## Command line

```powershell
.\.venv\Scripts\python.exe cli.py --body Mars --altitude 400 --duration 120 --inclination 35
```

The CLI writes the complete result, checks, time-series channels, and metadata as JSON.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

## Streamlit Community Cloud deployment

The repository includes pinned runtime dependencies and a production Streamlit theme. Create the app in [Streamlit Community Cloud](https://share.streamlit.io/) with:

| Setting | Value |
|---|---|
| Repository | `yuvrajsinghdrmlau/space-orbit-lab` |
| Branch | `main` |
| Entrypoint | `app.py` |
| Python | `3.12` |

No secrets or environment variables are required. Because the GitHub repository is private, the Streamlit account must be authorized to access private repositories. Every later push to `main` will trigger an automatic app update.

## Project layout

```text
app.py              Streamlit interface and charts
cli.py              Command-line interface
model.py            Numerical model and validation
requirements.txt    Cloud/runtime dependencies
requirements-dev.txt Test-only dependencies
.streamlit/config.toml Hosted app theme and server settings
tests/test_model.py Core regression tests
```

## Model scope

This is a point-mass, planet-centered inertial model. It excludes thrust, atmosphere, oblateness, third bodies, relativistic effects, and real ephemerides. The visualization is explanatory, not mission-design evidence. Passing numerical checks only shows that this implementation preserves the declared two-body invariants within tolerance.

## Good next improvements

- Add ephemeris-based initial conditions and additional forces.
- Add typed scenario files and result exports.
- Add independent benchmark cases and model-version metadata.
- Add CI for Windows, Linux, and macOS.

## License

No license has been selected yet. Add one before accepting external contributions or reuse.
