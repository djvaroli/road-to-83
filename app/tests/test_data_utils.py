from app.data_utils import clean_and_split_string


def test_clean_and_split_string():
    test_string = "Weight 92.0"
    r = clean_and_split_string(test_string)

    assert len(r) == 2, "Length is not 2."
    assert r[0] == "weight", f"The first entry should be 'weight' is {test_string[0]}"
    assert r[1] == "92.0", f"The first entry should be '92.0' is {test_string[1]}"
