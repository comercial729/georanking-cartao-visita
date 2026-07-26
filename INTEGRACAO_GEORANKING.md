# Subir o Cartão de Avaliação para o modal de Perfil do GeoRanking

O criador (`Cartão de Avaliação.dc.html`) já está **pronto para embutir** e **pré-preenche
sozinho** com os dados de cada perfil.

## Como embutir (recomendado: iframe)
No modal "Gerenciar Perfil", adicionar uma aba/seção "Cartão de Avaliação" com um iframe:

```html
<iframe
  src="https://SEU_HOST/Cartão%20de%20Avaliação.dc.html?profileId=PUBLIC_ID&token=BEARER_TOKEN"
  style="width:100%;height:820px;border:0"
  allow="clipboard-write"></iframe>
```

O iframe isola o runtime do cartão (support.js) do framework do site — não interfere no resto.

## Como ele pré-preenche (2 formas)
1. **Querystring:** `?profileId=<publicId>&token=<bearer>` (e opcional `&apiBase=`).
2. **postMessage** (quando o modal já tem o token em memória):
   ```js
   iframe.contentWindow.postMessage({ type:'geo-perfil', profileId, token }, '*');
   ```

Ele chama `GET /api/v1/business-profiles/{profileId}/details` (via `georanking-api.js`) e
mapeia: **nome → marca**, **categoria**, **iniciais**, **link de avaliação → QR**.
Sem token/perfil (ou se a API falhar) ele cai no **exemplo (CSA)** e mostra um selo avisando.

## O que o BACKEND precisa expor para ficar 100%
- **Link de avaliação do Google** no `/details` (o QR precisa dele). O adapter procura, nesta
  ordem: `googleReviewUrl` / `reviewUrl` / `reviewLink` / `googlePlaceId` (monta
  `search.google.com/local/writereview?placeid=...`) e, por fim, o `website`. **Basta o backend
  devolver um desses** (ideal: o Place ID). Enquanto não vier, o QR usa o site do perfil.
- **CORS**: `api.georanking.com.br` precisa liberar o host do cartão (ou servir o cartão no
  mesmo domínio → sem CORS).

## O que NÃO precisa de backend
- **"Vestir cartão na paleta da marca"**: é 100% no navegador (lê as cores da logo). Zero custo.
- **QR real + logo do GeoRanking no centro**: 100% no navegador (lib `qrcode.min.js`).

## O que ainda falta para produção (fora deste pacote)
1. **Exportar PDF/PNG de verdade**: hoje os botões são placeholders (mostram aviso). Falta
   plugar uma exportação real (render do cartão → imagem/PDF em alta). Posso implementar.
2. **"Melhorar logo" (IA de imagem)**: usa o backend `ai-backend/` — para produção, virar rota
   no Spring Boot reusando a `OPENAI_API_KEY` do servidor (a chave **nunca** vai no frontend).
3. **Aprovação**: entrar no front de produção do GeoRanking é mudança estrutural — precisa do
   aval do Reinaldo/Arthur e ir por **branch + PR** (nunca direto no main).

## Checklist rápido de deploy
- [ ] Hospedar os arquivos do cartão (mesmo domínio do app, de preferência).
- [ ] Backend devolver o link de avaliação (Place ID) no `/details`.
- [ ] Liberar CORS (ou mesmo domínio).
- [ ] Iframe no modal passando `profileId` + `token`.
- [ ] Implementar export PDF/PNG real.
- [ ] Testar com 3-4 perfis reais antes de liberar para clientes.
