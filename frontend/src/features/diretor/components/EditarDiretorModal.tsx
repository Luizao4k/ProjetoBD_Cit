import { useEffect, useState } from "react";
import { Save, X } from "lucide-react";

import {
  atualizarDiretor,
  type Diretor,
} from "../services/diretorService";

interface EditarDiretorModalProps {
  diretor: Diretor;
  onClose: () => void;
  onSuccess: (diretorAtualizado: Diretor) => void;
}

/**
 * Modal responsável pela edição dos dados de um diretor.
 */
export function EditarDiretorModal({
  diretor,
  onClose,
  onSuccess,
}: EditarDiretorModalProps) {
  const [nome, setNome] = useState(diretor.nome);
  const [telefone, setTelefone] = useState(
    diretor.telefone ?? "",
  );
  const [email, setEmail] = useState(
    diretor.email ?? "",
  );

  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(
    null,
  );

  useEffect(() => {
    setNome(diretor.nome);
    setTelefone(diretor.telefone ?? "");
    setEmail(diretor.email ?? "");
    setErro(null);
  }, [diretor]);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const nomeNormalizado = nome.trim();
    const telefoneNormalizado = telefone.trim();
    const emailNormalizado = email.trim();

    if (!nomeNormalizado) {
      setErro("O nome do diretor é obrigatório.");
      return;
    }

    try {
      setSalvando(true);
      setErro(null);

      const diretorAtualizado =
        await atualizarDiretor(
          diretor.id,
          {
            nome: nomeNormalizado,
            telefone:
              telefoneNormalizado || undefined,
            email:
              emailNormalizado || undefined,
          },
        );

      onSuccess(diretorAtualizado);
    } catch (error) {
      console.error(
        "Erro ao atualizar diretor:",
        error,
      );

      setErro(
        "Não foi possível atualizar o diretor.",
      );
    } finally {
      setSalvando(false);
    }
  }

  return (
    <div
      className="escola-modal__overlay"
      onClick={onClose}
    >
      <div
        className="escola-modal"
        onClick={(event) =>
          event.stopPropagation()
        }
      >
        <header className="escola-modal__header">
          <div>
            <h2>Editar diretor</h2>

            <p>
              Atualize os dados do diretor da escola.
            </p>
          </div>

          <button
            type="button"
            className="escola-modal__close"
            onClick={onClose}
            disabled={salvando}
            aria-label="Fechar"
          >
            <X size={20} />
          </button>
        </header>

        <form
          className="escola-modal__form"
          onSubmit={handleSubmit}
        >
          <div className="escola-modal__field">
            <label htmlFor="diretor-nome">
              Nome
            </label>

            <input
              id="diretor-nome"
              type="text"
              value={nome}
              onChange={(event) =>
                setNome(event.target.value)
              }
              disabled={salvando}
              autoFocus
            />
          </div>

          <div className="escola-modal__field">
            <label htmlFor="diretor-telefone">
              Telefone
            </label>

            <input
              id="diretor-telefone"
              type="text"
              value={telefone}
              onChange={(event) =>
                setTelefone(event.target.value)
              }
              placeholder="Informe o telefone"
              disabled={salvando}
            />
          </div>

          <div className="escola-modal__field">
            <label htmlFor="diretor-email">
              E-mail
            </label>

            <input
              id="diretor-email"
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="Informe o e-mail"
              disabled={salvando}
            />
          </div>

          {erro && (
            <div className="escola-modal__error">
              {erro}
            </div>
          )}

          <footer className="escola-modal__footer">
            <button
              type="button"
              className="escola-modal__cancel"
              onClick={onClose}
              disabled={salvando}
            >
              Cancelar
            </button>

            <button
              type="submit"
              className="escola-modal__save"
              disabled={salvando}
            >
              <Save size={17} />

              {salvando
                ? "Salvando..."
                : "Salvar"}
            </button>
          </footer>
        </form>
      </div>
    </div>
  );
}
