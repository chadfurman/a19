import day1
def test_mass_of_12():
    result = day1.run(12)
    assert result == 2

def test_mass_of_14():
    result = day1.run(14)
    assert result == 2

def test_mass_of_1969():
    result = day1.run(1969)
    assert result == 654

def test_mass_of_1969():
    result = day1.run(100756)
    assert result == 33583

def test_no_mass():
    result = day1.run(0)
    assert result == False

def test_negative_mass():
    result = day1.run(-12)
    assert result == False

def test_non_numeric_mass():
    result = day1.run("cat")
    assert result == False

def test_missing_mass():
    result = day1.run()
    assert result == False
