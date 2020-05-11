>**IMPORTANTE**
>
>Como lembrete, se não houver informações sobre a atualização, isso significa que se trata apenas da atualização da documentação, tradução ou texto

# 07/07/2019

- Corrigido um erro ao parar o daemon
- Correções de bugs
- ESTA ATUALIZAÇÃO PRECISA RECOMPILAR AS DEPENDÊNCIAS (REINICIAR)

# 2019-09-19

- Exibir correção de bug

# 09-10-2019

- Corrigido um problema com a exibição da tabela de roteamento

# 09-09-2019
- Adaptando Dependências para o Debian10 Buster
- Modificação que permite separar as saídas do implante inteligente (esta função requer uma recompilação de dependências)

2019-02-04
===
- ESTA ATUALIZAÇÃO PRECISA RECOMPILAR AS DEPENDÊNCIAS (REINICIAR)
- Correção de um bug em várias instâncias de termostatos
- Criação de um nível de fila descontinuado em ações para atualizações
- Adição de muitas confs (como lembrete, o botão para recuperar confs é útil para estar atualizado sem atualizar o plugin)
- Gerenciamento aprimorado de multicanais encapsulados
- Adição de CC específico do fabricante
- Instalação simples do CC Soundswitch
- Correção para inclusão múltipla de dispositivos <
- Binário de switch CC aprimorado
- A inserção de parâmetros manuais é sempre possível
- Realce da cauda
- Preparação para adicionar novos CCs (notificação em particular)
- Adição de códigos no alarme CC do teclado Zipato no momento
- Correção do philio no modo seguro, que durante os toques gerou um tempo limite de 10 segundos (é certamente necessário regenerar a detecção da sirene ou incluí-la novamente)
- Correção de um erro se o nível de log for nenhum
- ESTA ATUALIZAÇÃO PRECISA RECOMPENSAR AS DEPENDÊNCIAS

17/03/2018
===

- Alteração da ramificação para recuperação de confs durante o syncconf (após uma alteração na organização dos githubs)

2018-01-17 / 2018-01-19
===

-   Novidades

    -   Retorno da possibilidade de sincronizar confs sem atualizar o plugin

    -   Melhorias

    -   Adição da possibilidade interna de acionar atualizações em determinados valores e módulos específicos (usados em jeedom confs)

    -   Redesign completo da função, permitindo simular um valor em outro comando para evitar colocá-lo em um conjunto de módulos, mas especificamente (Jeedom interno)

-   Fixed bug

    -   Corrigido um erro que fazia com que as confs geradas automaticamente estivessem no formato antigo e, portanto, inutilizáveis

    -   Correção do erro da perda do ponto de ajuste pendente nas válvulas termostáticas (acompanha o ponto 2 das melhorias)

    -   Redução do tamanho das imagens para limitar ao máximo o tamanho do plug-in (aproximadamente 500 imagens)

    -   Remoção de dependências mais usadas, como Mercurial Sphinx etc

    -   Supressão da eliminação das configurações antes da atualização (evita que os ícones do Zwave substituam as imagens no caso de atualizações sem êxito por tempo limite ou outro)

2017-08-xx
===


-   Novos recursos

    -   Possibilidade de atualizar pedidos de equipamentos sem
        excluir os existentes.

    -   Possibilidade de criar um comando de informação sobre os valores de
        Guia Sistema.

-   Melhorias / Aprimoramentos

    -   Suporte para novos módulos, definições ozw
        e pedidos.

    -   Capacidade de selecionar a associação padrão
        (sem exemplo) nos módulos que suportam o
        associações de várias instâncias.

    -   Verificação da validade dos grupos de associação no final
        da entrevista.

    -   Recuperação do último nível das baterias quando o daemon inicia.

