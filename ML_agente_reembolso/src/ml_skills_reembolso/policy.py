from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Annotated, Self

import yaml
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    ValidationError,
    model_validator,
)


class PolicyLoadError(ValueError):
    """Raised when a policy file cannot be read or does not satisfy its schema."""


def _parse_money(value: object) -> Decimal:
    if not isinstance(value, str):
        raise ValueError("deve ser informado como texto decimal entre aspas")

    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("deve ser um valor decimal válido") from exc

    if not amount.is_finite():
        raise ValueError("deve ser um valor decimal finito")

    return amount


NonEmptyString = Annotated[StrictStr, Field(min_length=1)]
PositiveDays = Annotated[StrictInt, Field(gt=0)]
Money = Annotated[
    Decimal,
    BeforeValidator(_parse_money),
    Field(ge=Decimal("0")),
]


class _PolicyModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ArrependimentoPolicy(_PolicyModel):
    online_dias: PositiveDays
    loja_fisica_dias: PositiveDays
    loja_fisica_exige_embalagem_original: StrictBool


class DefeitoPolicy(_PolicyModel):
    prazo_reparo_dias: PositiveDays


class CategoriaPolicy(_PolicyModel):
    garantia_total_dias: PositiveDays
    teto_aprovacao_automatica: Money


class Policy(_PolicyModel):
    versao: NonEmptyString
    arrependimento: ArrependimentoPolicy
    defeito: DefeitoPolicy
    categorias: dict[StrictStr, CategoriaPolicy] = Field(min_length=1)
    valor_maximo_reembolsavel: Money
    produtos_essenciais: list[NonEmptyString] = Field(min_length=1)
    condicoes_excluidas: list[NonEmptyString] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_category_limits(self) -> Self:
        empty_categories = [name for name in self.categorias if not name.strip()]
        if empty_categories:
            raise ValueError("nomes de categorias não podem estar vazios")

        for name, category in self.categorias.items():
            if category.teto_aprovacao_automatica > self.valor_maximo_reembolsavel:
                raise ValueError(
                    f"categorias.{name}.teto_aprovacao_automatica não pode "
                    "superar valor_maximo_reembolsavel"
                )

        return self


def load_policy(path: Path) -> Policy:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise PolicyLoadError(f"Arquivo de política não encontrado: {path}") from exc
    except OSError as exc:
        raise PolicyLoadError(f"Não foi possível ler a política {path}: {exc}") from exc

    try:
        raw_policy = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise PolicyLoadError(f"YAML inválido em {path}: {exc}") from exc

    try:
        return Policy.model_validate(raw_policy)
    except ValidationError as exc:
        details = []
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"]) or "<raiz>"
            details.append(f"{location}: {error['msg']}")

        raise PolicyLoadError(
            f"Política inválida em {path}: {'; '.join(details)}"
        ) from exc
