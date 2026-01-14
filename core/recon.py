import subprocess
import os
from concurrent.futures import ThreadPoolExecutor
from core.logger import log


class ReconPipeline:

    def __init__(self):
      
        self.base_dir = "recon_data"
        self.sub_dir = os.path.join(self.base_dir, "subfinder")
        self.http_dir = os.path.join(self.base_dir, "httpx")
        self.wayback_dir = os.path.join(self.base_dir, "wayback")

        for path in [self.base_dir, self.sub_dir, self.http_dir, self.wayback_dir]:
            os.makedirs(path, exist_ok=True)

    def run(self, scope):
        log(f"Iniciando Recon para {scope}")

        with ThreadPoolExecutor(max_workers=3) as exe:
            exe.submit(self.subdomains, scope)
            exe.submit(self.http_scan, scope)
            exe.submit(self.archive_urls, scope)

        log(f"Recon concluído para {scope}")

    def subdomains(self, scope):
        output = os.path.join(self.sub_dir, f"{scope}_subs.txt")
        cmd = f"subfinder -d {scope} -silent -o {output}"

        log(f"Enumerando subdomínios ({scope})")
        subprocess.run(cmd, shell=True)

    def http_scan(self, scope):
        input_file = os.path.join(self.sub_dir, f"{scope}_subs.txt")
        output = os.path.join(self.http_dir, f"{scope}_alive.txt")
        cmd = f"httpx -l {input_file} -silent -o {output}"

        log(f"Verificando hosts ativos ({scope})")
        subprocess.run(cmd, shell=True)

    def archive_urls(self, scope):
        output = os.path.join(self.wayback_dir, f"{scope}_urls.txt")
        cmd = f"echo {scope} | waybackurls > {output}"

        log(f"Capturando URLs com waybackurls ({scope})")
        subprocess.run(cmd, shell=True)
