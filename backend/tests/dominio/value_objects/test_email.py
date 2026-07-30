import pytest

from domain.value_objects.email import Email
from shared.exceptions import EmailInvalidoError


def test_deve_criar_email_valido():
    email = Email(" TESTE@EMAIL.COM ")

    assert email.valor == "teste@email.com"


def test_email_invalido():
    with pytest.raises(EmailInvalidoError):
        Email("teste")
