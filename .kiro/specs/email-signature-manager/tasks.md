# Plano de Implementação: Email Signature Manager

## Visão Geral

Implementação de uma ferramenta web frontend estática para geração de assinaturas de e-mail em HTML para a equipe DOit. A aplicação utiliza HTML + CSS + JavaScript vanilla, sem frameworks ou build tools para produção. Testes são executados com vitest + fast-check como dependências de desenvolvimento.

## Tasks

- [x] 1. Configuração do projeto e estrutura base
  - [x] 1.1 Criar `package.json` com dependências de desenvolvimento (vitest, fast-check) e scripts de teste
    - Configurar `"type": "module"` para suporte a ES modules
    - Adicionar script `"test": "vitest --run"` e `"test:watch": "vitest"`
    - _Requisitos: 8.1, 8.5_

  - [x] 1.2 Criar arquivo de configuração do vitest (`vitest.config.js`)
    - Configurar environment jsdom para testes que manipulam DOM
    - _Requisitos: 8.2_

  - [x] 1.3 Criar estrutura de diretórios e arquivos vazios
    - Criar `index.html`, `css/style.css`, `js/app.js`, `js/signature-generator.js`
    - Criar diretório `tests/` com arquivos de teste vazios
    - _Requisitos: 8.2_

- [x] 2. Implementar módulo gerador de assinatura (`js/signature-generator.js`)
  - [x] 2.1 Implementar função `formatPhoneForWhatsApp(phone)`
    - Se o número começa com `+`, remover `+` e caracteres não numéricos, prefixar com `%2B`
    - Se NÃO começa com `+`, remover caracteres não numéricos, prefixar com `%2B55`
    - _Requisitos: 9.1, 9.3_

  - [x] 2.2 Implementar função auxiliar de escape de caracteres HTML
    - Escapar `<`, `>`, `&`, `"` para entidades HTML
    - Proteger contra quebra de estrutura HTML por dados do usuário
    - _Requisitos: 5.10_

  - [x] 2.3 Implementar função `generateSignature(data)`
    - Gerar estrutura de tabela com `border="0"`, `cellpadding="0"`, `cellspacing="0"`
    - Coluna esquerda (~225px): foto (condicional), nome (condicional, negrito), cargo (condicional)
    - Coluna direita: links de contato (Instagram, WhatsApp, e-mail, website) — cada um condicional
    - Todos os estilos inline, sem classes CSS
    - Fonte Arial, Helvetica, sans-serif em todos os elementos de texto
    - Links com `color: black; text-decoration: none; target="_blank"`
    - Linhas de contato com `font-size: 12px; line-height: 18px`
    - _Requisitos: 2.2, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 9.2_

  - [x] 2.4 Exportar funções públicas do módulo
    - Exportar `generateSignature` e `formatPhoneForWhatsApp`
    - _Requisitos: 8.2_

  - [ ]* 2.5 Escrever teste de propriedade para codificação do telefone WhatsApp
    - **Propriedade 4: Codificação do telefone para WhatsApp**
    - Gerar strings de telefone com/sem prefixo `+`, verificar formato da saída
    - **Valida: Requisitos 9.1, 9.3**

  - [ ]* 2.6 Escrever teste de propriedade para preservação visual do telefone
    - **Propriedade 5: Preservação visual do telefone**
    - Verificar que o texto visível do link é exatamente a string original
    - **Valida: Requisito 9.2**

  - [ ]* 2.7 Escrever teste de propriedade para renderização de nome e cargo
    - **Propriedade 1: Renderização de nome e cargo**
    - Gerar nomes e cargos não-vazios, verificar presença com estilos corretos
    - **Valida: Requisitos 2.2, 4.1, 4.2, 4.3, 4.4**

  - [ ]* 2.8 Escrever teste de propriedade para elemento de foto
    - **Propriedade 2: Corretude do elemento de foto**
    - Gerar URLs válidas (https://...) e nomes, verificar `<img>` com src e alt corretos
    - **Valida: Requisitos 3.1, 3.2, 3.4**

  - [ ]* 2.9 Escrever teste de propriedade para links de contato
    - **Propriedade 3: Formato dos links de contato**
    - Verificar formato dos hrefs de Instagram, WhatsApp, e-mail e website
    - **Valida: Requisitos 5.4, 5.5, 5.6, 5.7**

  - [ ]* 2.10 Escrever teste de propriedade para estrutura de tabela e estilos inline
    - **Propriedade 6: Invariante de estrutura de tabela e estilos inline**
    - Verificar atributos da tabela, duas colunas, ausência de classes, estilos inline
    - **Valida: Requisitos 5.1, 5.2, 5.10**

  - [ ]* 2.11 Escrever teste de propriedade para estilização dos links
    - **Propriedade 7: Estilização dos links de contato**
    - Verificar estilos inline dos links e divs de contato
    - **Valida: Requisitos 5.8, 5.9**

  - [ ]* 2.12 Escrever testes unitários para omissão condicional de elementos
    - Testar que campos vazios resultam em omissão dos respectivos elementos HTML
    - Testar escape de caracteres especiais no nome e cargo
    - _Requisitos: 3.5, 4.5, 4.6_

- [ ] 3. Checkpoint - Verificar testes do módulo gerador
  - Garantir que todos os testes passam, perguntar ao usuário se houver dúvidas.

- [x] 4. Implementar estrutura HTML (`index.html`)
  - [x] 4.1 Criar página HTML com formulário de dados
    - Seletor de região (select com opções "Brasil" e "USA")
    - Campos: nome (text), cargo (text), URL da foto (text), e-mail (email), telefone (tel), Instagram (text), website (text)
    - Placeholders descritivos em cada campo
    - _Requisitos: 1.1, 2.1_

  - [x] 4.2 Criar seção de preview ao vivo
    - Container para renderização do HTML gerado
    - _Requisitos: 6.1, 6.3_

  - [x] 4.3 Criar seção de área de código com botão de cópia
    - Elemento para exibição do código HTML em texto
    - Botão "Copiar" com área para feedback visual
    - _Requisitos: 7.1, 7.3_

  - [x] 4.4 Incluir scripts (`js/app.js` e `js/signature-generator.js`) com `type="module"`
    - _Requisitos: 8.2, 8.5_

- [x] 5. Implementar estilos da interface (`css/style.css`)
  - [x] 5.1 Estilizar layout geral da página
    - Layout responsivo para formulário, preview e área de código
    - Adaptação a diferentes tamanhos de tela
    - _Requisitos: 8.4_

  - [x] 5.2 Estilizar formulário e campos de entrada
    - Estados de validação (erro/sucesso) com mensagens visuais
    - _Requisitos: 2.4, 2.5, 2.6_

  - [x] 5.3 Estilizar preview container e área de código
    - Preview com borda/fundo para destaque visual
    - Área de código com fonte monospace e scroll
    - Botão de cópia com feedback visual (estado de sucesso temporário)
    - _Requisitos: 6.1, 7.1, 7.4_

- [x] 6. Implementar lógica principal (`js/app.js`)
  - [x] 6.1 Implementar funções de validação de campos
    - `validateEmail(email)`: verificar formato com `@` e `.` após o `@`
    - `validatePhone(phone)`: aceitar apenas dígitos, parênteses, espaços, hífens e `+` no início
    - `validatePhotoUrl(url)`: verificar que inicia com "https://"
    - Exportar funções de validação para testes
    - _Requisitos: 2.4, 2.5, 2.6_

  - [x] 6.2 Implementar `handleRegionChange(region)`
    - Atualizar campos Instagram e website com valores padrão da região selecionada
    - Usar constantes `REGION_DEFAULTS` (brasil/usa)
    - Disparar atualização do preview após mudança
    - _Requisitos: 1.2, 1.3, 1.4_

  - [x] 6.3 Implementar `handleFormInput()` e atualização do preview
    - Coletar todos os valores do formulário em objeto `SignatureData`
    - Chamar `generateSignature(data)` e atualizar preview + área de código
    - Executar validação visual dos campos
    - Atualização em menos de 500ms após alteração
    - _Requisitos: 2.3, 6.2, 7.2_

  - [x] 6.4 Implementar `copyToClipboard()` com fallback
    - Tentar `navigator.clipboard.writeText()` primeiro
    - Fallback: criar `<textarea>` temporário, selecionar e `document.execCommand('copy')`
    - Se falhar, manter texto selecionado para cópia manual
    - Exibir confirmação visual temporária após sucesso
    - _Requisitos: 7.3, 7.4, 7.5_

  - [x] 6.5 Implementar `init()` — inicialização e registro de event listeners
    - Registrar listeners de `input` e `change` nos campos do formulário
    - Registrar listener de `change` no seletor de região
    - Registrar listener de `click` no botão de cópia
    - Chamar `handleRegionChange` com região inicial para pré-preencher campos
    - _Requisitos: 1.1, 2.3, 6.2_

  - [ ]* 6.6 Escrever teste de propriedade para validação de e-mail
    - **Propriedade 8: Validação de e-mail**
    - Gerar strings válidas (com @, texto antes/depois, . após @) e inválidas
    - **Valida: Requisito 2.4**

  - [ ]* 6.7 Escrever teste de propriedade para validação de telefone
    - **Propriedade 9: Validação de telefone**
    - Gerar strings com caracteres permitidos e proibidos
    - **Valida: Requisito 2.5**

  - [ ]* 6.8 Escrever teste de propriedade para validação de URL da foto
    - **Propriedade 10: Validação de URL da foto**
    - Gerar strings com/sem prefixo "https://"
    - **Valida: Requisito 2.6**

  - [ ]* 6.9 Escrever testes unitários para lógica de UI
    - Testar seleção de região e pré-preenchimento de campos
    - Testar funcionalidade de cópia (mock clipboard API)
    - Testar feedback visual após cópia
    - Testar fallback quando clipboard não disponível
    - _Requisitos: 1.2, 1.3, 1.4, 7.3, 7.4, 7.5_

- [ ] 7. Checkpoint final - Verificar integração completa
  - Garantir que todos os testes passam, perguntar ao usuário se houver dúvidas.

## Notas

- Tasks marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Cada task referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Testes de propriedade validam propriedades universais de corretude
- Testes unitários validam exemplos específicos e edge cases
- A aplicação em produção não depende de vitest/fast-check — são apenas dev dependencies
