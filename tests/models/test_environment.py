import numpy as np

from opendrift.models.basemodel.environment import Environment
from opendrift.models.oceandrift import OceanDrift
from opendrift.config import Configurable
from opendrift.readers import reader_constant


def test_add_readers(test_data_roms):
    c = Configurable()
    required_variables = {
        'x_sea_water_velocity': {
            'fallback': 0
        },
        'y_sea_water_velocity': {
            'fallback': 10
        },
    }
    env = Environment(required_variables, c._config)
    env.add_reader(test_data_roms)
    env.finalize()

    e, p, k = env.get_environment(
        ['x_sea_water_velocity', 'y_sea_water_velocity'],
        test_data_roms.start_time, [10], [50], [0], [])
    assert e[0][0] == 0
    assert e[0][1] == 10


def test_profiles_from_second_reader_group_are_not_dropped():
    """A second reader/reader-group's *profile* variable must not be
    silently discarded in favour of its fallback constant.

    Regression test for a bug where env_profiles (the running dict merged
    across reader groups in Environment.get_environment()) was only ever
    initialised from whichever reader group ran first; a later group's new
    profile-variable name was then never a key in that dict, so its data
    was dropped without error or warning.
    """
    c = Configurable()
    required_variables = {
        'x_sea_water_velocity': {
            'fallback': 0,
            'profiles': True
        },
        'y_sea_water_velocity': {
            'fallback': 999,
            'profiles': True
        },
    }
    env = Environment(required_variables, c._config)
    r1 = reader_constant.Reader({'x_sea_water_velocity': 1.23})
    r1.name = 'r1'
    r2 = reader_constant.Reader({'y_sea_water_velocity': 4.56})
    r2.name = 'r2'
    env.add_reader(r1, variables=['x_sea_water_velocity'])
    env.add_reader(r2, variables=['y_sea_water_velocity'])
    env.finalize()

    import datetime
    e, p, k = env.get_environment(
        ['x_sea_water_velocity', 'y_sea_water_velocity'],
        datetime.datetime(2020, 1, 1), np.array([10.0]), np.array([50.0]),
        np.array([-5.0]),
        profiles=['x_sea_water_velocity', 'y_sea_water_velocity'],
        profiles_depth=10)

    assert 'y_sea_water_velocity' in p
    np.testing.assert_allclose(p['y_sea_water_velocity'], 4.56, atol=1e-4)
    np.testing.assert_allclose(e['y_sea_water_velocity'], 4.56, atol=1e-4)


def test_profiles_from_second_reader_group_are_regridded(test_data_roms):
    """When two reader groups' profile variables have different vertical
    grids (e.g. a structured reader's native sigma levels vs. a
    ConstantReader's default 2-point [0, -profiles_depth]), the second
    group's data must be regridded onto the already-established
    env_profiles['z'] axis, not stored (or dropped) under a mismatched
    grid - every profile variable is later indexed against that single
    shared 'z' array by consumers (e.g. PASCAL's
    individual.py::get_profile()).

    This reproduces the "Bigger finding" in a20_test/README.md: pred1dens
    (from a ConstantReader after the main physical reader, exactly this
    two-group shape) has likely been silently reading back its raw
    fallback instead of its configured constant in existing CMEMS/
    HPC-Barents runs.
    """
    c = Configurable()
    required_variables = {
        'sea_water_temperature': {
            'fallback': -999,
            'profiles': True
        },
        'pred1dens': {
            'fallback': 999.0,  # deliberately different from the reader's real value
            'profiles': True
        },
    }
    env = Environment(required_variables, c._config)
    const = reader_constant.Reader({'pred1dens': 0.00001})
    const.name = 'constant_reader'
    env.add_reader(test_data_roms, variables=['sea_water_temperature'])
    env.add_reader(const, variables=['pred1dens'])
    env.finalize()
    env.prepare_readers([10, 65, 20, 70], test_data_roms.start_time,
                        test_data_roms.end_time)

    e, p, k = env.get_environment(
        ['sea_water_temperature', 'pred1dens'],
        test_data_roms.start_time, np.array([12.0, 13.0]),
        np.array([67.0, 68.0]), np.array([-5.0, -20.0]),
        profiles=['sea_water_temperature', 'pred1dens'], profiles_depth=50)

    assert len(p['z']) > 2  # real ROMS sigma levels, not the 2-point default
    assert p['pred1dens'].shape == p['sea_water_temperature'].shape
    # Every level/element should carry the reader's real constant, not the
    # (deliberately different) fallback value.
    np.testing.assert_allclose(p['pred1dens'], 0.00001, atol=1e-9)
    np.testing.assert_allclose(e['pred1dens'], 0.00001, atol=1e-9)
