import time
from pyfiglet import Figlet
from colorama import Fore, Style
from core.api import fetch_all_scopes
from core.database import DB
from core.diff import DiffEngine
from core.recon import ReconPipeline
from core.discord import send_discord
from core.logger import log


def banner():
    f = Figlet(font="slant")
    print(Fore.CYAN + f.renderText("Scope$craping") + Style.RESET_ALL)
    print(Fore.YELLOW + "HackerOne Scope Monitor & Auto Recon" + Style.RESET_ALL)
    print(Fore.WHITE + "-" * 60 + Style.RESET_ALL)


def main():
    banner()
    db = DB()
    diff = DiffEngine(db)
    recon = ReconPipeline()

    log("Iniciando atualização de escopos…")
    scopes = fetch_all_scopes()

    added, removed, updated = diff.compare(scopes)

    if added:
        log(f"{len(added)} novos escopos encontrados")
        send_discord(f"Novos escopos adicionados:\n" + "\n".join(added))
        for scope in added:
            recon.run(scope)

    if removed:
        log(f"{len(removed)} escopos removidos")
        send_discord(f"Escopos removidos:\n" + "\n".join(removed))

    if updated:
        log(f"{len(updated)} escopos atualizados")
        send_discord(f"Escopos atualizados:\n" + "\n".join(updated))

    db.save(scopes)
    log("Processo concluído.")


if __name__ == "__main__":
    main()
