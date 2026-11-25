from pathlib import Path

import ml_skills_reembolso


def test_package_is_importable_from_src_layout():
    assert Path(ml_skills_reembolso.__file__).is_file()
