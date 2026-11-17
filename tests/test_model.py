from model import simulate


def test_mars_circular_orbit_is_stable():
    result = simulate(duration=120)
    assert result["status"] == "COMPLETED"
    assert result["checks"]["energy_passed"]
    assert abs(result["summary"]["Final altitude (km)"] - 400) < 0.01


def test_invalid_altitude_is_rejected():
    try:
        simulate(altitude=0)
    except ValueError:
        return
    raise AssertionError("Expected ValueError")
