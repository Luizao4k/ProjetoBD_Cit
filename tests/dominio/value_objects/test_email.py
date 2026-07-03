import pytest

from domain.value_objects.email import Email
from shared.exceptions import EmailInvalidoError


def test_deve_criar_email_valido():
    email = Email(" TESTE@EMAIL.COM ")

    assert email.valor == "teste@email.com"


def test_email_invalido():
    with pytest.raises(EmailInvalidoError):
        Email("teste")


def test_criar_retorna_none_para_none():
    assert Email.criar(None) is None


def test_criar_retorna_none_para_vazio():
    assert Email.criar("") is None


def test_criar_retorna_none_para_email_invalido():
    assert Email.criar("abc") is None


def test_criar_retorna_email():
    email = Email.criar("teste@email.com")

    assert isinstance(email, Email)
