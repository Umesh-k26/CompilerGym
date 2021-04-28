# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Unit tests for //compiler_gym:compiler_env_state."""
import pytest
from pydantic import ValidationError as PydanticValidationError

from compiler_gym import CompilerEnvState
from tests.test_main import main


def test_state_from_dict_empty():
    with pytest.raises(PydanticValidationError):
        CompilerEnvState(**{})


def test_state_invalid_benchmark_uri():
    with pytest.raises(PydanticValidationError, match="benchmark"):
        CompilerEnvState(benchmark="invalid", walltime=100, reward=1.5, commandline="")


def test_state_invalid_walltime():
    with pytest.raises(PydanticValidationError, match="Walltime cannot be negative"):
        CompilerEnvState(
            benchmark="benchmark://cbench-v0/foo",
            walltime=-1,
            reward=1.5,
            commandline="",
        )


def test_state_to_csv_from_csv():
    original_state = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo",
        walltime=100,
        reward=1.5,
        commandline="-a -b -c",
    )
    state_from_csv = CompilerEnvState.from_csv(original_state.to_csv())

    assert state_from_csv.benchmark == "benchmark://cbench-v0/foo"
    assert state_from_csv.walltime == 100
    assert state_from_csv.reward == 1.5
    assert state_from_csv.commandline == "-a -b -c"


def test_state_to_csv_from_csv_no_reward():
    original_state = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=100, commandline="-a -b -c"
    )
    state_from_csv = CompilerEnvState.from_csv(original_state.to_csv())

    assert state_from_csv.benchmark == "benchmark://cbench-v0/foo"
    assert state_from_csv.walltime == 100
    assert state_from_csv.reward is None
    assert state_from_csv.commandline == "-a -b -c"


def test_state_from_csv_empty():
    with pytest.raises(ValueError) as ctx:
        CompilerEnvState.from_csv("")

    assert str(ctx.value) == "Failed to parse input: ``"


def test_state_from_csv_invalid_format():
    with pytest.raises(ValueError) as ctx:
        CompilerEnvState.from_csv("abcdef")

    assert str(ctx.value).startswith("Failed to parse input: `abcdef`: ")


def test_state_to_json_from_dict():
    original_state = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo",
        walltime=100,
        reward=1.5,
        commandline="-a -b -c",
    )
    state_from_dict = CompilerEnvState(**original_state.dict())

    assert state_from_dict.benchmark == "benchmark://cbench-v0/foo"
    assert state_from_dict.walltime == 100
    assert state_from_dict.reward == 1.5
    assert state_from_dict.commandline == "-a -b -c"


def test_state_to_json_from_dict_no_reward():
    original_state = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=100, commandline="-a -b -c"
    )
    state_from_dict = CompilerEnvState(**original_state.dict())

    assert state_from_dict.benchmark == "benchmark://cbench-v0/foo"
    assert state_from_dict.walltime == 100
    assert state_from_dict.reward is None
    assert state_from_dict.commandline == "-a -b -c"


def test_state_equality_different_types():
    state = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=10, commandline="-a -b -c"
    )
    assert not state == 5  # noqa testing __eq__
    assert state != 5  # testing __ne__


def test_state_equality_same():
    a = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=10, commandline="-a -b -c"
    )
    b = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=10, commandline="-a -b -c"
    )
    assert a == b  # testing __eq__
    assert not a != b  # noqa testing __ne__


def test_state_equality_differnt_walltime():
    """Test that walltime is not compared."""
    a = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=10, commandline="-a -b -c"
    )
    b = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=5, commandline="-a -b -c"
    )
    assert a == b  # testing __eq__
    assert not a != b  # noqa testing __ne__


def test_state_equality_one_sided_reward():
    a = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo",
        walltime=5,
        commandline="-a -b -c",
        reward=2,
    )
    b = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo", walltime=5, commandline="-a -b -c"
    )
    assert a == b  # testing __eq__
    assert b == a  # testing __eq__
    assert not a != b  # noqa testing __ne__
    assert not b != a  # noqa testing __ne__


def test_state_equality_equal_reward():
    a = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo",
        walltime=5,
        commandline="-a -b -c",
        reward=2,
    )
    b = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo",
        walltime=5,
        commandline="-a -b -c",
        reward=2,
    )
    assert a == b  # testing __eq__
    assert b == a  # testing __eq__
    assert not a != b  # noqa testing __ne__
    assert not b != a  # noqa testing __ne__


def test_state_equality_unequal_reward():
    a = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo",
        walltime=5,
        commandline="-a -b -c",
        reward=2,
    )
    b = CompilerEnvState(
        benchmark="benchmark://cbench-v0/foo",
        walltime=5,
        commandline="-a -b -c",
        reward=3,
    )
    assert not a == b  # noqa testing __eq__
    assert not b == a  # noqatesting __eq__
    assert a != b  # testing __ne__
    assert b != a  # testing __ne__


if __name__ == "__main__":
    main()
