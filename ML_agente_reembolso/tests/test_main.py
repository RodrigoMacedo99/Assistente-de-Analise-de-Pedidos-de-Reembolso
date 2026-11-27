from ml_skills_reembolso.main import DEFAULT_POLICY_PATH, main


def test_main_loads_default_policy(capsys):
    result = main([])

    captured = capsys.readouterr()
    assert result == 0
    assert f"Política válida: {DEFAULT_POLICY_PATH}" in captured.out
    assert "Versão: 0.1.0" in captured.out
    assert "Categorias carregadas: 3" in captured.out
    assert captured.err == ""


def test_main_returns_error_for_invalid_policy(tmp_path, capsys):
    invalid_policy = tmp_path / "politica.yaml"
    invalid_policy.write_text("versao: [invalido\n", encoding="utf-8")

    result = main(["--policy", str(invalid_policy)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Erro ao validar a política" in captured.err
    assert str(invalid_policy) in captured.err
    assert captured.out == ""
