# Processo de Construção do Projeto "Tem Leite Aí?"

Este documento detalha o processo de desenvolvimento do projeto "Tem Leite Aí?", uma plataforma para conectar doadores e receptores de leite materno. Aqui você encontrará informações sobre cada etapa do desenvolvimento, decisões técnicas, desafios enfrentados e soluções implementadas.

## 1. Definição da Estrutura e Requisitos

### Requisitos Iniciais
- Plataforma web para conectar doadores e receptores de leite materno
- Banco de dados SQLite para armazenamento de dados
- Cadastro separado para doadores e receptores
- Cálculo de distância entre usuários baseado em endereço
- Sistema de mensagens entre usuários
- Funcionalidade de reserva de doações

### Decisões Técnicas Iniciais
- **Framework Backend**: Flask (Python) pela simplicidade e flexibilidade
- **Banco de Dados**: SQLite pela facilidade de configuração e portabilidade
- **ORM**: SQLAlchemy para abstração do banco de dados
- **Frontend**: HTML, CSS, JavaScript com Bootstrap 5 para responsividade
- **Autenticação**: Flask-Login para gerenciamento de sessões
- **Geolocalização**: API OpenStreetMap (Nominatim) para conversão de endereços em coordenadas

## 2. Criação dos Modelos de Dados

### Modelos Implementados
- **User**: Armazena dados de usuários (doadores e receptores)
  - Campos: id, username, email, password, tipo, endereço, cidade, estado, cep, latitude, longitude
  - Relacionamentos: doações feitas, doações recebidas, mensagens enviadas, mensagens recebidas

- **Doacao**: Armazena dados de doações
  - Campos: id, doador_id, data_doacao, quantidade, disponivel, receptor_id
  - Relacionamentos: doador, receptor

- **Mensagem**: Armazena mensagens entre usuários
  - Campos: id, remetente_id, destinatario_id, conteudo, timestamp, lida
  - Relacionamentos: remetente, destinatario

### Considerações de Design
- Separação clara entre doadores e receptores através do campo "tipo"
- Rastreamento do status de disponibilidade das doações
- Sistema de mensagens com marcação de leitura
- Armazenamento de coordenadas geográficas para cálculo de distância

## 3. Configuração do Ambiente

### Estrutura de Diretórios
Criação da estrutura de diretórios seguindo as melhores práticas para aplicações Flask:
```
tem_leite_ai/
├── app/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── routes.py
├── instance/
└── run.py
```

### Desafios de Configuração
- **Compatibilidade Multiplataforma**: Garantir que o projeto funcione tanto em Windows quanto em Linux
- **Solução**: Uso de `os.path.join()` para criar caminhos compatíveis com qualquer sistema operacional

- **Criação da Pasta Instance**: Garantir que a pasta para o banco de dados SQLite exista
- **Solução**: Implementação de código para criar automaticamente a pasta instance se não existir

## 4. Implementação do Backend

### Autenticação e Cadastro
- Implementação do sistema de login com Flask-Login
- Criação de formulários de cadastro com validação
- Conversão de endereços em coordenadas geográficas usando a API Nominatim
- Separação de fluxos para doadores e receptores

### Cadastro e Listagem de Doações
- Implementação do formulário de cadastro de doações
- Validação de dados de entrada (quantidade > 0)
- Listagem de doações por doador
- Marcação de status (disponível/reservada)

### Cálculo de Distância
- Implementação da fórmula de Haversine para cálculo de distância entre coordenadas
- Filtro de doadores por proximidade (até 50km)
- Ordenação de resultados por distância

### Sistema de Mensagens
- Implementação de envio de mensagens entre usuários
- Criação de chat para visualização de conversas
- Sistema de marcação de mensagens como lidas
- Contagem de mensagens não lidas
- Mensagens contextualizadas sobre doações específicas

