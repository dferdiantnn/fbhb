"""
Terminal UI, In-Place Spinner, and Step Progress Manager for HACKBEN.
"""

import sys
import time
import threading
from colorama import Fore, Style, init

init(autoreset=True)

VERSION = "11.0.8 (Universal Cross-Platform Edition)"

SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

class Spinner:
    """Animated in-place terminal spinner that does not create new lines."""
    
    def __init__(self, message: str = "", prefix: str = ""):
        self.message = message
        self.prefix = prefix
        self._running = False
        self._thread = None
        self._idx = 0

    def _spin(self):
        while self._running:
            frame = SPINNER_FRAMES[self._idx % len(SPINNER_FRAMES)]
            self._idx += 1
            text = f"\r\033[K{Fore.CYAN}[{frame}]{Fore.RESET} {self.prefix}{self.message}"
            sys.stdout.write(text)
            sys.stdout.flush()
            time.sleep(0.08)

    def start(self, message: str | None = None):
        if message:
            self.message = message
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()

    def update(self, message: str, prefix: str | None = None):
        self.message = message
        if prefix is not None:
            self.prefix = prefix

    def stop(self, final_text: str | None = None, success: bool = True):
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.2)
        if final_text:
            icon = f"{Fore.GREEN}✔{Fore.RESET}" if success else f"{Fore.RED}✖{Fore.RESET}"
            sys.stdout.write(f"\r\033[K[{icon}] {self.prefix}{final_text}\n")
        else:
            sys.stdout.write("\r\033[K")
        sys.stdout.flush()


def print_banner(store_name: str | None = None, mode: str | None = None, headless: bool = True):
    """Render authentic Bento Box terminal banner for HACKBEN."""
    bento = (
        f"{Fore.GREEN}hackben@localhost:$ deploy_Bento.sh --casual-mode\n\n"
        f"{Fore.WHITE}System core:\n"
        f"Network: Integrt:\n"
        f"{Fore.GREEN}hackben@localhost:${Fore.WHITE}\n"
        f"System Integrity: {Fore.GREEN}Nominal\n\n"
        f"{Fore.WHITE}._________________________________________________________.\n"
        f"|  #   #     #   |        {Fore.GREEN}/------------\\{Fore.WHITE}                 |\n"
        f"|    #   # #     |       {Fore.GREEN}/      {Fore.YELLOW}@{Fore.GREEN}       \\{Fore.WHITE}                |\n"
        f"|     # ### #    |      {Fore.GREEN}|       {Fore.YELLOW}@{Fore.GREEN}        |{Fore.WHITE}               |\n"
        f"|    # ## #      |      {Fore.GREEN}|      {Fore.YELLOW}@@{Fore.GREEN}        |{Fore.WHITE}               |\n"
        f"|   #     #   #  |       {Fore.GREEN}\\      {Fore.YELLOW}@{Fore.GREEN}       /{Fore.WHITE}                |\n"
        f"|     #   # #    |        {Fore.GREEN}\\____/ \\_____/{Fore.WHITE}                 |\n"
        f"|________________|________________________________________|\n"
        f"|  {Fore.CYAN}/\\{Fore.WHITE}            |       | |    {Fore.GREEN}\\    /{Fore.WHITE}                   |\n"
        f"| {Fore.CYAN}/  \\{Fore.WHITE}     #     |       |{Fore.YELLOW}\'{Fore.WHITE}|    {Fore.GREEN}( - ){Fore.WHITE}                  |\n"
        f"| {Fore.CYAN}\\  /{Fore.WHITE}       ##  |_______|_|   {Fore.GREEN}/ \\_/ \\{Fore.WHITE}                 |\n"
        f"|  {Fore.CYAN}\\/{Fore.WHITE}   /-\\      |             {Fore.GREEN}|     |{Fore.WHITE}                 |\n"
        f"|      (   )  #  |            {Fore.GREEN}/ \\___/ \\{Fore.WHITE}                |\n"
        f"|   #    #   #   |           {Fore.GREEN}/_________\\{Fore.WHITE}               |\n"
        f"|________________|________________________________________|\n"
        f" \\______________________________________________________/\n\n"
        f"     {Fore.GREEN}{Style.BRIGHT}██╗  ██╗ █████╗  ██████╗██╗  ██╗██████╗ ███████╗███╗   ██╗\n"
        f"     ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝████╗  ██║\n"
        f"     ███████║███████║██║     █████═╝ ██████╔╝█████╗  ██╔██╗ ██║\n"
        f"     ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══██╗██╔══╝  ██║╚██╗██║\n"
        f"     ██║  ██║██║  ██║╚██████╗██║ ╚██╗██████╔╝███████╗██║ ╚████║\n"
        f"     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝{Fore.RESET}\n"
    )
    print(bento)
    print(Fore.CYAN + "=" * 61)
    print(Fore.WHITE + f"   📦 Versi     : {VERSION}")
    if store_name:
        print(Fore.WHITE + f"   🎯 Target    : {store_name}")
    if mode:
        print(Fore.WHITE + f"   🌐 Jaringan  : {mode}")
    print(Fore.WHITE + f"   👁️  Tampilan  : {'Background (Headless)' if headless else 'Visual Window'}")
    print(Fore.CYAN + "=" * 61 + "\n")


def print_step(step_curr: int, step_total: int, text: str, status: str = "running"):
    """Format step prefix like [Step 1/7]."""
    prefix = f"{Fore.YELLOW}[Step {step_curr}/{step_total}]{Fore.RESET} "
    return prefix, text
