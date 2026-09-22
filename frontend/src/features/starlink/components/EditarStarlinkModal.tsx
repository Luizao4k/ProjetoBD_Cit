import { useState } from "react";
import {
  atualizarStarlink,
  type Starlink,
} from "../services/starlinkService";

interface EditarStarlinkModalProps {
  starlink: Starlink;
  onClose: () => void;
  onSuccess: (starlinkAtualizado: Starlink) => void;
}

export function EditarStarlinkModal({
  starlink,
  onClose,
  onSuccess,
}: EditarStarlinkModalProps) {
  const [designacao, setDesignacao] = useState(
    starlink.designacao,
  );

  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    try {
      setSalvando(true);
      setErro(null);

      const starlinkAtualizado = await atualizarStarlink(
        starlink.id,
        {
          designacao,
        },
      );

      onSuccess(starlinkAtualizado);
    } catch (error) {
      console.error("Erro ao atualizar Starlink:", error);
      setErro("Não foi possível atualizar a Starlink.");
    } finally {
      setSalvando(false);
    }
  }

  return (
    <div className="escola-modal__overlay">
      <div className="escola-modal">
        <div className="escola-modal__header">
          <h2>Editar Starlink</h2>

          <button
            type="button"
            className="escola-modal__close"
            onClick={onClose}
            disabled={salvando}
          >
            ×
          </button>
        </div>

        <form
          className="escola-modal__form"
          onSubmit={handleSubmit}
        >
          <div className="escola-modal__field">
            <label htmlFor="starlink-designacao">
              Designação
            </label>

            <input
              id="starlink-designacao"
              type="text"
              value={designacao}
              onChange={(event) =>
                setDesignacao(event.target.value)
              }
              disabled={salvando}
              required
            />
          </div>

          {erro && (
            <p className="escola-modal__error">
              {erro}
            </p>
          )}

          <div className="escola-modal__footer">
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
              {salvando ? "Salvando..." : "Salvar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}