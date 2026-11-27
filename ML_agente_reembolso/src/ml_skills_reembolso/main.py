import argparse
import sys
from pathlib import Path
from typing import Sequence

from ml_skills_reembolso.policy import PolicyLoadError, load_policy

DEFAULT_POLICY_PATH = Path(__file__).resolve().parents[2] / "politica.yaml"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Carrega e valida a política de reembolso."
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=DEFAULT_POLICY_PATH,
        help="caminho do arquivo YAML da política",
    )
    args = parser.parse_args(argv)

    try:
        policy = load_policy(args.policy)
    except PolicyLoadError as exc:
        print(f"Erro ao validar a política: {exc}", file=sys.stderr)
        return 1

    print(f"Política válida: {args.policy}")
    print(f"Versão: {policy.versao}")
    print(f"Categorias carregadas: {len(policy.categorias)}")
    print(f"Valor máximo reembolsável: R$ {policy.valor_maximo_reembolsavel:.2f}")
    return 0
