import pytest
from mongoke.support import download_file

@pytest.mark.skip
def test_dowload_config_from_github():
    x = download_file('https://raw.githubusercontent.com/remorses/mongoke/master/tests/confs/spec_conf.yaml')
    print(x)
    assert x