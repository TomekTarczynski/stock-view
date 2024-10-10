import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from sum import mysum


def test__sum():
    result = mysum(1, 2)
    assert result == 3
