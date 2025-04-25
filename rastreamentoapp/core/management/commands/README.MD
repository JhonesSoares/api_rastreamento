Remover registros da tabela Location com mais de 30 dias, automaticamente todos os dias.

Testes:
terminal: python manage.py clean_old_locations

Se houver dados antigos, ele irá deletar e mostrar:
terminal: [sucesso] 42 localizações antigas removidas.


AMBIENTE DE PRODUÇÃO (Linux - Ubuntu, VPS, etc.)
Usar o crontab do Linux

1. Acesse o terminal do servidor com o ambiente ativado.

2. Edite o crontab:
    terminal: crontab -e

3. Adicione a linha:
    terminal:  0 3 * * * /home/usuario/seu_projeto/venv/bin/python /home/usuario/seu_projeto/manage.py clean_old_locations >> /home/usuario/seu_projeto/cron_clean.log 2>&1



🧪 Ambiente de Desenvolvimento (Windows)
✅ Opção 1: Agendar com o Agendador de Tarefas do Windows
Abra o Agendador de Tarefas (Task Scheduler):

No menu Iniciar, digite "Agendador de Tarefas" e abra.

Crie uma nova tarefa básica:

No menu à direita, clique em "Criar Tarefa Básica..."

Dê um nome, como LimparLocalizacoesVelhas.

Defina a frequência:

Ex: Diariamente, às 3h da manhã.

Escolha a ação:

Selecione "Iniciar um programa"

Configure o Python + manage.py:

Programa/script: caminho completo para o Python do seu ambiente virtual.

Exemplo:

    C:\Users\SeuUsuario\meuprojeto\venv\Scripts\python.exe

Argumentos:

    manage.py clean_old_locations

Iniciar em (muito importante): caminho da pasta do seu projeto Django.

    C:\Users\SeuUsuario\meuprojeto

Salve e teste:

    Você pode clicar com o botão direito na tarefa → Executar para testar.