-   Fixed bug

    -   Correção da migração das informações da bateria.

    -   Correção do feedback das informações da bateria em
        a tela de equipamentos.

    -   Restauração do tipo de bateria nas configurações
        de módulos.

    -   Correção de ações nos valores de tipo de botão em
        tela do módulo.

    -   Correção da recuperação de traduções de parâmetros.

    -   Correção de erro vazio na modificação dos valores do tipo RAW
        (Código RFid).

    -   Exibição fixa de valores pendentes
        a ser aplicado.

    -   Supressão da notificação de mudança de valor antes
        que não é aplicado.

    -   Não exibirá mais o cadeado na tela do módulo se o módulo
        não suporta a classe de comando de segurança.

    -   Aplicação de atualização manual em
        configurações recomendadas.

    -   Assistente de gerenciamento de emblemas para leitores RFID.

    -   Correção do assistente de detecção de módulos desconhecidos.

    -   Correção dos assistentes de "Continuar a partir de .." e "Aplicar
        on ... "na guia configurações.

20/06/2017
===

-   Novos recursos

    -   N / A

-   Melhorias / Aprimoramentos

    -   Adicione todas as configurações do módulo ao
        novo formato.

-   Fixed bug

    -   Não teste se um nodeId existe durante a exclusão
        de uma associação.

    -   Restaurando a notificação de depósito pendente em
        termostatos.

    -   Enviando cena de ativação pendente 1.

    -   Não exibe mais o cadeado na tela de integridade no
        módulos que não suportam a classe de comando de segurança.

    -   Repetição do valor nos controles remotos antes do final de
        a entrevista (kyefob, minimote).

    -   Modifique um parâmetro da lista de tipos por valor através de um
        Comando de ação.

    -   Modifique um parâmetro em um módulo sem configuração definida.

13/06/2017
===

-   Novos recursos

    -   N / A

-   Melhorias / Aprimoramentos

    -   Adição da configuração do módulo Fibaro US

-   Fixed bug

    -   N / A

31-05-2017
===

-   Novos recursos

    -   N / A

-   Melhorias / Aprimoramentos

    -   N / A

-   Fixed bug

    -   Correção da atribuição de valores no formato RAW de códigos
        para leitor RFid.

23-05-2017
===

-   Novos recursos

    -   Remoção do modo mestre / escravo. Substituído pelo plugin
        link jeedom.

    -   Uso de uma chave de API privada no plug-in ZWave.

    -   Novo formato dos arquivos de configuração no mapeamento de
        ordem com jeedom.

    -   Conversão automática de pedidos existentes para novos
        formato ao instalar o plug-in.

    -   Adicionado suporte para a Central Scene Command Class.

    -   Adicionado suporte à classe de comando do operador de barreira.

-   Melhorias / Aprimoramentos

    -   Revisão completa do servidor REST usando TORNADO.

        -   Modificação de todas as estradas existentes,
            scripts precisarão ser adaptados se você usar a API do ZWave.

        -   Reforço da segurança, apenas as chamadas são ouvidas em
            o servidor REST.

        -   Usando a chave da API ZWave necessária para iniciar
            Solicitações REST.

    -   Desativando testes de saúde (temporários).

    -   Desativação (temporária) do mecanismo de atualização
        configurações do módulo.

    -   Desativação da função Heal Network automaticamente
        duas vezes por semana (diminuição das trocas com
        o controlador).

    -   Otimizações de código de biblioteca Openzwave.

        -   O Fibaro FGK101 não precisa mais completar a entrevista para anunciar
            uma mudança de estado.

        -   O comando do botão de liberação (Parada do obturador) não força mais
            atualizando todos os valores do módulo
            (diminuição na fila de mensagens).

        -   Possibilidade de notificar valores na classe de
            Comando de alarme (seleção de toque nas sirenes)

    -   Maior demanda diária por nível de bateria (menos de
        mensagens, economizando baterias).

    -   O nível da bateria é enviado diretamente para a tela da bateria no
        relatório de nível de recebimento.

-   Fixed bug

    -   Atualização de todas as instâncias após um
        Transmissão CC ALL ALL.

26/08/2016
===

