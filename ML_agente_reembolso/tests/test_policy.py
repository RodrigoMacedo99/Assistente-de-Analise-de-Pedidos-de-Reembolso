from decimal import Decimal
from pathlib import Path

import pytest

from ml_skills_reembolso.policy import PolicyLoadError, load_policy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = PROJECT_ROOT / "politica.yaml"


def test_loads_current_policy_with_decimal_amounts():
    policy = load_policy(POLICY_PATH)

    assert policy.versao == "0.1.0"
    assert policy.valor_maximo_reembolsavel == Decimal("15000.00")
    assert policy.categorias["eletronicos"].teto_aprovacao_automatica == Decimal(
        "2500.00"
    )


def test_missing_policy_file_has_clear_error(tmp_path):
    missing_path = tmp_path / "politica.yaml"

    with pytest.raises(PolicyLoadError) as error:
        load_policy(missing_path)

    assert "Arquivo de política não encontrado" in str(error.value)
    assert str(missing_path) in str(error.value)


def test_invalid_yaml_has_clear_error(tmp_path):
    policy_path = tmp_path / "politica.yaml"
    policy_path.write_text("versao: [0.1.0\n", encoding="utf-8")

    with pytest.raises(PolicyLoadError) as error:
        load_policy(policy_path)

    assert "YAML inválido" in str(error.value)
    assert str(policy_path) in str(error.value)


def test_missing_required_field_names_the_field(tmp_path):
    policy_path = tmp_path / "politica.yaml"
    content = POLICY_PATH.read_text(encoding="utf-8")
    content = content.replace('valor_maximo_reembolsavel: "15000.00"\n', "")
    policy_path.write_text(content, encoding="utf-8")

    with pytest.raises(PolicyLoadError) as error:
        load_policy(policy_path)

    assert "valor_maximo_reembolsavel" in str(error.value)


def test_money_must_be_a_quoted_decimal_string(tmp_path):
    policy_path = tmp_path / "politica.yaml"
    content = POLICY_PATH.read_text(encoding="utf-8")
    content = content.replace(
        'teto_aprovacao_automatica: "2500.00"',
        "teto_aprovacao_automatica: 2500.00",
        1,
    )
    policy_path.write_text(content, encoding="utf-8")

    with pytest.raises(PolicyLoadError) as error:
        load_policy(policy_path)

    assert "categorias.eletronicos.teto_aprovacao_automatica" in str(error.value)
    assert "texto decimal entre aspas" in str(error.value)


def test_unknown_policy_field_is_rejected(tmp_path):
    policy_path = tmp_path / "politica.yaml"
    content = POLICY_PATH.read_text(encoding="utf-8")
    policy_path.write_text(
        f"{content}campo_desconhecido: true\n",
        encoding="utf-8",
    )

    with pytest.raises(PolicyLoadError) as error:
        load_policy(policy_path)

    assert "campo_desconhecido" in str(error.value)


def test_category_auto_approval_limit_cannot_exceed_global_limit(tmp_path):
    policy_path = tmp_path / "politica.yaml"
    content = POLICY_PATH.read_text(encoding="utf-8")
    content = content.replace(
        'teto_aprovacao_automatica: "2500.00"',
        'teto_aprovacao_automatica: "15000.01"',
        1,
    )
    policy_path.write_text(content, encoding="utf-8")

    with pytest.raises(PolicyLoadError) as error:
        load_policy(policy_path)

    assert "categorias.eletronicos.teto_aprovacao_automatica" in str(error.value)
