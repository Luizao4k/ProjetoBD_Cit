import { useEffect, useState } from "react";
import { X, Save } from "lucide-react";

import { atualizarDre } from "../services/dreService";
import type { Dre } from "../types/dre";

interface EditarDreModalProps {
  dre: Dre;
  onClose: () => void;
  onSuccess: (dreAtualizada: Dre) => void;
}

/**
 * Modal responsável pela edição dos dados de uma DRE.
 *
 * Atualmente permite alterar somente o telefone.
 */
export function EditarDreModal({
  dre,
  onClose,
  onSuccess,
}: EditarDreModalProps) {
  const [telefone, setTelefone] = useState(dre.telefone ?? "");
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  /**
   * Atualiza o telefone caso a DRE recebida pelo componente seja alterada.
   */
  useEffect(() => {
    setTelefone(dre.telefone ?? "");
  }, [dre]);

  /**
   * Salva as alterações da DRE.
   */
  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    try {
      setSalvando(true);
      setErro(null);

      const dreAtualizada = await atualizarDre(dre.id, {
        telefone: telefone.trim(),
      });

      onSuccess(dreAtualizada);
    } catch (error) {
      console.error("Erro ao atualizar DRE:", error);
      setErro("Não foi possível atualizar a DRE.");
    } finally {
      setSalvando(false);
    }
  }

  return (
    <div
      className="dre-modal__overlay"
      onClick={onClose}
    >
      <div
        className="dre-modal"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="dre-modal__header">
          <div>
            <h2>Editar DRE</h2>
            <p>Atualize os dados da diretoria.</p>
          </div>

          <button
            type="button"
            className="dre-modal__close"
            onClick={onClose}
            disabled={salvando}
            aria-label="Fechar"
          >
            <X size={20} />
          </button>
        </header>

        <form
          className="dre-modal__form"
          onSubmit={handleSubmit}
        >
          <div className="dre-modal__field">
            <label htmlFor="dre-nome">
              Nome
            </label>

            <input
              id="dre-nome"
              type="text"
              value={dre.nome}
              disabled
            />
          </div>

          <div className="dre-modal__field">
            <label htmlFor="dre-telefone">
              Telefone
            </label>

            <input
              id="dre-telefone"
              type="tel"
              value={telefone}
              onChange={(event) =>
                setTelefone(event.target.value)
              }
              placeholder="Informe o telefone"
              disabled={salvando}
              autoFocus
            />
          </div>

          {erro && (
            <div className="dre-modal__error">
              {erro}
            </div>
          )}

          <footer className="dre-modal__footer">
            <button
              type="button"
              className="dre-modal__cancel"
              onClick={onClose}
              disabled={salvando}
            >
              Cancelar
            </button>

            <button
              type="submit"
              className="dre-modal__save"
              disabled={salvando}
            >
              <Save size={17} />

              {salvando ? "Salvando..." : "Salvar"}
            </button>
          </footer>
        </form>
      </div>
    </div>
  );
}