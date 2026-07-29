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

PROMPT_LOGO = (
    "Recrie esta logomarca como um arquivo limpo e profissional, pronto para impressao. "
    "Mantenha EXATAMENTE o mesmo desenho, as mesmas cores e o mesmo texto do original — "
    "nao invente elementos, nao mude palavras, nao adicione nada. "
    "Remova completamente o fundo (deixe fundo branco solido e uniforme), "
    "endireite e centralize a marca, corrija distorcao de perspectiva, "
    "deixe as bordas nitidas e as cores solidas. "
    "Remova ruido, sombra, reflexo, marca d'agua e qualquer resto de foto. "
    "Resultado: a mesma logo, apenas limpa e vetorizada visualmente."
)


def _multipart(campos, arquivos):
    """Monta multipart/form-data na mao (sem dependencia externa)."""
    limite = "----georanking" + os.urandom(8).hex()
    corpo = b""
    for k, v in campos.items():
        corpo += (f"--{limite}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for k, (nome, dados, tipo) in arquivos.items():
        corpo += (f"--{limite}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{nome}\"\r\n"
                  f"Content-Type: {tipo}\r\n\r\n").encode()
        corpo += dados + b"\r\n"
    corpo += f"--{limite}--\r\n".encode()
    return corpo, f"multipart/form-data; boundary={limite}"


def melhorar_logo(data_url, size="1024x1024"):
    """Limpa a logo do cliente: tira fundo, endireita, deixa pronta para impressao."""
    import base64
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    imagem = base64.b64decode(data_url)

    corpo, content_type = _multipart(
        {"model": "gpt-image-1", "prompt": PROMPT_LOGO, "size": size, "n": "1",
         "background": "opaque", "quality": "high"},
        {"image": ("logo.png", imagem, "image/png")},
    )
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/edits", data=corpo,
        headers={"Authorization": "Bearer " + API_KEY, "Content-Type": content_type},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    return "data:image/png;base64," + d["data"][0]["b64_json"]


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

        # rota de limpeza da logo do cliente
        if self.path.rstrip("/").endswith("melhorar-logo"):
            origem = payload.get("image") or payload.get("logo")
            if not origem:
                return self._json(400, {"error": "Envie a logo no campo 'image' (data URL)."})
            try:
                return self._json(200, {"image": melhorar_logo(origem, payload.get("size", "1024x1024"))})
            except urllib.error.HTTPError as e:
                return self._json(e.code, {"error": "OpenAI: " + e.read().decode("utf-8", "ignore")[:500]})
            except Exception as e:
                return self._json(500, {"error": str(e)})

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
