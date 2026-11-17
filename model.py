"""Bounded two-body orbit model used by the UI and CLI."""

import numpy as np
from scipy.integrate import solve_ivp

PLANETS = {
    "Earth": {"mu": 398600.435507, "radius": 6378.137},
    "Mars": {"mu": 42828.375214, "radius": 3396.19},
}


def simulate(body="Mars", altitude=400.0, duration=120.0, inclination=35.0, speed_factor=1.0):
    if body not in PLANETS:
        raise ValueError(f"Unsupported body: {body}")
    if altitude <= 0 or duration <= 0 or not 0 <= inclination <= 180 or speed_factor <= 0:
        raise ValueError("Use positive altitude/duration/speed and inclination from 0 to 180 degrees.")

    mu, radius = PLANETS[body]["mu"], PLANETS[body]["radius"]
    r0 = radius + altitude
    speed = np.sqrt(mu / r0) * speed_factor
    inc = np.deg2rad(inclination)
    initial = np.array([r0, 0, 0, 0, speed * np.cos(inc), speed * np.sin(inc)])
    duration_s = duration * 60
    period = 2 * np.pi * np.sqrt(r0**3 / mu)

    def rhs(_time, state):
        position = state[:3]
        return np.r_[state[3:], -mu * position / np.linalg.norm(position) ** 3]

    def impact(_time, state):
        return np.linalg.norm(state[:3]) - radius

    impact.terminal = True
    impact.direction = -1
    solution = solve_ivp(
        rhs,
        (0, duration_s),
        initial,
        method="DOP853",
        rtol=1e-10,
        atol=1e-10,
        events=impact,
        dense_output=True,
        max_step=min(period / 100, duration_s / 100),
    )
    if not solution.success:
        raise RuntimeError("Orbit integration failed: " + solution.message)

    time = np.unique(np.r_[solution.t, np.linspace(0, solution.t[-1], 600)])
    state = solution.sol(time).T
    radius_series = np.linalg.norm(state[:, :3], axis=1)
    velocity = np.linalg.norm(state[:, 3:], axis=1)
    energy = velocity**2 / 2 - mu / radius_series
    angular_momentum = np.cross(state[:, :3], state[:, 3:])
    energy_error = np.abs(energy - energy[0]) / (mu / r0)
    momentum_error = np.linalg.norm(angular_momentum - angular_momentum[0], axis=1) / max(
        np.linalg.norm(angular_momentum[0]), 1e-12
    )
    valid = bool(
        energy_error.max() < 1e-6
        and momentum_error.max() < 1e-6
        and np.all(np.isfinite(state))
    )
    hit_surface = bool(len(solution.t_events[0]))
    return {
        "status": ("SURFACE_CONTACT" if hit_surface else "COMPLETED") if valid else "FAILED_VALIDATION",
        "summary": {
            "Final altitude (km)": float(radius_series[-1] - radius),
            "Final speed (km/s)": float(velocity[-1]),
            "Simulated time (min)": float(time[-1] / 60),
            "Energy relative error": float(energy_error.max()),
        },
        "checks": {
            "energy_passed": bool(energy_error.max() < 1e-6),
            "angular_momentum_passed": bool(momentum_error.max() < 1e-6),
            "finite_states_passed": bool(np.all(np.isfinite(state))),
        },
        "channels": {
            "time_min": (time / 60).tolist(),
            "x_km": state[:, 0].tolist(),
            "y_km": state[:, 1].tolist(),
            "z_km": state[:, 2].tolist(),
            "altitude_km": (radius_series - radius).tolist(),
            "speed_km_s": velocity.tolist(),
        },
        "meta": {"body": body, "radius_km": radius, "reference_frame": "planet-centered inertial"},
    }
