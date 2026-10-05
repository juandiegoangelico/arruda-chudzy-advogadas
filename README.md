# Arruda Chudzy Advogadas — Website Institucional

Website institucional moderno, responsivo e sofisticado desenvolvido para o escritório de advocacia boutique **Arruda Chudzy Advogadas** (OAB/SC 12.228), com sede em Lages – SC.

---

## 🏛️ Identidade Visual & Design System

A paleta de cores e tipografia foram especialmente concebidas para transmitir elegância, sofisticação feminina e alto padrão técnico:

| Elemento | Valor Hex | Descrição |
| :--- | :--- | :--- |
| **Cor Primária** | `#65194B` | Vinho profundo |
| **Cor Secundária** | `#742356` | Ameixa escuro |
| **Cor Destaque** | `#C9A0B8` | Rosa antigo |
| **Cor Texto Claro**| `#F8F2F5` | Whisper blush / Marfim |
| **Cor de Apoio** | `#D8CCD3` | Heather acinzentado |

### Tipografia
- **Títulos & Serifas:** *Cormorant Garamond* / *Playfair Display*
- **Textos & Interface:** *Plus Jakarta Sans*

---

## 👩‍⚖️ Nossas Sócias

### Dra. Julia Arruda de Souza
- **OAB/SC:** 72.463
- **Perfil:** Advogada com atuação especializada na construção de soluções jurídicas estratégicas nas áreas de Direito Médico e da Saúde, Contratos e Direito Criminal.

### Dra. Bianca Chudzy
- **OAB/SC:** 71.437
- **Perfil:** Advogada dedicada à atuação consultiva e contenciosa, oferecendo suporte jurídico qualificado e personalizado para proteção dos interesses de seus clientes.

---

## ⚖️ Áreas de Atuação

1. **Direito Médico e da Saúde**
   - Assessoria para médicos
   - Clínicas e consultórios
   - Termos e contratos médicos (TCLE)
   - Compliance em saúde
   - Defesa ética e administrativa perante CRM/CFM
   - Gestão de riscos jurídicos

2. **Contratos**
   - Elaboração de contratos
   - Revisão contratual
   - Negociações
   - Instrumentos empresariais
   - Prevenção de litígios

3. **Direito Criminal**
   - Defesa criminal
   - Acompanhamento de inquéritos
   - Consultoria preventiva
   - Atuação em audiências
   - Estratégias de proteção jurídica

---

## 📱 Contatos Oficiais & Localização

- **WhatsApp Oficial:** [(49) 99937-0099](https://wa.me/5549999370099)
- **Instagram:** [@arrudachudzy](https://www.instagram.com/arrudachudzy/)
- **Endereço:** Edifício Azteca, Sala 712, Rua Coronel Córdova, 458, Centro, Lages – SC, CEP 88502-000

---

## 🚀 Estrutura de Arquivos

```text
├── index.html                   # Página principal institucional
├── manifest.json                # Manifesto PWA com paleta oficial
├── robots.txt                   # Diretivas de rastreamento de busca
├── sitemap.xml                  # Mapa XML do site
├── README.md                    # Documentação do projeto
├── .gitignore                   # Arquivos ignorados pelo Git
├── .github/
│   └── workflows/
│       └── pages.yml            # Pipeline de deploy automático no GitHub Pages
└── assets/
    ├── css/
    │   ├── style.css            # Estilos globais, grid, tipografia, paleta
    │   └── animations.css       # Animações de scroll, micro-interações, reduced motion
    ├── js/
    │   ├── main.js              # Menu mobile, scrollspy, encolhimento de header, contato
    │   └── gallery.js           # Galeria dinâmica de eventos, modal <dialog> com light-dismiss
    └── images/
        ├── julia-arruda.jpg     # Fotografia profissional da Dra. Julia Arruda
        ├── bianca-chudzy.jpg    # Fotografia profissional da Dra. Bianca Chudzy
        ├── logo-monogram.svg    # Monograma vetorial AC oficial
        ├── logo-full.svg        # Logomarca vetorial completa
        ├── favicon.svg          # Ícone de navegador
        ├── hero-advocacia-saude.jpg # Imagem editorial boutique de abertura
        ├── office-consultation.jpg  # Sala de atendimento personalizado
        ├── events-lecture.jpg   # Palestras e eventos acadêmicos/jurídicos
        ├── contracts-desk.jpg   # Mesa executiva e instrumentos contratuais
        ├── logo.jpg             # Badge institucional
        └── og-preview.jpg       # Imagem Open Graph para WhatsApp e redes sociais
```

---

## 🛠️ Tecnologias & Melhores Práticas Aplicadas

- **Modern Web Guidance:**
  - Header adaptativo no scroll com detecção nativa (`CSS.supports`) e fallback performático.
  - Modal nativo `<dialog>` com fallback obrigatório de *light-dismiss* por clique no backdrop.
  - Acessibilidade WCAG AA, tags semânticas HTML5, skip links e suporte a `prefers-reduced-motion`.
- **SEO & Otimização:**
  - Metadados Open Graph e Twitter Cards integrados com imagem de compartilhamento 1200x630.
  - Dados estruturados Schema.org JSON-LD (`LegalService` e `Person` para as sócias).
  - Imagens com lazy-loading e `fetchpriority="high"` no Hero para otimização de LCP.
- **WhatsApp Bridge:**
  - Formulário com formatação automática de mensagem pré-configurada e botão flutuante com animação de pulso sutil.

---

## 🌐 Como Publicar (Deploy)

### 1. GitHub Pages (Automático)
1. Acesse as **Settings** do repositório no GitHub.
2. Navegue até a seção **Pages**.
3. Em **Build and deployment > Source**, selecione **GitHub Actions**.
4. O workflow `.github/workflows/pages.yml` já está configurado para publicar o site a cada push no branch `main`.

### 2. Vercel ou Netlify
- Basta conectar este repositório diretamente no painel da [Vercel](https://vercel.com) ou [Netlify](https://netlify.com). Por ser um projeto estático moderno, não requer nenhum comando de build (`Publish directory: .`).

---

**Arruda Chudzy Advogadas** &bull; OAB/SC 12.228 &bull; Todos os direitos reservados.