-   Novos recursos

    -   Aucune

-   Melhorias / Aprimoramentos

    -   Detecção RPI3 na atualização de dependência.

    -   Ativar o modo de inclusão não seguro padrão.

-   Fixed bug

    -   As informações do fabricante do teste na tela de integridade não
        não mais NOK.

    -   Perda de caixas de seleção na guia Comandos do
        página de equipamento.

17/08/2016
===

-   Novos recursos

    -   Relançamento do demônio se a detecção do controlador expirar durante
        inicialização do controlador.

-   Melhorias / Aprimoramentos

    -   Atualização da biblioteca do OpenZWave 1.4.2088.

    -   Correção ortográfica.

    -   Redesign da tela do equipamento com abas.

-   Fixed bug

    -   Problema ao exibir determinados módulos na tabela de roteamento
        e gráfico de rede.

    -   Módulos Vision Secure que não retornam ao modo de espera
        durante a entrevista.

    -   Instalação de dependências em loop (problema no lado do github).

11/07/2016
===

-   Novos recursos

    -   Suporte para restauração do último nível conhecido em
        ofuscá-los.

    -   Distinção dos módulos FLiRS na tela de integridade.

    -   Pedido adicionado para atualizar rotas de retorno
        para o controlador.

    -   Assistente para aplicar os parâmetros de configuração de um
        módulo para vários outros módulos.

    -   Identificação dos módulos de suporte Zwave +
        COMANDO\_CLASS\_ZWAVE\_PLUS\_INFO.

    -   Exibição do status de segurança dos módulos que suportam
        COMANDO\_CLASS\_SECURITY.

    -   Adição da possibilidade de selecionar a instância 0 do
        controlador para associações de várias instâncias.

    -   Protegendo todas as chamadas para o servidor REST.

    -   Detecção automática de dongles, na página de configuração
        plugin.

    -   Diálogo de inclusão com opção de modo de inclusão para
        simplifique a inclusão segura.

    -   Tendo em conta o equipamento desativado dentro do
        Motor Z-Wave.

        -   Tela cinza na tela de integridade sem análise na
            o nó.

        -   Oculto na tabela de rede e no gráfico de rede.

        -   Nós desativados, excluir testes de integridade.

-   Melhorias / Aprimoramentos

    -   Otimização de controles sanitários.

    -   Otimização de gráficos de rede.

    -   Detecção aprimorada do controlador principal para
        teste de grupo.

    -   Atualização para a biblioteca OpenZWave 1.4.296.

    -   Otimização do resfriamento em segundo plano das unidades.

    -   Atualização de plano de fundo otimizada para
        os motores.

    -   Adaptação para o Jeedom core 2.3

    -   Tela de integridade, modificação do nome da coluna e aviso
        no caso de não comunicação com um módulo.

    -   Otimização do servidor REST.

    -   Correção da ortografia das telas, obrigado @ Juan-Pedro
        aka: kiko.

    -   Atualizando a documentação do plug-in.

-   Fixed bug

    -   Correção de possíveis problemas ao atualizar
        configurações do módulo.

    -   Gráfico de rede, cálculo de saltos no ID do controlador
        principal e não assumir ID 1.

    -   Gerenciamento do botão adicionar uma associação de grupo.

    -   Exibição de valores falsos na guia Configuração.

    -   Não assuma mais a data atual do estado das baterias se não for recebida
        relatório de equipamentos.

30/05/2016
===

-   Novos recursos

    -   Adicionada opção para ativar / desativar controles
        sanitário em todos os módulos.

    -   Adicionando uma guia Notificações para visualizar os últimos 25
        notificações do controlador.

    -   Adicionando uma rota para recuperar a integridade de um nó.
        ip\_jeedom:8083 / ZWaveAPI / Run / devices \ [node\_id \]. GetHealth ()

    -   Adicionando uma rota para recuperar a última notificação
        de um nó.
        ip\_jeedom:8083 / ZWaveAPI / Run / devices \ [node\_id \]. GetLastNotification ()

