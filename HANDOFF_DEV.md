# Presença Digital — o que o dev precisa fazer

Documento para o **Arthur / Leroy Dev**. Objetivo: integrar dois módulos novos ao
GeoRanking **sem tocar em nada que já está rodando**.

Tudo o que está aqui já foi construído e testado. O que falta é **backend** (3 campos
no endpoint que já existe + 1 endpoint novo) e **1 aba** no modal.

---

## 1. Visão geral

Dois produtos entram no modal **Gerenciar Perfil** (`app.georanking.com.br/following-profiles`),
numa aba nova chamada **Presença Digital**:

| Produto | O que é | Onde roda |
|---|---|---|
| **Cartão de Avaliação** | Cartão para imprimir com QR que abre a avaliação no Google | Estático (HTML/JS), sem backend |
| **Mini-site** | Página do negócio estilo linktree, indexável | Next.js na Vercel |

**Nenhum dos dois escreve no banco hoje.** Ambos só **leem** o perfil.

---

## 2. O que muda no FRONT (1 aba)

Adicionar uma aba **"Presença Digital"** na barra do modal, depois de "SEO".
O conteúdo é a tela pronta em `Presença Digital.dc.html`.

⚠️ **Ao integrar, remover do arquivo o bloco marcado como `CHROME DO MODAL`** — ele
existe só para visualizar o encaixe. O app já desenha o cabeçalho azul e as abas.
O que entra é apenas o bloco marcado como `CONTEÚDO DA ABA`.

A tela já usa os tokens reais do sistema (medidos no app em produção):

| Token | Valor |
|---|---|
| Fonte | `Roboto` |
| Fundo | `#F8F9FA` |
| Azul | `#4285F4` (ativo/hover `#1967D2`) |
| Card | `#fff`, radius `8px`, borda `1px solid #E5E7EB`, sombra `0 1px 2px rgba(15,23,42,.04)` |
| Padding do card | `32px 36px 48px` |
| Largura do conteúdo | `1120px` |
| Título de seção | `20px / 600 / #202124` + barra azul de `4px` à esquerda |

---

## 3. O que muda no BACKEND

### 3.1 Acrescentar campos no endpoint que JÁ EXISTE (não quebra nada)

`GET /api/v1/business-profiles/{id}/details`

São **campos adicionais** no mesmo payload. Quem já consome o endpoint continua
funcionando (só ignora o que não conhece).

> ✅ **Fontes conferidas no banco de produção em 28/07/2026.** A tabela abaixo já
> está corrigida — a primeira versão deste documento assumia origens erradas.

| Campo no front | Fonte real no banco | Cobertura | Prioridade |
|---|---|---|---|
| `reviewUrl` | **`business_profile.review_url`** — já vem no formato certo (`search.google.com/local/writereview?placeid=...`) | **10.911 / 11.526 (94,7%)** | **ALTA** |
| `photos` | **tabela `photo_profile`** (NÃO `urls_image`, que está 100% vazia) | 132.665 fotos · **5.918 perfis com ≥3** | **ALTA** |
| `reviews` | tabela de avaliações | 274.652 · **6.703 perfis com ≥3** | ALTA |
| `rating` / `reviewCount` | agregado das avaliações | idem | MÉDIA |
| `hoursText` | horários do perfil | existe | BAIXA |
| `logoUrl` | ⚠️ **não existe fonte no schema** — precisa decidir (upload manual ou sync do GBP) | — | decisão |
| `serviceAreaDescription`, `faqs`, `coverUrl` | ⚠️ **não existem no schema** → vêm do **editor**, gravados no `jsonb` do item 3.2 | — | via editor |

🔴 **ARMADILHA — não mapear `googlePlaceId` ← `place_google_id`.**
Essa coluna guarda o **CID numérico** (ex.: `17725265890874731983`), que **não
funciona** na URL `writereview?placeid=`. Os cartões sairiam impressos com QR que
não abre a avaliação. **Use `review_url`, que já está pronto.**

O front aceita todos esses campos e funciona sem eles (cai em exemplo).
Ver o mapeamento em `georanking-minisite/lib/tenant.js` → `mapearTenant()`.

**Se der para fazer só uma coisa: expor `review_url`.** Destrava o Cartão de
Avaliação inteiro, sem custo e sem Places API.

### 3.2 Endpoint NOVO para salvar a configuração do mini-site

```
GET  /api/v1/business-profiles/{id}/minisite   -> devolve a config salva (ou 404)
PUT  /api/v1/business-profiles/{id}/minisite   -> salva
```

Corpo (JSON livre, uma coluna `jsonb`/`text` já resolve — não precisa modelar):

