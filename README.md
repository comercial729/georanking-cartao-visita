# GeoRanking — Cartão de Visita / Presença Digital

Protótipo navegável de alta fidelidade (arquivo único) da feature **Presença Digital**, que fica dentro de **Gerenciar Perfil** no GeoRanking. É a camada pública de conversão do negócio, montada a partir dos dados do Perfil (fonte de verdade), sem recadastro.

**Abrir:** `index.html` (mesmo conteúdo de `Presenca-Digital.dc.html`). HTML/CSS/JS puro, sem build. Fontes e ícones via Google Fonts (precisa de internet).
**Navegar:** botão flutuante **"Telas do protótipo"** (canto inferior direito) leva a todas as telas e estados. As sub-abas no topo também navegam.

## Módulos
- **Visão geral** + primeiro acesso (nunca abre vazio; já vem pré-preenchido pelo Perfil).
- **Cartão Digital** — editor (edição à esquerda, preview mobile ao vivo à direita) + página pública.
- **Página de Links** — blocos com drag & drop, editar/destacar/ocultar, e switch **Lista de Links ↔ Mini-site** (estilo Linktree, semi-pronto e editável).
- **Cartão de Avaliações** — criador de cartão para pedir avaliação no Google, com **24 modelos em 5 estilos** (Elegante/Luxo, Tech, Automotivo, Corporativo Clean, Vibrante), preview A6/A5/adesivo, QR e export PDF/PNG/Imprimir. Painel de **IA (GPT)** para gerar design a partir do logo.
- **Compartilhar** — link, WhatsApp, QR (baixar/testar) e **Cartão NFC** (gravação real via Web NFC no Chrome/Android).
- **Desempenho** — métricas 7/30/90 dias (UI).

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
