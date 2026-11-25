# ML Skills Reembolso

Base limpa para projetos de machine learning e agentes de IA, gerenciada com
UV e Python 3.12+.

## Ambiente

```powershell
uv sync
```

## Testes

```powershell
uv run pytest
```

Os testes ficam em `tests/`. O pytest está configurado para descobrir arquivos
com o padrão `test_*.py`.

## Qualidade de código

```powershell
uv run ruff check .
uv run ruff format --check .
```

As dependências de desenvolvimento ficam no grupo `dev` do `pyproject.toml`.