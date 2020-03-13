
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)



def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 9


def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 188


def test_forms(cldf_dataset):
    # Yinhawangka-1_black-1,,Yinhawangka,1_black,warru/waru[76],warru,,,Haynie2016,,
    # Yinhawangka-1_black-2,,Yinhawangka,1_black,warru/waru[76],waru,,,Haynie2016,,

    forms = [
        f for f in cldf_dataset["FormTable"] if f["Value"] == "martajarri, pataljali, warrulywarruly"
    ]
    assert len(forms) == 3
    assert set([f["Form"] for f in forms]) == set(["martajarri", "pataljali", "warrulywarruly"])
