# Brief — Biblioteca de Artes GeoRanking (handoff para o Claude Design)

**Para:** Claude Design
**De:** GeoRanking (via Claude Code)
**Objetivo:** montar uma **biblioteca padrão de artes/fundos premium**, ampla e catalogada, para os Cartões de Avaliação (e derivados). Custo de geração é **único**; depois disso, cada cartão sai a **custo zero** — o sistema escolhe a base, **recolore para a paleta da marca do cliente**, aplica logo + texto + **QR real** e a **marca d'água GeoRanking**.

> Referência de qualidade: os 5 cartões-exemplo do time (joalheria preto+dourado, internet fibra azul tech, auto peças carbono, distribuidora branca corporativa, celular azul circuito). O protótipo vivo está em `index.html` (aba **Cartão de Avaliações**).

---

## 1. Regras de ouro de TODA base (inegociáveis)

1. **SEM texto, letras, números, logos ou QR** dentro da arte. (QR de IA não lê; texto de IA sai errado. Tudo isso é sobreposto pelo sistema.)
2. **Área central livre** (~55% central da composição calma/escura ou clara uniforme) — é onde entram título, QR e botão. Motivos decorativos ficam nas **bordas e cantos**.
3. **Monocromática ou duotone** (1 cor dominante + neutros). É o que permite recolorir por código para qualquer marca. Evitar arco-íris/multicolor.
4. **Composição vertical 2:3** (base mestra 2048×3072 px, ≥300 DPI equivalente). Derivados 1:1 e 9:16 podem ser crop da mestra quando a composição permitir.
5. Iluminação de estúdio, acabamento premium, sem rostos/pessoas, sem marcas reais (nada de logotipos de terceiros, produtos identificáveis de marca).
6. **Margens seguras:** nada essencial a menos de 6% das bordas (sangria de impressão).

## 2. Segmentos e cobertura

**Fase 1 (prioridade — clientes atuais):**
1. Joalheria & Boutique
2. Tecnologia & Internet (fibra, provedores)
3. Celular & Assistência Técnica
4. Automotivo (peças, oficina)
5. Segurança Eletrônica (câmeras, alarmes)
6. Distribuição & Escritório (toners, suprimentos, corporativo)

**Fase 2 (ampliação do portfólio):**
7. Food (restaurante, café, delivery)
8. Beleza & Estética
9. Saúde & Clínicas
10. Casa & Construção
11. Pet
12. Moda & Varejo

**Pack Universal (12 bases):** gradientes suaves, texturas de papel/linho, geométrico minimal, luxo escuro com brilho, clean claro com formas — servem para qualquer segmento sem motivo específico.

**Volume por segmento:** 3 estilos × 2 variações = **6 bases** por segmento.
Fase 1 = 36 bases + 12 universais = **~48 bases mestras**. Fase 2 adiciona +36.

## 3. Os 3 estilos de cada segmento

| Estilo | Vibe | Tratamento |
|---|---|---|
| **Premium Escuro** | luxo, noite | fundo escuro profundo, motivos do segmento nas bordas com brilho sutil, vinheta |
| **Clean Claro** | corporativo, leve | fundo claro, motivos em outline/aquarela muito sutis nas bordas, respiro |
| **Vibrante** | varejo, energia | cor dominante saturada, formas geométricas grandes, motivos estilizados |

## 4. Prompt kit (template mestre)

Use como base, trocando `[MOTIVOS]`, `[ESTILO]` e `[TOM]`:

```
Premium print-ready background artwork for a business review card.
[MOTIVOS DO SEGMENTO] arranged only along the edges and corners, elegant depth of field.
[ESTILO: deep dark luxury / bright clean corporate / bold vibrant] style.
Monochromatic [TOM: neutral gray / deep navy / warm gold] palette with soft neutrals, duotone-friendly.
Large calm empty area in the center for content overlay.
NO text, NO letters, NO numbers, NO logos, NO QR codes, NO people.
Vertical 2:3 composition, studio lighting, subtle vignette, high detail, 300 dpi print quality.
```

**Motivos por segmento (Fase 1):**
- Joalheria: anéis, gemas, colares desfocados, pó de brilho
- Tecnologia/Internet: fibras ópticas, ondas de luz, hexágonos, circuitos sutis
- Celular: smartphones de perfil, cabos, chips, vidro
- Automotivo: fibra de carbono, disco de freio, pistão, chave, faixa xadrez sutil
- Segurança Eletrônica: câmeras dome, lentes, feixes de luz, escudo abstrato
- Distribuição/Escritório: papel, impressora estilizada, formas corporativas, swoosh

## 5. Recolorização (por que monocromático)

Pipeline em produção: base em tons neutros → **duotone** (sombra = cor escura da marca, luz = cor clara da marca) via processamento de imagem (Canvas/Sharp). 1 base = infinitas paletas — o cliente vê a arte "na cor da marca dele" sem custo novo de IA. Por isso: nada de cenas multicoloridas.

## 6. Marca d'água GeoRanking (obrigatória em toda arte final)

- **Só o pin** do logo GeoRanking (o marcador de mapa) — não o logo completo.
- Monocromático, na **cor do texto do cartão**, **opacidade 45–55%**.
- Posição padrão: **centralizado abaixo do rodapé** do cartão (já implementado no protótipo — ver `.rc-mark` em `index.html`); alternativa: canto inferior direito com margem de 6 mm, **nunca sobre o QR**.
- Tamanho: ~4% da largura do cartão. Discreto, profissional — assina o serviço sem gritar.
- SVG de referência no protótipo (`.rc-mark svg`).

## 7. Entrega esperada (o que devolver)

1. **Bases PNG** organizadas: `biblioteca/{segmento}/{estilo}-{nn}.png` (ex.: `automotivo/escuro-01.png`), 2048×3072.
2. **`catalog.json`** com uma entrada por base:
```json
{
  "id": "automotivo-escuro-01",
  "segmento": "automotivo",
  "estilo": "premium-escuro",
  "tags": ["carbono", "pecas", "vinheta"],
  "tom_base": "neutro-escuro",
  "recolor": "duotone",
  "centro_livre": true,
  "arquivo": "automotivo/escuro-01.png"
}
```
3. **Folha de prova**: 1 imagem-grade com thumbnails de todas as bases para aprovação rápida.
4. Se possível, **2 variações de crop** por base mestra: 1:1 (post) e 9:16 (story).

## 8. Checklist de aceite (cada base)

- [ ] Zero texto/letra/número/logo/QR na imagem
- [ ] Centro calmo e utilizável (contraste suficiente para título + QR branco)
- [ ] Monocromática/duotone-friendly
- [ ] Motivos claros do segmento (reconhecível em 1s) sem clichê exagerado
- [ ] 2:3 vertical, 2048×3072, sem artefatos de IA visíveis (dedos, texto fantasma, distorções)
- [ ] Funciona nos 3 formatos de recorte (A6, A5, quadrado)

## 9. Extras que ampliam o valor (fase 2+)

- **Packs sazonais:** Natal, Black Friday, Dia das Mães, Dia dos Pais, aniversário da loja — mesmas regras, motivos sazonais nas bordas.
- **Formatos sociais:** cada arte vira também post 1:1 e story 9:16 "Avalie-nos no Google" — o lojista divulga no Instagram sem custo extra.
- O sistema fará **auto-match**: extrai a paleta do logo do cliente e escolhe/recolore a base mais próxima automaticamente.