-   Melhorias / Aprimoramentos

    -   Permite a seleção de módulos FLiRS durante
        associações diretas.

    -   Permitir a seleção de todas as instâncias de módulos durante
        associações diretas.

    -   Atualização do wrapper python OpenZWave para a versão 0.3.0.

    -   Atualização da biblioteca do OpenZWave 1.4.248.

    -   Não exiba um aviso de ativação expirada para
        módulos alimentados por bateria.

    -   Validação de que um módulo é idêntico no nível de IDs para
        permite copiar parâmetros.

    -   Simplificação do assistente para copiar parâmetros.

    -   Ocultar valores de guia do sistema não ocorrentes
        para ser exibido.

    -   Exibição da descrição dos recursos do controlador.

    -   Atualização da documentação.

    -   Correção da ortografia da documentação, obrigado
        @Juan-Pedro aka: kiko.

-   Fixed bug

    -   Correção ortográfica.

    -   Inclusão corrigida no modo seguro.

    -   Correção de chamada assíncrona. (error: \ [Erro 32 \]
        Tubo quebrado)

04/05/2016
===

-   Novos recursos

    -   Adicionada opção para desativar a atualização em segundo plano
        dimmers.

    -   Exibição de associações às quais um módulo está associado
        (encontrar uso).

    -   Adicionado suporte para CC MULTI\_INSTANCE\_ASSOCIATION.

    -   Adicionando uma notificação info ao aplicar
        Defina\_Point para usar o ponto de ajuste solicitado em
        cmd formulário de informações.

    -   Incluindo um Assistente de Configuração Recomendado.

    -   Adicionar opção para ativar / desativar o assistente
        configuração recomendada ao incluir
        novos módulos.

    -   Adicionar opção para ativar / desativar a atualização de
        configurações do módulo a cada noite.

    -   Adição de uma rota para gerenciar várias instâncias de associação.

    -   Adicionar estágio de consulta ausente.

    -   Adicionada validação da seleção do Dongle USB ao
        começando o demônio.

    -   Adição de validação e teste de retorno de chamada na inicialização
        do demônio.

    -   Adicionada opção para desativar a atualização automática
        configuração do módulo.

    -   Incluindo uma Rota para Modificar os Rastreios de Log em Tempo de Execução
        o servidor REST. Note: nenhum efeito no nível do OpenZWave.
        <http://ip_jeedom:8083/ZWaveAPI/Run/ChangeLogLevel(level>) level
        ⇒ 40:Erro, 20: Informações sobre depuração 10

-   Melhorias / Aprimoramentos

    -   Atualização do wrapper python OpenZWave para a versão 0.3.0b9.

    -   Destacando grupos de associações pendentes
        a ser aplicado.

    -   Atualização para a biblioteca OpenZWave 1.4.167.

    -   Modificação do sistema de associação direta.

    -   Atualização da documentação

    -   Capacidade de iniciar a regeneração da detecção de nó
        para todos os módulos idênticos (marca e modelo).

    -   Exibido na tela de integridade se itens de configuração
        não são aplicados.

    -   Exibido na tela do equipamento se elementos de
        configuração não é aplicada.

    -   É exibido na tela de funcionamento se um módulo de bateria não tiver
        nunca acordei.

    -   Exibido na tela de integridade se um módulo de bateria excedeu
        a hora de despertar prevista.

    -   Adicionando rastreamentos após erro de notificação.

    -   Melhor recuperação do status da bateria.

    -   Resumo / conformidade de integridade dos termostatos da bateria.

    -   Melhor detecção de módulos nas baterias.

    -   Otimização do modo de depuração para o servidor REST.

    -   Forçar uma atualização do estado do comutador e um dímero
        após o envio de um comando switch all.

