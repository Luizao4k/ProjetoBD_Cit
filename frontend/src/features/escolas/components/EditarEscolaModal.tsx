import { useEffect, useState } from "react";
import { Save, X } from "lucide-react";

import { atualizarEscola } from "../services/escolaService";
import type { Escola } from "../types/escola";

interface EditarEscolaModalProps {
  escola: Escola;
  onClose: () => void;
  onSuccess: (escolaAtualizada: Escola) => void;
}

/**
 * Modal responsável pela edição dos dados de uma escola.
 *
 * Atualmente permite alterar somente o nome e o endereço.
 */
export function EditarEscolaModal({
  escola,
  onClose,
  onSuccess,
}: EditarEscolaModalProps) {
  const [nome, setNome] = useState(escola.nome);
  const [endereco, setEndereco] = useState(
    escola.endereco ?? "",
  );

  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  /**
   * Sincroniza os campos caso a escola recebida pelo
   * componente seja alterada.
   */
  useEffect(() => {
    setNome(escola.nome);
    setEndereco(escola.endereco ?? "");
    setErro(null);
  }, [escola]);

  /**
   * Salva as alterações da escola.
   */
  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const nomeNormalizado = nome.trim();
    const enderecoNormalizado = endereco.trim();

    if (!nomeNormalizado) {
      setErro("O nome da escola é obrigatório.");
      return;
    }

    try {
      setSalvando(true);
      setErro(null);

      const escolaAtualizada = await atualizarEscola(
        escola.id,
        {
          nome: nomeNormalizado,
          endereco: enderecoNormalizado,
        },
      );

      onSuccess(escolaAtualizada);
    } catch (error) {
      console.error(
        "Erro ao atualizar escola:",
        error,
      );

      setErro(
        "Não foi possível atualizar a escola.",
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
            <h2>Editar escola</h2>

            <p>
              Atualize os dados cadastrais da escola.
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
            <label htmlFor="escola-inep">
              INEP
            </label>

            <input
              id="escola-inep"
              type="text"
              value={escola.inep}
              disabled
            />
          </div>

          <div className="escola-modal__field">
            <label htmlFor="escola-nome">
              Nome
            </label>

            <input
              id="escola-nome"
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
            <label htmlFor="escola-tipo">
              Tipo
            </label>

            <input
              id="escola-tipo"
              type="text"
              value={escola.tipo}
              disabled
            />
          </div>

          <div className="escola-modal__field">
            <label htmlFor="escola-municipio">
              Município
            </label>

            <input
              id="escola-municipio"
              type="text"
              value={escola.municipio}
              disabled
            />
          </div>

          <div className="escola-modal__field">
            <label htmlFor="escola-endereco">
              Endereço
            </label>

            <input
              id="escola-endereco"
              type="text"
              value={endereco}
              onChange={(event) =>
                setEndereco(event.target.value)
              }
              placeholder="Informe o endereço"
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