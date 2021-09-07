import pytest
from src.finding import Finding, WrongFindingInputError


def test_finding_creation():
    finding = Finding(100.0, 50.0, ["Tag1", "Tag2"], "image_hash")
    assert finding.longitude == 100.0
    assert finding.latitude == 50.0
    assert ["Tag1", "Tag2"] == finding.tags
    assert finding.image_hash == "image_hash"


def test_wrong_input():
    with pytest.raises(WrongFindingInputError):
        finding = Finding(200.0, 50.0, ["Tag1", "Tag2"], "image_hash")

    with pytest.raises(WrongFindingInputError):
        finding = Finding(100, -100.0, ["Tag1", "Tag2"], "image_hash")

    with pytest.raises(WrongFindingInputError):
        finding = Finding(100, 50, [], "image_hash")


def test_change_property():
    with pytest.raises(AttributeError):
        finding = Finding(100.0, 50.0, ["Tag1", "Tag2"], "image_hash")
        finding.longitude = 50

    with pytest.raises(AttributeError):
        finding = Finding(100.0, 50.0, ["Tag1", "Tag2"], "image_hash")
        finding.latitude = 60

    with pytest.raises(AttributeError):
        finding = Finding(100.0, 50.0, ["Tag1", "Tag2"], "image_hash")
        finding.tags = ["Tag3"]


def test_finding_to_dict():
    finding = Finding(100.0, 50.0, ["Tag1", "Tag2"], "image_hash")
    expected_dict = {
        "longitude": 100.0,
        "latitude": 50.0,
        "tags": ["Tag1", "Tag2"],
        "image_hash": "image_hash"
    }
    assert finding.to_dict() == expected_dict


def test_finding_creation_from_dict():
    finding = Finding.create_from_json({
        "longitude": 100.0,
        "latitude": 50.0,
        "tags": ["Tag1", "Tag2"],
        "image_hash": "image_hash"
    })

    finding = Finding.create_from_json({
        "longitude": 100.0,
        "latitude": 50.0,
        "tags": ["Tag1", "Tag2"]
    })
