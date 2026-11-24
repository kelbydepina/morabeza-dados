"""Linha de comandos do projeto Morabeza (Sessão 3).

Uso:  python -m morabeza.cli --ilha Sal
"""
import argparse
import logging
import sys

from morabeza.apoio import faturacao_por_ilha, ler_vendas
from morabeza.config import carregar_config

logger = logging.getLogger(__name__)


def criar_parser() -> argparse.ArgumentParser:
    # TODO 5: cria um argparse.ArgumentParser com dois argumentos opcionais:
    #         --config (por defeito "config.yaml") e --ilha (sem valor por defeito).
    parser = argparse.ArgumentParser(description="Resumo de vendas da Morabeza")
    parser.add_argument("--config", default="config.yaml", help="ficheiro de configuração")
    parser.add_argument("--ilha", help="mostrar só a faturação desta ilha")
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = criar_parser().parse_args(argv)

    # TODO 6: carrega a configuração (args.config) e lê as vendas do ficheiro indicado nela.
    # TODO 7: regista no log: logger.info("Li %d vendas de %s", ...). Não uses print para isto.
    # TODO 8: calcula a faturação por ilha. Sem --ilha, imprime "Faturação total: <valor> <moeda>".
    #         Com --ilha, imprime "Faturação em <ilha>: <valor> <moeda>".
    #         Se a ilha não existir, logger.error(...) e devolve 1. No fim, devolve 0.
    config = carregar_config(args.config)
    caminho = config["ficheiro_vendas"]
    moeda = config["moeda"]
    vendas = ler_vendas(caminho)
    logger.info("Li %d vendas de %s", len(vendas), caminho)

    por_ilha = faturacao_por_ilha(vendas)
    if args.ilha is None:
        print(f"Faturação total: {sum(por_ilha.values())} {moeda}")
    elif args.ilha in por_ilha:
        print(f"Faturação em {args.ilha}: {por_ilha[args.ilha]} {moeda}")
    else:
        logger.error("Ilha desconhecida: %s", args.ilha)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
