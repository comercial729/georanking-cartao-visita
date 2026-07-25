# Backend da IA (geração de imagem)

Proxy local para a OpenAI. **A chave da OpenAI fica só aqui, no `.env` — nunca no frontend nem no git.**

## Rodar
1. Crie `.env` a partir de `.env.example` e cole a chave:
   ```
   OPENAI_API_KEY=sk-...
   PORT=8788
   ```
2. Dê 2 cliques em `INICIAR-IA.bat` (ou `python server.py`).
3. Abra o Cartão de Avaliação e clique **"Gerar design da marca"**.

## Como funciona
- Frontend (`Cartão de Avaliação.dc.html`) faz `POST http://127.0.0.1:8788/gerar-fundo`
  com `{ segmento, marca }`.
- O backend monta o prompt, chama `gpt-image-1` (1024x1536), e devolve a imagem
  em base64. O frontend aplica como fundo do cartão.
- Geração leva ~20-25s. Custo aproximado: qualidade `medium` ≈ US$ 0,15/imagem
  (mude `quality` para `low` no `server.py` para baratear nos testes).

## Segurança / produção
- `.env` está no `.gitignore` — a chave **não** é versionada.
- Para produção no GeoRanking, este endpoint deve virar uma rota no **backend**
  (Spring Boot), reutilizando a `OPENAI_API_KEY` do ambiente do servidor.
  O frontend público **nunca** deve conter a chave. Mudança estrutural =
  precisa do aval do Reinaldo/Arthur.
