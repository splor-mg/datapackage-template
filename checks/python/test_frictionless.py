def test_package(package):
    report = package.validate()
    assert report.valid