### Reserva de Doações
- Implementação do fluxo de reserva de doações
- Tela de confirmação antes da reserva
- Atualização de status da doação após reserva
- Envio automático de mensagem ao doador após reserva
- Redirecionamento para chat após reserva

## 5. Implementação do Frontend

### Templates HTML
- Criação de template base com estrutura comum
- Implementação de páginas específicas:
  - Página inicial
  - Login e cadastro
  - Dashboards para doador e receptor
  - Cadastro de doação
  - Busca de doadores
  - Confirmação de reserva
  - Envio de mensagens
  - Chat e caixa de entrada

### Estilos CSS
- **main.css**: Estilos globais, layout, cores e tipografia
- **animations.css**: Animações, transições e efeitos visuais
- **components.css**: Estilos específicos para componentes da interface

### JavaScript
- **main.js**: Funcionalidades principais e inicialização
- **validation.js**: Validação de formulários e feedback ao usuário
- **utils.js**: Utilitários para melhorar a experiência do usuário

### Características da Interface
- Design responsivo para desktop e dispositivos móveis
- Animações suaves para melhorar a experiência do usuário
- Feedback visual para ações do usuário
- Validação de formulários em tempo real
- Confirmação para ações importantes
- Indicadores de carregamento para operações assíncronas

## 6. Desafios e Soluções

### Desafio: Importação de Configurações
**Problema**: Erro ao importar o arquivo config.py em diferentes ambientes
**Solução**: Implementação de configuração direta no arquivo __init__.py, eliminando a dependência de importação externa

### Desafio: Registro de Rotas
**Problema**: Erro ao tentar importar função register_routes inexistente
**Solução**: Ajuste do código para usar a função init_routes existente no arquivo routes.py

### Desafio: Acesso ao Banco de Dados
**Problema**: Erro "unable to open database file" em ambiente Windows
**Solução**: Criação explícita da pasta instance e uso de caminhos absolutos para o banco de dados

### Desafio: Templates Não Encontrados
**Problema**: Erro TemplateNotFound ao tentar renderizar páginas
**Solução**: Criação e organização correta de todos os templates na pasta templates

### Desafio: Rotas Inconsistentes
**Problema**: BuildError ao tentar acessar rotas não definidas
**Solução**: Implementação das rotas faltantes (enviar_mensagem_doacao, confirmar_reserva) e ajuste dos templates correspondentes

## 7. Testes e Validação

### Fluxos Testados
- Cadastro e autenticação de usuários
- Cadastro e listagem de doações
- Busca de doadores por proximidade
- Envio e recebimento de mensagens
- Reserva de doações

### Validação de Usabilidade
- Verificação de responsividade em diferentes dispositivos
- Teste de feedback visual para ações do usuário
- Validação de formulários em tempo real
- Confirmação para ações importantes

## 8. Documentação

### Documentação Técnica
- README.md com instruções detalhadas
- Documentação de código com comentários explicativos
- Descrição da estrutura do projeto
- Instruções de instalação e execução

### Documentação de Usuário
- Descrição dos fluxos de usuário
- Explicação das funcionalidades
- Guia de uso do sistema

## 9. Considerações Finais

### Melhorias Futuras
- Implementação de hashing de senhas
- Adição de sistema de avaliação pós-doação
- Implementação de notificações em tempo real
- Adição de filtros adicionais na busca
- Implementação de perfil de usuário com foto
- Adição de sistema de moderação de conteúdo
- Implementação de testes automatizados
- Otimização de performance para grandes volumes de dados

### Lições Aprendidas
- Importância da compatibilidade multiplataforma
- Necessidade de tratamento robusto de erros
- Valor de uma estrutura de projeto bem organizada
- Benefícios de um design responsivo e intuitivo

---

Este documento representa o processo completo de construção do projeto "Tem Leite Aí?", desde a concepção até a implementação final. O projeto foi desenvolvido com foco na usabilidade, segurança e eficiência, visando conectar doadores e receptores de leite materno de forma simples e eficaz.
# tem-leite-ai-v2
