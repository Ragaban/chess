from main import is_valid_coord

def test_valid_coord():
    # Valid coordinates should return True
    assert is_valid_coord('A1') is True
    assert is_valid_coord('H8') is True
    assert is_valid_coord('C5') is True

def test_invalid_coord():
    # Invalid coordinates should return False
    assert is_valid_coord('') is False
    assert is_valid_coord('A') is False
    assert is_valid_coord('1') is False
    assert is_valid_coord('I4') is False
    assert is_valid_coord('A9') is False
    assert is_valid_coord('B0') is False
    assert is_valid_coord('C11') is False
    assert is_valid_coord('AB') is False
    assert is_valid_coord('12') is False

def test_coord_with_invalid_characters():
    # Coordinates with invalid characters should return False
    assert is_valid_coord('A@') is False
    assert is_valid_coord('B#') is False
    assert is_valid_coord('%1') is False
    assert is_valid_coord('^8') is False
    assert is_valid_coord('&4') is False