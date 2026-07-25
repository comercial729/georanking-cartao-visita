#!/usr/bin/env python3
# Backend local do Cartao de Avaliacao: proxy para a OpenAI (geracao de imagem).
# A CHAVE fica so aqui (env / .env), NUNCA no frontend/repo publico.
import json, os, sys, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8788"))

def load_env():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

load_env()
API_KEY = os.environ.get("OPENAI_API_KEY", "")

def build_prompt(seg, marca):
    seg = (seg or "negocio local").strip()
    marca = (marca or "").strip()
    extra = f" da marca {marca}" if marca else ""
    return (
        f"Fundo vertical proporcao 2:3 para um cartao impresso de 'Avalie no Google'{extra}. "
        f"Tema visual: {seg}. Estilo 3D minimalista, luz suave, fundo claro e elegante. "
        "Inclua elementos sutis: estrelas douradas de avaliacao, um pin de localizacao do Google Maps, "
        "e toques discretos das cores do Google (azul, vermelho, amarelo, verde). "
        "MUITO IMPORTANTE: mantenha TODO O CENTRO da imagem vazio, limpo e claro (area livre), "
        "porque um QR code e textos serao colocados por cima depois. "
        "Sem nenhum texto, sem letras, sem numeros. Composicao com margens decoradas e centro livre. Alta qualidade."
    )

def gen_image(prompt, size="1024x1536", quality="medium"):
    body = json.dumps({
        "model": "gpt-image-1", "prompt": prompt,
        "size": size, "quality": quality, "n": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode("utf-8"))
    b64 = data["data"][0]["b64_json"]
    return "data:image/png;base64," + b64

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        # healthcheck
        self.send_response(200); self._cors()
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "hasKey": bool(API_KEY)}).encode())

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        except Exception:
            payload = {}
        if not API_KEY:
            return self._json(500, {"error": "OPENAI_API_KEY ausente no backend (.env)."})
        prompt = payload.get("prompt") or build_prompt(payload.get("segmento"), payload.get("marca"))
        try:
            img = gen_image(prompt, payload.get("size", "1024x1536"), payload.get("quality", "medium"))
            return self._json(200, {"image": img})
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:500]
            return self._json(e.code, {"error": "OpenAI: " + detail})
        except Exception as e:
            return self._json(500, {"error": str(e)})

    def _json(self, code, obj):
        self.send_response(code); self._cors()
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print(f"IA backend em http://127.0.0.1:{PORT}  (chave carregada: {bool(API_KEY)})")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
