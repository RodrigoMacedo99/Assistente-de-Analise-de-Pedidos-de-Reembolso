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

## Política de reembolso

Use `load_policy` para carregar `politica.yaml`. A função usa `yaml.safe_load`,
valida a estrutura com Pydantic e devolve os valores monetários como `Decimal`.
Arquivos inválidos geram `PolicyLoadError` com o caminho e os campos inválidos.
Na aplicação, carregue a política no início e passe o objeto validado aos
componentes que precisarem dela.

Para iniciar a aplicação de validação com o arquivo padrão:

```powershell
uv run ml-skills-reembolso
```

Para validar outro arquivo:

```powershell
uv run ml-skills-reembolso --policy caminho\para\politica.yaml
```

Também é possível iniciar pelo módulo:

```powershell
uv run python -m ml_skills_reembolso
```

```python
from pathlib import Path

from ml_skills_reembolso.policy import load_policy

policy = load_policy(Path("politica.yaml"))
```

## Qualidade de código

```powershell
uv run ruff check .
uv run ruff format --check .
```

As dependências de desenvolvimento ficam no grupo `dev` do `pyproject.toml`.