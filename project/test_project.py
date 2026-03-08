import pytest
from project import validate_day, validate_time, validate_id

def test_validatetime():
    assert validate_time("1430") == True
    assert validate_time("mon") == False

def test_validateid():
    assert validate_id("16") == True
    with pytest.raises(SystemExit):
        validate_id("dog")

def test_validateday():
    assert validate_day("mon") == True
    assert validate_day("1700") == False
