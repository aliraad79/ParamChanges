import json
import sys
from pathlib import Path

PROJECTION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECTION_DIR))

from calculations.SimulationClass import SimulationClass
from calculations.config import default_config

SNAPSHOT_PATH = Path(__file__).resolve().parent / "snapshot_default_config.json"


def test_default_config_matches_snapshot():
    sim = SimulationClass()
    sim.run()
    actual = sim.json_report()
    expected = json.loads(SNAPSHOT_PATH.read_text())
    assert actual == expected, (
        "Simulation output drifted from snapshot. If intentional, regenerate "
        f"with: python -c \"...\" > {SNAPSHOT_PATH.name}"
    )


def test_simulation_is_deterministic():
    a = SimulationClass()
    a.run()
    b = SimulationClass()
    b.run()
    assert a.json_report() == b.json_report()


def test_report_has_one_entry_per_simulated_year():
    sim = SimulationClass()
    sim.run()
    report = sim.json_report()
    assert len(report) == default_config["SIMULATION_YEARS"]
    years = [r["year"] for r in report]
    assert years == list(range(1400, 1400 + default_config["SIMULATION_YEARS"]))


def test_populations_remain_non_negative():
    sim = SimulationClass()
    sim.run()
    for entry in sim.json_report():
        for key in (
            "bazneshasteh_alive_population",
            "azkaroftadeh_alive_population",
            "survivor_alive_population",
            "insured_alive_population",
            "all_population",
        ):
            assert entry[key] >= 0, f"{key} negative in year {entry['year']}: {entry[key]}"