-   Fixed bug

    -   Corrigida descoberta de grupos de associação.

    -   Correção do erro "Exceção KeyError: (91) em
        'libopenzwave.notif\_callback 'ignorado".

    -   Correção da seleção da documentação do módulo para
        módulos com vários perfis.

    -   Gerenciamento dos botões de ação do módulo.

    -   Correção da descrição do nome genérico da classe.

    -   Correção do backup do arquivo zwcfg.

01/03/2016
===

-   Novos recursos

    -   Adicionando o botão Configuração através da tela de gerenciamento
        equipamento.

    -   Adição de novos estados de entrevista do módulo.

    -   Editando rótulos nas UIs.

-   Melhorias / Aprimoramentos

    -   Melhor gerenciamento dos botões de ações do módulo.

    -   Documentação Adicionando seções.

    -   Otimização do mecanismo de detecção de estado do daemon.

    -   Mecanismo de protesto durante a recuperação do
        descrição dos parâmetros se ele contiver caracteres
        inválido.

    -   Nunca volte para as informações de status da bateria em um
        módulo conectado à rede.

    -   Atualização da documentação.

-   Fixed bug

    -   Ortografia e correções gramaticais.

    -   Validação do conteúdo do arquivo zwcfg antes de aplicá-lo.

    -   Correção da instalação.

12/02/2016
===

-   Melhorias / Aprimoramentos

    -   Nenhum alerta de nó morto se estiver desativado.

-   Fixed bug

    -   Correção do retorno do status do fio piloto Fibaro.

    -   Correção de um bug que recria os comandos durante a configuração
        atualizado.

2016.02.09
===

-   Novos recursos

    -   A adição de notificação por push no nó\_event case, permite
        implementação de uma informação de cmd no CC 0x20 para recuperar
        evento em nós.

    -   Adicionada rota ForceRefresh
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ForceRefresh()
        pode ser usado em pedidos.

    -   Adicionando a rota SwitchAll
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[1\].commandClasses\[0xF0\].SwitchAll(&lt;int:state&gt;)
        disponível através do controlador principal.

    -   Adicionando a rota ToggleSwitch
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ToggleSwitch()
        pode ser usado em pedidos.

    -   Adição de uma notificação por push em caso de nó morto presumido.

    -   Ajout de la commande “refresh all parameters” dans
        a guia Configurações.

    -   Adição da informação do parâmetro aguardando para ser aplicada.

    -   Adicionando notificação de rede.

    -   Adição de uma legenda no gráfico de rede.

    -   Adição da função de cuidado de rede através da tabela de roteamento.

    -   Remoção automática de nó fantasma com apenas um clique.

    -   Gerenciamento de ações no nó de acordo com o estado do nó e o tipo.

    -   Gerenciamento de ações de rede de acordo com o status da rede.

    -   Atualização da configuração automática do módulo
        as noites.

-   Melhorias / Aprimoramentos

    -   Refatoração completa do código do servidor REST, otimização de
        velocidade inicial, legibilidade, conformidade com a convenção
        nomeação.

    -   Troncos quadrados.

    -   Simplificação do gerenciamento manual de atualização de 5 minutos com
        possibilidade de aplicação em nós de baterias.

    -   Atualização da biblioteca OpenZWave na 1.4

    -   Modificação do teste de saúde para reviver os nós presumidos
        morto mais facilmente sem ações do usuário.

    -   Uso de cores brilhantes na tabela de roteamento e
        gráfico de rede.

    -   Padronização das cores da tabela de roteamento e do
        gráfico de rede.

    -   Otimização das informações na página de integridade do Z-Wave de acordo com
        o estado da entrevista.

    -   Melhor gerenciamento dos parâmetros somente leitura ou gravação
        somente na guia Configurações.

    -   Aviso aprimorado nos termostatos da bateria.

-   Fixed bug

    -   A temperatura convertida em Celsius retorna a unidade C
        de F.

    -   Correção da atualização de valores na inicialização.

    -   Correção da atualização por valor na guia Valores.

    -   Correção de nomes genéricos de módulo.

    -   Correção do ping nos nós no Timeout durante o
        teste de saúde.
