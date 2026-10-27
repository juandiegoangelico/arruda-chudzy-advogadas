# Diretrizes de Segurança Cloudflare — Arruda Chudzy Advogadas

Este documento estabelece a configuração de borda (Edge Security) recomendada e auditada via `security-audit` para o portal `arrudachudzy.com.br`, garantindo proteção contra interceptação, roubo de credenciais no CMS e ataques automatizados.

---

## 1. Criptografia SSL/TLS (Borda e Origem)

Como o site é hospedado na origem via GitHub Pages (que fornece certificados assinados e válidos automaticamente para o domínio customizado), a comunicação entre a Cloudflare e a origem deve ser estritamente validada.

1. Acesse o painel da Cloudflare -> Selecione **arrudachudzy.com.br**.
2. Vá em **SSL/TLS** -> **Overview**:
   - Defina o modo como: **Full (Strict)**.
   - *Nota: Evite o modo "Flexible", pois ele trafega dados em texto claro (HTTP porta 80) entre a Cloudflare e o servidor de origem.*
3. Vá em **SSL/TLS** -> **Edge Certificates**:
   - **Always Use HTTPS**: `Ativado` (redireciona automaticamente todo tráfego HTTP para HTTPS).
   - **Minimum TLS Version**: `TLS 1.2` (desativa versões obsoletas TLS 1.0 e 1.1).
   - **Opportunistic Encryption**: `Ativado`.
   - **Automatic HTTPS Rewrites**: `Ativado`.

---

## 2. Injeção de Cabeçalhos de Segurança (Transform Rules)

Como servidores estáticos do GitHub Pages não permitem customização de cabeçalhos de resposta HTTP, a injeção deve ser realizada na camada de borda da Cloudflare.

1. No painel Cloudflare, vá em **Rules** -> **Transform Rules**.
2. Clique na aba **Modify Response Header** -> **Create rule**.
3. Configure a regra:
   - **Rule name**: `Security Headers - Arruda Chudzy`
   - **If incoming requests match**: `All incoming requests` (ou `Hostname equals arrudachudzy.com.br`)
   - Em **Modify response headers**, adicione as seguintes entradas (todas com operador `Set static`):

| Nome do Cabeçalho | Valor Recomendado | Finalidade |
| :--- | :--- | :--- |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | Força navegadores a utilizarem exclusivamente HTTPS por 1 ano. |
| `X-Content-Type-Options` | `nosniff` | Impede o navegador de adivinhar o tipo MIME de arquivos estáticos. |
| `X-Frame-Options` | `DENY` | Impede que o site seja embutido em iframes por terceiros (anti-clickjacking). |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Evita vazamento de caminhos e parâmetros de URL em requisições externas. |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | Desativa APIs de sensores e hardware desnecessárias para o site. |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://api.github.com; frame-ancestors 'none';` | Restringe origens de execução de scripts, fontes e conexões de API. |

4. Clique em **Deploy**.

---

## 3. Blindagem de Acesso ao Painel Administrativo (`/admin`)

O painel Sveltia CMS opera no caminho `/admin/`. Para evitar que robôs de varredura e raspadores façam requisições excessivas ou explorem a interface:

1. No painel Cloudflare, vá em **Security** -> **WAF** -> **Custom rules**.
2. Clique em **Create rule**:
   - **Rule name**: `Proteção contra Robôs em /admin`
   - **Field**: `URI Path`
   - **Operator**: `contains`
   - **Value**: `/admin`
   - **Action**: **Managed Challenge**
3. Clique em **Deploy**.

*Com essa regra, qualquer visitante ou bot não humano que tentar acessar a área de administração passará pelo desafio interativo invisível da Cloudflare, mitigando tentativas de varredura automatizada.*

---

## 4. Práticas Seguras para Autenticação no CMS

- Para ativar o acesso inicial no navegador de uma nova máquina/autora, prefira sempre o uso de **Fragmento de Hash**:
  `https://arrudachudzy.com.br/admin/#token=SEU_TOKEN_AQUI`
- O caractere `#` (hash fragment) garante que o segredo fique estritamente no cliente e **nunca seja transmitido nas requisições de rede ou cabeçalhos HTTP**, nem fique registrado em logs de proxy.
- O script em `admin/index.html` limpa a URL imediatamente após a leitura do token para que o histórico do navegador permaneça limpo.
