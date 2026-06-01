# Documento de Requisitos

## Introdução

Ferramenta web para gerenciar e gerar assinaturas de e-mail em HTML para a equipe DOit. A ferramenta permite que os membros da equipe preencham seus dados em um formulário e obtenham o código HTML da assinatura pronto para uso. A assinatura é gerada inteiramente em HTML com elementos separados para foto, nome, cargo e informações de contato, utilizando layout de tabela para compatibilidade com clientes de e-mail. A aplicação é puramente frontend, sem dependências de servidor, e pode ser publicada como site estático.

## Glossário

- **Gerador_de_Assinatura**: Sistema web frontend responsável por gerar o código HTML da assinatura de e-mail a partir dos dados informados pelo usuário.
- **Formulário_de_Dados**: Interface de entrada onde o usuário preenche as informações pessoais e de contato para a assinatura.
- **Preview_ao_Vivo**: Área da interface que exibe em tempo real a renderização visual da assinatura conforme os dados são preenchidos.
- **Região**: Variante geográfica da assinatura (Brasil ou USA) que determina valores padrão de Instagram e website.
- **Template_HTML**: Estrutura HTML baseada em tabela que compõe a assinatura de e-mail, com layout de duas colunas: foto/nome/cargo à esquerda e links de contato à direita.
- **Coluna_Esquerda**: Seção da assinatura (~225px de largura) que contém a foto da pessoa como elemento `<img>`, o nome e o cargo renderizados como texto HTML.
- **Coluna_Direita**: Seção da assinatura que contém os links de contato (Instagram, telefone, e-mail, website).
- **Área_de_Código**: Seção da interface que exibe o código HTML gerado da assinatura para cópia.

## Requisitos

### Requisito 1: Seleção de Região

**User Story:** Como membro da equipe DOit, eu quero selecionar a região (Brasil ou USA), para que os campos de Instagram e website sejam pré-preenchidos com os valores corretos da minha região.

#### Critérios de Aceitação

1. THE Formulário_de_Dados SHALL exibir um seletor de região com as opções "Brasil" e "USA".
2. WHEN a região "Brasil" é selecionada, THE Gerador_de_Assinatura SHALL pré-preencher o campo Instagram com "doitsistema" e o campo website com "www.doit.com.br".
3. WHEN a região "USA" é selecionada, THE Gerador_de_Assinatura SHALL pré-preencher o campo Instagram com "doit.systems" e o campo website com "www.doiterp.com".
4. WHEN a região é alterada, THE Gerador_de_Assinatura SHALL atualizar os campos de Instagram e website com os novos valores padrão da região selecionada.

### Requisito 2: Formulário de Dados da Assinatura

**User Story:** Como membro da equipe DOit, eu quero preencher meus dados pessoais e de contato em um formulário, para que a assinatura seja gerada com minhas informações completas.

#### Critérios de Aceitação

1. THE Formulário_de_Dados SHALL exibir campos para: nome da pessoa, cargo, URL da foto (imagem de perfil), endereço de e-mail, número de telefone (formato WhatsApp), handle do Instagram e URL do website.
2. THE Formulário_de_Dados SHALL incluir os campos de nome e cargo no HTML gerado como elementos de texto na Coluna_Esquerda da assinatura.
3. WHEN qualquer campo do formulário é alterado, THE Preview_ao_Vivo SHALL atualizar a visualização da assinatura em tempo real.
4. THE Formulário_de_Dados SHALL validar que o campo de e-mail contém um formato de e-mail válido.
5. THE Formulário_de_Dados SHALL validar que o campo de telefone contém apenas números, parênteses, espaços e hífens.
6. THE Formulário_de_Dados SHALL validar que a URL da foto é uma URL válida iniciando com "https://".

### Requisito 3: Renderização da Foto na Assinatura

**User Story:** Como membro da equipe DOit, eu quero que minha foto apareça na assinatura como um elemento de imagem HTML, para que seja exibida corretamente em todos os clientes de e-mail.

#### Critérios de Aceitação

1. THE Gerador_de_Assinatura SHALL renderizar a foto da pessoa como um elemento `<img>` na Coluna_Esquerda da assinatura.
2. THE Gerador_de_Assinatura SHALL definir o atributo src do elemento `<img>` com a URL fornecida pelo usuário no formulário.
3. THE Gerador_de_Assinatura SHALL aplicar dimensões fixas na foto para manter a proporção visual consistente dentro da Coluna_Esquerda.
4. THE Gerador_de_Assinatura SHALL incluir o atributo alt no elemento `<img>` com o nome da pessoa como valor.
5. IF a URL da foto não for fornecida, THEN THE Gerador_de_Assinatura SHALL omitir o elemento `<img>` da assinatura.

### Requisito 4: Renderização do Nome e Cargo na Assinatura

**User Story:** Como membro da equipe DOit, eu quero que meu nome e cargo apareçam como texto HTML na assinatura, para que sejam legíveis e editáveis sem depender de uma imagem externa.

#### Critérios de Aceitação

1. THE Gerador_de_Assinatura SHALL renderizar o nome da pessoa como um elemento de texto na Coluna_Esquerda, abaixo da foto.
2. THE Gerador_de_Assinatura SHALL aplicar estilo de fonte em negrito no nome para diferenciá-lo visualmente do cargo.
3. THE Gerador_de_Assinatura SHALL renderizar o cargo da pessoa como um elemento de texto na Coluna_Esquerda, abaixo do nome.
4. THE Gerador_de_Assinatura SHALL aplicar fonte "Arial, Helvetica, sans-serif" nos elementos de nome e cargo.
5. IF o nome não for fornecido, THEN THE Gerador_de_Assinatura SHALL omitir o elemento de nome da assinatura.
6. IF o cargo não for fornecido, THEN THE Gerador_de_Assinatura SHALL omitir o elemento de cargo da assinatura.

