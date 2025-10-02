import subprocess

RESOLVER = "8.8.8.8"   # troque para seu DNS interno se preferir
TIMEOUT  = "2"
TRIES    = "1"

for i in range(128, 132):       # 190.111.128.0 ... 190.111.131.255
    for j in range(256):
        ip = f"190.111.{i}.{j}"
        cmd = ["dig", "-x", ip, f"@{RESOLVER}", "+noall", "+answer", "+comments", f"+timeout={TIMEOUT}", f"+tries={TRIES}"]
        try:
            r = subprocess.run(cmd, text=True, capture_output=True)
            out = r.stdout.strip()
            if "status: NOERROR" in out and "\tPTR\t" in out:
                # há resposta PTR na seção ANSWER
                line = next((ln for ln in out.splitlines() if "\tPTR\t" in ln), "")
                ptr = line.split()[-1] if line else ""
                print(f"{ip} -> {ptr}")
            elif "status: NOERROR" in out:
                print(f"{ip} -> (NOERROR, mas sem PTR)")
            elif "status: NXDOMAIN" in out:
                print(f"{ip} -> (NXDOMAIN)")
            elif "status: SERVFAIL" in out or "status: REFUSED" in out:
                print(f"{ip} -> (erro DNS: SERVFAIL/REFUSED)")
            else:
                # Pode ser timeout, rede bloqueada, etc.
                err = r.stderr.strip()
                msg = err if err else (out if out else "sem saída (possível timeout/bloqueio)")
                print(f"{ip} -> (falha na consulta) {msg}")
        except Exception as e:
            print(f"{ip} -> ERRO: {e}")
