
# Introdução ao pgAgent

O **pgAgent** é um agendador de tarefas para o **PostgreSQL**, utilizado para automatizar rotinas como backups, execuções de scripts SQL ou tarefas de manutenção. Ele faz parte do projeto **pgAdmin** e permite o gerenciamento de tarefas diretamente pelo banco de dados, com suporte a tarefas recorrentes e execução condicional.

O pgAgent funciona como um serviço, conectando-se ao PostgreSQL para obter e executar tarefas agendadas armazenadas em tabelas específicas no banco.

No contexto do projeto Marventura, o **pgAgent** será utilizado para executar automaticamente, a cada minuto, as funções responsáveis por reviver inimigos (lacaios e chefes) no jogo que tiverem ultrapassado o intervalo de tempo destinado ao seu renascimento (5 minutos para lacaios e 15 minutos para chefes). A escolha pelo **pgAgent**, em vez do **pg_cron** adotado anteriormente, se deve à sua maior compatibilidade com o sistema operacional Windows, o que facilita a execução do agendador em ambientes de desenvolvimento que utilizam essa plataforma. Além disso, o **pgAgent** mantém suporte completo para Linux, garantindo portabilidade e flexibilidade entre diferentes sistemas operacionais durante o desenvolvimento e a implantação.

---

## Instalação no Linux

### Pré-requisitos
- PostgreSQL instalado e configurado
- pgAdmin (opcional, para gerenciar graficamente)
- Superusuário ou permissão de root

### Passos

1. **Instale o pgAgent via gerenciador de pacotes** (exemplo para Debian/Ubuntu):

   ```bash
   sudo apt update
   sudo apt install pgagent
   ```

## Instalação no Windows

### Pré-requisitos
- PostgreSQL instalado
- pgAdmin instalado
- Conta com permissões de administrador

### Passos

1. **Baixe o instalador do pgAgent**:

   - Acesse: https://www.pgadmin.org/download/pgagent/

2. **Execute o instalador** e siga os passos fornecendo:
   - Host do banco PostgreSQL
   - Nome do banco onde o pgAgent será configurado
   - Usuário e senha com permissões para criar extensões



## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Israel Thalles](https://github.com/IsraelThalles) | 15/07/2025 |  |  |