### Requisito 5: Geração do HTML da Assinatura

**User Story:** Como membro da equipe DOit, eu quero que o HTML da assinatura seja gerado automaticamente com layout de tabela, para que eu possa usá-lo no meu cliente de e-mail com compatibilidade garantida.

#### Critérios de Aceitação

1. THE Gerador_de_Assinatura SHALL produzir código HTML utilizando uma estrutura de tabela com border="0", cellpadding="0" e cellspacing="0".
2. THE Gerador_de_Assinatura SHALL organizar a assinatura em duas colunas: a Coluna_Esquerda com foto, nome e cargo, e a Coluna_Direita com os links de contato.
3. THE Gerador_de_Assinatura SHALL definir a largura da Coluna_Esquerda em aproximadamente 225px para acomodar foto, nome e cargo.
4. THE Gerador_de_Assinatura SHALL gerar o link do Instagram com href no formato "https://www.instagram.com/{handle}/" e target="_blank".
5. THE Gerador_de_Assinatura SHALL gerar o link do telefone com href no formato "https://api.whatsapp.com/send/?phone={numero_codificado}" e target="_blank".
6. THE Gerador_de_Assinatura SHALL gerar o link do e-mail com href no formato "mailto:{email}" e target="_blank".
7. THE Gerador_de_Assinatura SHALL gerar o link do website com href no formato "https://{website}/" e target="_blank".
8. THE Gerador_de_Assinatura SHALL aplicar estilo "color: black; text-decoration: none" em todos os links de contato.
9. THE Gerador_de_Assinatura SHALL aplicar fonte "Arial, Helvetica, sans-serif" com tamanho 12px e line-height 18px em cada linha de contato na Coluna_Direita.
10. THE Gerador_de_Assinatura SHALL utilizar estilos inline em todos os elementos para garantir compatibilidade com clientes de e-mail.

### Requisito 6: Preview ao Vivo

**User Story:** Como membro da equipe DOit, eu quero visualizar a assinatura em tempo real enquanto preencho os dados, para que eu possa verificar como ficará antes de copiar.

#### Critérios de Aceitação

1. THE Preview_ao_Vivo SHALL renderizar o HTML gerado como conteúdo visual na página.
2. WHEN qualquer campo do Formulário_de_Dados é modificado, THE Preview_ao_Vivo SHALL atualizar a renderização em menos de 500ms.
3. THE Preview_ao_Vivo SHALL exibir a foto, nome e cargo na Coluna_Esquerda e os links de contato na Coluna_Direita.
4. THE Preview_ao_Vivo SHALL representar fielmente a aparência final da assinatura como será vista no cliente de e-mail.

### Requisito 7: Exibição e Cópia do Código HTML

**User Story:** Como membro da equipe DOit, eu quero visualizar o código HTML gerado e copiá-lo com um clique, para que eu possa colá-lo facilmente no meu cliente de e-mail.

#### Critérios de Aceitação

1. THE Área_de_Código SHALL exibir o código HTML completo gerado da assinatura em formato texto legível.
2. WHEN o código HTML é atualizado, THE Área_de_Código SHALL refletir as alterações automaticamente.
3. WHEN o botão "Copiar" é clicado, THE Gerador_de_Assinatura SHALL copiar o código HTML completo para a área de transferência do navegador.
4. WHEN a cópia é realizada com sucesso, THE Gerador_de_Assinatura SHALL exibir uma confirmação visual temporária ao usuário.
5. IF a API de clipboard do navegador não estiver disponível, THEN THE Gerador_de_Assinatura SHALL selecionar o texto do código automaticamente para cópia manual.

### Requisito 8: Arquitetura Frontend Estática

**User Story:** Como desenvolvedor da equipe DOit, eu quero que a ferramenta seja puramente frontend sem dependências de servidor, para que possa ser publicada como site estático em qualquer hospedagem.

#### Critérios de Aceitação

1. THE Gerador_de_Assinatura SHALL funcionar inteiramente no navegador sem requisições a servidores backend.
2. THE Gerador_de_Assinatura SHALL ser composto por arquivos separados de HTML, CSS e JavaScript.
3. THE Gerador_de_Assinatura SHALL ser compatível com os navegadores modernos (Chrome, Firefox, Safari, Edge em suas versões atuais).
4. THE Gerador_de_Assinatura SHALL apresentar uma interface responsiva que se adapta a diferentes tamanhos de tela.
5. THE Gerador_de_Assinatura SHALL carregar sem dependências externas de CDN ou bibliotecas de terceiros.

### Requisito 9: Formatação do Número de Telefone para WhatsApp

**User Story:** Como membro da equipe DOit, eu quero que o número de telefone seja formatado corretamente para o link do WhatsApp, para que o link funcione quando clicado pelo destinatário do e-mail.

#### Critérios de Aceitação

1. WHEN o número de telefone é inserido, THE Gerador_de_Assinatura SHALL gerar o href do WhatsApp removendo caracteres não numéricos e adicionando o prefixo "%2B55" para números brasileiros.
2. THE Gerador_de_Assinatura SHALL exibir o número de telefone no formato visual legível conforme digitado pelo usuário (ex: "(11) 91305-2222").
3. WHEN o número de telefone contém código de país explícito (iniciando com +), THE Gerador_de_Assinatura SHALL usar o código informado em vez de adicionar o prefixo padrão.
