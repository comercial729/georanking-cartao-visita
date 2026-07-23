# GeoRanking — Cartão de Visita / Presença Digital

Protótipo navegável de alta fidelidade (arquivo único) da feature **Presença Digital**, que fica dentro de **Gerenciar Perfil** no GeoRanking. É a camada pública de conversão do negócio, montada a partir dos dados do Perfil (fonte de verdade), sem recadastro.

## Estrutura (v2 — redesign do Claude Design)
- **`index.html`** → redireciona para **`Presença Digital.dc.html`** (protótipo principal: Visão geral, Cartão Digital, Página de Links + Mini-site, Compartilhar + NFC, Desempenho).
- **`Cartão de Avaliação.dc.html`** — Criador de Cartões de Avaliação: 35 modelos em 8 motores de design, filtro por estilo e por segmento (12 segmentos), paleta alterável por modelo, marca d'água pin GeoRanking em todos.
- Componentes: `CartaoAvaliacao.dc.html` (cartão), `CartaoPublico.dc.html`, `PaginaPublica.dc.html` + runtime `support.js`.
  ⚠️ **Não renomear** os arquivos `.dc.html` — o runtime importa componentes pelo nome via fetch (`<dc-import name="...">`), e por isso o protótipo precisa ser servido por **HTTP** (não abre por file://).
- `legacy-v1.html` — versão 1 (arquivo único), mantida como referência.

**Navegar:** botão flutuante (canto inferior direito) indexa as telas; sub-abas no topo navegam entre módulos.

## Biblioteca de artes + Integração (teste local)
- **`biblioteca/`** — 72 bases premium (12 segmentos × 6 estilos) + `catalog.json`. O criador de cartões tem a seção **"Arte de fundo · Biblioteca"**: filtro por segmento, thumbnail aplica a arte no cartão com scrim de contraste do próprio tema (conteúdo, QR e pin por cima).
- **`georanking-api.js`** — adaptador da API real (`GET /api/v1/business-profiles/{id}/details` → modelo da Presença), com fallback mock automático.
- **`integracao.html`** — harness de teste: configure base/profileId/token (fica no localStorage), teste a conexão e veja o perfil mapeado + contrato completo dos endpoints.
- **`TESTAR-LOCAL.bat`** — duplo clique sobe o servidor local (requer Python) e abre o navegador.
⚠️ Staging apenas — nada aqui escreve no GeoRanking produção.

## Módulos
- **Visão geral** + primeiro acesso (nunca abre vazio; já vem pré-preenchido pelo Perfil).
- **Cartão Digital** — editor (edição à esquerda, preview mobile ao vivo à direita) + página pública.
- **Página de Links** — blocos com drag & drop, editar/destacar/ocultar, e switch **Lista de Links ↔ Mini-site** (estilo Linktree, semi-pronto e editável).
- **Cartão de Avaliações** — criador de cartão para pedir avaliação no Google, com **24 modelos em 5 estilos** (Elegante/Luxo, Tech, Automotivo, Corporativo Clean, Vibrante), preview A6/A5/adesivo, QR e export PDF/PNG/Imprimir. Painel de **IA (GPT)** para gerar design a partir do logo.
- **Compartilhar** — link, WhatsApp, QR (baixar/testar) e **Cartão NFC** (gravação real via Web NFC no Chrome/Android).
- **Desempenho** — métricas 7/30/90 dias (UI).

## 📌 Brief ativo para o Claude Design
Ver **[BRIEF_BIBLIOTECA_ARTES.md](BRIEF_BIBLIOTECA_ARTES.md)** — especificação completa da biblioteca de artes por segmento (regras das bases, prompt kit, recolorização duotone, marca d'água com o pin GeoRanking, catálogo JSON e checklist de aceite).

## O que gostaríamos de aprimorar (foco visual)
Buscamos um acabamento **nível time de design profissional, moderno e premium**, mantendo **simplicidade de uso**:
1. Hierarquia visual, espaçamento e tipografia dos editores e da Visão geral.
2. As **páginas públicas** (Cartão e Mini-site) — deixá-las mais expressivas sem virar poluição.
3. Os **modelos do Cartão de Avaliações** — molduras, fundos temáticos e QR mais sofisticados por estilo.
4. Microinterações e estados (loading, sucesso, erro, vazio).

## Design system (resumo)
- Base Material-inspired, identidade GeoRanking. Azul primário `#1A73E8` / `#0B57D0`.
- Superfícies brancas, canvas `#F8FAFD`, bordas `#DADCE0`, raios 8–16px.
- Tipografia: Inter (UI), Playfair Display (cartões elegantes), Oswald (cartões tech/auto/vibrante).
- Ícones: Material Symbols Rounded. Sem glassmorphism, sem neon, sem emoji como ícone.

## Observações
- Dados de exemplo (CSA Casa da Segurança Eletrônica) são fictícios.
- O cabeçalho azul "Gerenciar Perfil" + navegação global são o **chrome do modal real** do GeoRanking (placeholder no protótipo); a feature é embutida nesse modal existente.
- Nenhum segredo/credencial no repositório.

> Feito com Claude Code · aberto para o Claude Design analisar e propor melhorias visuais.
