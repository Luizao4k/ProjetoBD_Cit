"""
Conversores puros de tipo primitivo: str (o que qualquer Reader
entrega) para int, bool, date etc.

A regra que separa isso dos Value Objects: um conversor não sabe NADA
sobre a entidade. `para_inteiro_opcional("5")` devolve 5 pra
"quantidade de chromebooks" ou pra "ano de fundação" exatamente da
mesma forma — ele não sabe que quantidade tem que ser positiva, isso é
`Quantidade.__post_init__`. Se essa regra migrasse pra cá, o mesmo
conhecimento de negócio passaria a existir em dois lugares (o
Conversor E o Value Object), e um dia os dois divergem.
"""

from __future__ import annotations

from datetime import date, datetime


def para_texto_opcional(valor: str | None) -> str | None:
    """Vazio (ou só espaços) vira None; senão, devolve com espaços
    nas pontas removidos."""
    valor = (valor or "").strip()
    return valor or None


def para_inteiro_opcional(valor: str | None) -> int | None:
    """None/"" vira None. Qualquer outra coisa que não seja um
    inteiro válido levanta ValueError (deixado propagar de propósito
    — o Pipeline captura e registra como falha da linha)."""
    valor = (valor or "").strip()
    return int(valor) if valor else None


def para_inteiro(valor: str) -> int:
    """Versão obrigatória: KeyError/ValueError sobem se a coluna
    faltar ou não for um inteiro."""
    return int(valor.strip())


def para_booleano(
    valor: str | None,
    *,
    verdadeiros: frozenset[str] = frozenset({"1", "true", "verdadeiro", "sim", "s", "yes"}),
) -> bool:
    """Qualquer valor fora do conjunto reconhecido como verdadeiro
    conta como False — não levanta erro, porque "booleano" não tem
    conceito natural de 'formato inválido' (tudo que não é
    reconhecidamente verdadeiro é, por definição, falso)."""
    return (valor or "").strip().lower() in verdadeiros


def para_data_opcional(valor: str | None, formato: str = "%Y-%m-%d") -> date | None:
    """None/"" vira None. Formato errado levanta ValueError, deixado
    propagar."""
    valor = (valor or "").strip()
    return datetime.strptime(valor, formato).date() if valor else None