```json
{
  "template": "clean",
  "variacao": "beleza-dourado-elegante-suave-claro",
  "cores": { "accent": "#1a73e8", "onAccent": "#ffffff", "star": "#FBBC04" },
  "fontes": { "titulo": "'Inter',sans-serif", "texto": "'Inter',sans-serif" },
  "capa": "https://...", 
  "publicado": true,
  "slug": "csa-casa-da-seguranca"
}
```

> Sugestão: **uma tabela nova** `business_profile_minisite` (`profile_id`, `config jsonb`,
> `updated_at`). Assim nenhuma tabela existente é alterada.

### 3.3 CORS

O mini-site roda em outro domínio (Vercel). Liberar em `api.georanking.com.br`:
```
Access-Control-Allow-Origin: https://<dominio-do-minisite>
```
(ou servir o mini-site no mesmo domínio — aí não precisa de CORS.)

---

## 4. IA (opcional, só se for aprovado)

O botão **"Criar capa com IA"** gera a foto de capa. Hoje aponta para um backend
local (`ai-backend/server.py`) que faz proxy para a OpenAI.

Para produção: virar uma rota no Spring Boot reusando a `OPENAI_API_KEY` que **já
existe no ambiente do processo Java** (`/proc/<pid>/environ`). A chave **nunca** pode
ir para o frontend.

```
POST /api/v1/ai/imagem   { "prompt": "...", "size": "1536x1024" }  ->  { "image": "data:image/png;base64,..." }
```
Custo: ~US$ 0,15 por imagem (gpt-image-1, qualidade média). Sugiro limitar por perfil.

---

## 5. Deploy do mini-site (Vercel)

- Projeto: `georanking-minisite` (Next.js 16, App Router).
- Variáveis: `NEXT_PUBLIC_ROOT_DOMAIN`, `GEORANKING_API_BASE`, `GEORANKING_API_TOKEN`.
- Domínio: um **wildcard** `*.<dominio>` para dar um endereço por cliente
  (`cliente.dominio.com.br`). ⚠️ Wildcard SSL exige apontar os **nameservers para a Vercel**.
- **Não** cadastrar domínio próprio de cliente no início: o plano Hobby trava em
  **50 domínios por projeto**. Subdomínio é ilimitado.
- Páginas usam **ISR** (estático + revalida de hora em hora) — barato e rápido.

---

## 6. Regras de SEO que já estão no código (não remover)

Foram a parte mais sensível do projeto — protegem o cliente e o GeoRanking:

1. **Trava anti-duplicação**: o mini-site só é indexado com conteúdo único mínimo
   (texto do negócio, texto da área atendida, 3 avaliações, 3 FAQs, 3 fotos).
   Sem isso sai como rascunho + `noindex`. Evita dezenas de páginas clonadas
   trocando só a cidade — o maior risco de penalização.
2. **Indexação condicional**: cliente que **já tem site próprio** recebe `noindex`.
   O mini-site não compete com o site do próprio cliente.
3. `canonical`, Open Graph e **JSON-LD LocalBusiness** por página.

---

## 6.1 Quantos clientes a trava alcança (medido em produção, 28/07/2026)

| Situação | Perfis |
|---|---|
| Total na base | 11.526 |
| Passam texto + avaliações + fotos | **4.146** |
| Passam **e** seriam indexáveis (não têm site próprio) | **698** |
| Com FAQs no critério | 0 — FAQs não existem no banco (vêm do editor) |

**Leitura:** ~698 perfis teriam mini-site **indexável** hoje. Mas `noindex` **não
significa inútil**: os outros ~3.448 que passam no conteúdo continuam com um
mini-site funcional para usar como link na bio do Instagram/WhatsApp, em QR e em
campanhas — só não disputam o Google com o site do próprio cliente.

Ou seja, a trava não reduz o produto; ela separa **"vale ranquear"** de
**"vale como link"**. Decisão de posicionamento é do Reinaldo.

---

## 7. Impacto no que está rodando

| Item | Impacto |
|---|---|
| Endpoint `/details` | **Nenhum** — só ganha campos novos |
| Tabelas existentes | **Nenhum** — tabela nova e separada |
| Front atual | **Nenhum** — 1 aba a mais |
| Java/app.jar | Só se a IA for aprovada (rota nova) |

Sugestão de ordem: (1) `googlePlaceId` + `logoUrl` + `photos` → já libera os dois
produtos; (2) endpoint do mini-site; (3) resto dos campos; (4) IA.

---

## 8. Onde está o código

| Repositório | Conteúdo |
|---|---|
| `georanking-cartao-visita` (público) | Cartão de Avaliação, tela Presença Digital, `ai-backend` |
| `georanking-minisite` | Mini-site Next.js + editor |

Guia técnico da integração: `INTEGRACAO_GEORANKING.md`.

**Nada foi enviado para produção.** Tudo está em staging aguardando validação.
