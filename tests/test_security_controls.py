import pytest

from rewt_public.security.control_plane import ControlPlaneStore, FileBackedSecurityPort
from rewt_public.security.port import KillSwitch, SecurityViolation


def test_internet_stop_fails_closed(tmp_path):
    state = tmp_path / "control" / "state.json"
    control = ControlPlaneStore(state, require_authorization=False)
    control.engage(KillSwitch.INTERNET_STOP)

    with pytest.raises(SecurityViolation) as error:
        FileBackedSecurityPort(state).assert_internet_allowed()

    assert error.value.control is KillSwitch.INTERNET_STOP
