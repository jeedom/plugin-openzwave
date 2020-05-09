Description
===========

Este plugin permite a exploração de módulos Z-Wave através de
a biblioteca do OpenZwave.

Introduction
============

O Z-Wave se comunica usando a tecnologia de rádio de baixa potência na faixa de frequência de 868,42 MHz. Foi projetado especificamente para aplicações de automação residencial. O protocolo de rádio Z-Wave é otimizado para trocas de baixa largura de banda (entre 9 e 40 kbit / s) entre dispositivos com bateria ou alimentados por rede elétrica.

O Z-Wave opera na faixa de frequência sub-gigahertz, dependendo da
regiões (868 MHz na Europa, 908 MHz nos EUA e outras frequências
de acordo com as bandas ISM das regiões). O alcance teórico é aproximadamente
30 metros em ambientes fechados e 100 metros em ambientes externos. A rede Z-Wave
usa tecnologia de malha para aumentar o alcance e
confiabilidade. O Z-Wave foi projetado para ser facilmente integrado ao
produtos eletrônicos de baixo consumo, incluindo
baterias como controles remotos, detectores de fumaça e
Segurança.

O Z-Wave + traz algumas melhorias, incluindo um melhor alcance e
melhora a vida da bateria, entre outras coisas. O
total compatibilidade com o Z-Wave.

Distâncias a serem respeitadas com outras fontes de sinais sem fio
-----------------------------------------------------------------

Os receptores de rádio devem estar posicionados a uma distância mínima de
50 cm de outras fontes de rádio.

Exemplos de fontes de rádio:

-   Ordinateurs

-   Aparelhos de microondas

-   Transformadores eletrônicos

-   equipamento de áudio e vídeo

-   Dispositivos de pré-acoplamento para lâmpadas fluorescentes

> **Tip**
>
> Se você possui um controlador USB (Z-Stick), é recomendável
> afaste-o da caixa usando um simples cabo de extensão USB de 1M por
> Exemplo.

A distância entre outros transmissores sem fio, como telefones
As transmissões de áudio sem fio ou rádio devem ter pelo menos 3 metros. O
as seguintes fontes de rádio devem ser consideradas :

-   Interferência por interruptor de motores elétricos
-   Interferência de dispositivos elétricos defeituosos
-   Interferência do equipamento de solda HF
-   dispositivos de tratamento médico

Espessura eficaz da parede
---------------------------

Os locais dos módulos devem ser escolhidos de forma que
a linha de conexão direta funciona apenas em um curto espaço de tempo
distância através do material (uma parede), a fim de evitar o máximo possível
mitigações.

![introduction01](../images/introduction01.png)

Peças de metal do edifício ou móveis podem bloquear
ondas eletromagnéticas.

Malha e roteamento
-------------------

Os nós Z-Wave principais podem transmitir e repetir mensagens
que não estão dentro do alcance direto do controlador. Isso permite uma
grande flexibilidade de comunicação, mesmo se não houver conexão
sem fio direto ou se uma conexão estiver temporariamente indisponível, para
por causa de uma mudança na sala ou no prédio.

![introduction02](../images/introduction02.png)

O controlador **Id 1** pode se comunicar diretamente com os nós 2, 3
e 4. O nó 6 está fora de seu alcance de rádio, no entanto, é
encontrado na área de cobertura de rádio do nó 2. Portanto, o
o controlador pode se comunicar com o nó 6 via nó 2. Disso
Dessa forma, o caminho do controlador através do nó 2 até o nó 6 é chamado
estrada. No caso em que a comunicação direta entre o nó 1 e o nó
nó 2 está bloqueado, existe ainda outra opção para se comunicar com
nó 6, usando o nó 3 como outro repetidor de sinal.

Torna-se óbvio que quanto mais nós do setor você tiver, mais o
as opções de roteamento aumentam e mais estabilidade da rede aumenta.
O protocolo Z-Wave é capaz de rotear mensagens por
através de um máximo de quatro nós repetidos. É um
compromisso entre tamanho da rede, estabilidade e duração máxima
de uma mensagem.

> **Tip**
>
> É altamente recomendável no início da instalação ter uma relação
> entre nós do setor e nó em 2/3 baterias, para ter uma boa
> malha de rede. Favorecer os micromódulos sobre os plugues inteligentes. O
> micródulos estarão em um local final e não serão
> desconectados, eles também geralmente têm um alcance melhor. Uma boa
> partida é a iluminação das áreas comuns. Vai ajudar bem
> distribua os módulos do setor em locais estratégicos em seu
> casa. Então você pode adicionar quantos módulos na pilha
> conforme desejado, se suas rotas básicas forem boas.

> **Tip**
>
> O **Gráfico de rede** bem como o **Tabela de roteamento**
> permitem visualizar a qualidade da sua rede.

> **Tip**
>
> Existem módulos repetidores para preencher áreas onde nenhum módulo
> setor não tem utilidade.

Propriedades dos dispositivos Z-Wave
-------------------------------

|  | Vizinhos | Estrada | Funções possíveis |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controlador | Conhece todos os vizinhos | Tem acesso à tabela de roteamento completa | Pode se comunicar com todos os dispositivos da rede, se houver um canal |
| Escravo | Conhece todos os vizinhos | Não possui informações na tabela de roteamento | Não é possível responder ao nó que recebeu a mensagem. Portanto, não é possível enviar mensagens não solicitadas |
| Escravos de roteamento | Conhece todos os seus vizinhos | Com conhecimento parcial da tabela de roteamento | Pode responder ao nó do qual recebeu a mensagem e pode enviar mensagens não solicitadas para vários nós |

Em resumo:

-   Cada dispositivo Z-Wave pode receber e confirmar o recebimento de
    messages

-   Os controladores podem enviar mensagens para todos os nós no
    réseau, sollicités onde non « O maître peut parler quand il veut e à
    quem ele quer »

-   Escravos não podem enviar mensagens não solicitadas,
    mais seulement une réponse aux demande «L'esclave ne parle que si
    pedimos a ele »

-   Os escravos de roteamento podem responder a solicitações e são
    permissão para enviar mensagens não solicitadas a certos nós que
    le Controlador a prédéfini « L'esclave é toujours un esclave, mais
    com autorização, ele pode falar »

Configuração do plugin
=======================

Depois de baixar o plugin, você só precisa ativá-lo e
configurer.

![Configuração01](../images/configuration01.png)

Uma vez ativado, o demônio deve lançar. O plug-in está pré-configurado
com valores padrão; você normalmente não tem mais nada a fazer.
No entanto, você pode alterar a configuração.

Dependências
-----------

Esta parte permite validar e instalar as dependências necessárias
o bom funcionamento do plug-in Zwave (localmente e
deportados, aqui localmente) ![configuration02](../images/configuration02.png)

-   Estatuto **OK** confirma que as dependências foram atendidas.

-   Se o status for **NOK**, dependências terão que ser reinstaladas
    usando o botão ![configuration03](../images/configuration03.png)

> **Tip**
>
> A atualização de dependências pode levar mais de 20 minutos, dependendo da
> seu material. O progresso é exibido em tempo real e um log
> **Openzwave\_update** está acessível.

> **Important**
>
> A atualização de dependências normalmente deve ser feita apenas
> Se o status for **NOK**, mas, no entanto, é possível ajustar
> certos problemas, a serem solicitados a refazer a instalação do
> Dependências.

> **Tip**
>
> Se você estiver no modo remoto, as dependências do daemon local podem
> ser NOK, é completamente normal.

Demônio
-----

Esta parte permite que você valide o estado atual do (s) demônio (s) e
configurar o gerenciamento automático desses.
![Configuração04](../images/configuration04.png) O démon local et
todos os demônios deportados serão exibidos com seus diferentes
informations

-   O **Statut** indica que o demônio está atualmente em execução.

-   O **Configuration** indica se a configuração do daemon
    é válido.

-   O botão **(Re) iniciar** permite forçar o reinício do
    plugin, no modo normal ou inicie-o pela primeira vez.

-   O botão **Preso**, visível apenas se o gerenciamento automático
    está desativado, força o demônio a parar.

-   O **Gerenciamento automático** permite que o Jeedom seja iniciado automaticamente
    o demônio quando Jeedom começa, bem como para reiniciá-lo no caso
    de problema.

-   O **último lançamento** é como o nome sugere a data de
    último lançamento conhecido do demônio.

Log
---

Esta parte permite escolher o nível do log e consultá-lo.
o conteúdo.

![Configuração05](../images/configuration05.png)

Selecione o nível e salve; o daemon será reiniciado
com instruções e rastreios selecionados.

O nível **Debug** onde **Info** pode ser útil para entender
por que o demônio planta ou não aumenta um valor.

> **Important**
>
> No modo **Debug** o demônio é muito detalhado, é recomendado
> use este modo somente se precisar diagnosticar um problema
> particular. Não é recomendado deixar o demônio correr enquanto
> **Debug** permanentemente, se usarmos um **SD-Card**. Uma vez que o
> depurar, não se esqueça de retornar a um nível inferior
> alto como o nível **Error** que só volta ao possível
> erros.

Configuration
-------------

Esta parte permite que você configure os parâmetros gerais do plugin
![Configuração06](../images/configuration06.png)

-   **Geral** :

    -   **Excluir automaticamente dispositivos excluídos** :
        A opção Sim permite excluir os dispositivos excluídos do
        Rede Z-Wave. A opção Não permite manter o equipamento
        no Jeedom, mesmo que tenham sido excluídos da rede. O equipamento
        terá que ser excluído ou reutilizado manualmente nele
        atribuindo um novo ID do Z-Wave se você estiver migrando o
        controlador de chumbo.

    -   **Aplique o conjunto de configurações recomendado para inclusão** :
        opção para aplicar o conjunto de
        configuração recomendada pela equipe Jeedom (recomendado)

    -   **Desativar a atualização em segundo plano das unidades** :
        Não solicite uma atualização das unidades
        em segundo plano.

    -   **Ciclo (s)** : permite definir a frequência dos elevadores
        na Jeedom.

    -   **Porta de chave Z-Wave** : a porta USB na qual sua interface
        O Z-Wave está conectado. Se você usa o Razberry, você tem,
        dependendo da sua arquitetura (RPI ou Jeedomboard), os 2
        possibilidades no final da lista.

    -   **Porta do servidor** (modificação perigosa, deve ter o mesmo
        valor em todos os Jeedoms remotos Z-Wave) : deixa
        modificar a porta de comunicação interna do daemon.

    -   **Backups** : permite gerenciar backups do arquivo
        topologia de rede (veja abaixo)

    -   **Módulos de configuração** : permite recuperar, manualmente,
        Arquivos de configuração do OpenZWave com parâmetros para
        módulos, bem como definir comandos do módulo para
        seus usos.

        > **Tip**
        >
        > As configurações do módulo são recuperadas
        > automaticamente todas as noites.

        > **Tip**
        >
        > Reiniciando o daemon após atualizar o
        > configurações do módulo é desnecessário.

        > **Important**
        >
        > Se você possui um módulo não reconhecido e uma atualização do
        > configuração acabou de ser aplicada, você pode manualmente
        > comece a recuperar as configurações do módulo.

Uma vez recuperadas as configurações, serão necessárias de acordo com as alterações
trouxe:

-   Para um novo módulo sem configuração ou controle : excluir e
    inclua novamente o módulo.

-   Para um módulo para o qual apenas os parâmetros foram atualizados :
    inicie a regeneração da detecção de nó, através da guia Actions
    do módulo (o plugin deve reiniciar).

-   Pour un módulo dont le « mapping » de ordems a été corrigé : la
    lupa nos controles, veja abaixo.

    > **Tip**
    >
    > Em caso de dúvida, é recomendável excluir e incluir novamente o módulo.

Não esqueça de ![configuration08](../images/configuration08.png) si
você faz uma mudança.

> **Important**
>
> Se você estiver usando o Ubuntu : Para que o demônio funcione, você deve
> absolutamente tem ubuntu 15.04 (versões inferiores têm um bug e
> o demônio não pode começar). Tenha cuidado se você fizer uma aposta
> atualizado a partir de 14.04 leva uma vez em 15.04 relançamento
> instalação de dependências.

> **Important**
>
> Selecionando a porta de chave Z-Wave no modo de detecção automática,
> **Auto**, só funciona para dongles USB.

Painel Móvel
-------------

![Configuração09](../images/configuration09.png)

Permite exibir ou não o painel móvel quando você usa
o aplicativo em um telefone.

Configuração do equipamento
=============================

A configuração do equipamento Z-Wave pode ser acessada no menu
plugin :

![appliance01](../images/appliance01.png)

Abaixo está um exemplo de uma página de plug-in do Z-Wave (apresentada com
alguns equipamentos) :

![appliance02](../images/appliance02.png)

> **Tip**
>
> Como em muitos lugares em Jeedom, coloque o mouse na extremidade esquerda
> abre um menu de acesso rápido (você pode, em
> do seu perfil, deixe-o sempre visível).

> **Tip**
>
> Os botões na linha superior **Synchroniser**,
> **Rede Zwave** e **Santé**, são visíveis apenas se você estiver em
> modo **Expert**. ![appliance03](../images/appliance03.png)

Geral
-------

Aqui você encontra toda a configuração do seu equipamento :

![appliance04](../images/appliance04.png)

-   **Nome de equipamentos** : nome do seu módulo Z-Wave.

-   **Objeto pai** : indica o objeto pai ao qual
    pertence a equipamento.

-   **Categoria** : categorias de equipamentos (pode pertencer a
    várias categorias).

-   **Activer** : torna seu equipamento ativo.

-   **Visible** : torna visível no painel.

-   **ID do nó** : ID do módulo na rede Z-Wave. Isso pode ser
    útil se, por exemplo, você deseja substituir um módulo com defeito.
    Basta incluir o novo módulo, obter seu ID e o
    colocar no lugar do antigo ID do módulo e finalmente excluir
    o novo módulo.

-   **Module** : esse campo só aparece se houver diferentes tipos de
    configuração para o seu módulo (caso de módulos que podem fazer
    fios piloto, por exemplo). Permite escolher o
    configuração para usá-lo ou modificá-lo posteriormente

-   **Marque** : fabricante do seu módulo Z-Wave.

-   **Configuration** : janela para configurar os parâmetros do
    module

-   **Assistant** : disponível apenas em determinados módulos, você
    ajuda a configurar o módulo (estojo no teclado zipato, por exemplo)

-   **Documentation** : Este botão permite abrir diretamente o
    Documentação Jeedom referente a este módulo.

-   **Supprimer** : Permite excluir um item de equipamento e todos esses
    comandos anexados sem excluí-lo da rede Z-Wave.

> **Important**
>
> A exclusão de um equipamento não resulta em exclusão do módulo
> no controlador. ![appliance11](../images/appliance11.png) Un
> equipamento excluído que ainda esteja conectado ao seu controlador
> recriado automaticamente após a sincronização.

Commandes
---------

Abaixo você encontra a lista de pedidos :

![appliance05](../images/appliance05.png)

> **Tip**
>
> Dependendo dos tipos e subtipos, algumas opções podem ser
> ausente.

-   o nome exibido no painel
-   ícone : no caso de uma ação, você pode escolher um ícone para
    exibir no painel em vez de texto
-   Valor do pedido : no caso de um comando do tipo ação, sua
    pode ser vinculado a um comando de tipo de informação, é aqui que
    está configurado. Exemplo para uma lâmpada, a intensidade está ligada à sua
    estado, isso permite que o widget tenha o estado real da lâmpada.
-   tipo e subtipo.
-   a instância deste comando Z-Wave (reservada para especialistas).
-   a classe do controle Z-Wave (reservada a especialistas).
-   o índice de valor (reservado para especialistas).
-   o próprio pedido (reservado para especialistas).
-   "Valor do feedback do status "e" Duração antes do feedback do status" : permet
    para indicar a Jeedom que após uma alteração nas informações
    O valor deve retornar para Y, X min após a alteração. Exemplo : dans
    no caso de um detector de presença que emite apenas durante um
    detecção de presença, é útil definir, por exemplo, 0
    valor e 4 de duração, de modo que 4 minutos após a detecção de
    movimento (e se não houvesse novos) Jeedom
    redefine o valor da informação para 0 (não é mais detectado movimento).

-   Historicizar : permite historiar os dados.
-   Display : permite exibir os dados no painel.
-   Inverter : permite inverter o estado para tipos binários.
-   Unidade : unidade de dados (pode estar vazia).
-   Min / max : limites de dados (podem estar vazios).
-   Configuração avançada (pequenas rodas dentadas) : exibe a configuração avançada do comando (método de registro, widget etc.).

-   Teste : permite testar o comando.
-   Excluir (assinar -) : permite excluir o comando.

> **Important**
>
> O botão **Tester** no caso de um comando do tipo Info, não
> não consultar o módulo diretamente, mas o valor disponível no
> cache jeedom. O teste retornará o valor correto somente se o
> módulo em questão transmitiu um novo valor correspondente ao
> definição do comando. É então completamente normal não
> obter resultados após a criação de um novo comando Info,
> especialmente em um módulo de bateria que raramente notifica Jeedom.

O **loupe**, disponível na guia geral, permite recriar
todos os comandos para o módulo atual.
![appliance13](../images/appliance13.png) Si aucune Ordem n'est
presente ou se os comandos estiverem incorretos, a lupa deve remediar
a situação.

> **Important**
>
> O **loupe** excluirá os pedidos existentes. Se os pedidos
> foram usados em cenários, você precisará corrigir sua
> cenários em outros lugares onde os controles foram operados.

Jogos de Comando
-----------------

Alguns módulos possuem vários conjuntos de comandos pré-configurados

![appliance06](../images/appliance06.png)

Você pode selecioná-los através das opções possíveis, se o módulo
permet.

> **Important**
>
> É necessário executar a lupa para aplicar os novos conjuntos de
> Comandos.

Documentação e Assistente
--------------------------

Para um certo número de módulos, ajuda específica para configurar
local, bem como recomendações de parâmetros estão disponíveis.

![appliance07](../images/appliance07.png)

O botão **Documentation** fornece acesso à documentação
módulo específico para Jeedom.

Módulos especiais também têm um assistente específico para
para facilitar a aplicação de certos parâmetros ou operações.

O botão **Assistant** permite acesso à tela específica do assistente
do módulo.

Configuração recomendada
-------------------------

![appliance08](../images/appliance08.png)

Permite aplicar um conjunto de configurações recomendado pela equipe
Jeedom.

> **Tip**
>
> Quando incluídos, os módulos têm as configurações padrão de
> fabricante e algumas funções não são ativadas por padrão.

O seguinte, conforme aplicável, será aplicado para simplificar
usando o módulo.

-   **Configurações** permitindo comissionamento rápido da montagem
    funcionalidade do módulo.

-   **Grupos de associação** necessário para o funcionamento adequado.

-   **Intervalo de despertar**, para módulos com bateria.

-   Ativação de **atualização manual** para módulos
    não voltando por si mesmas suas mudanças de estados.

Para aplicar o conjunto de configurações recomendado, clique no botão
: **Configuração recomendada**, depois confirme a aplicação de
configurações recomendadas.

![appliance09](../images/appliance09.png)

O assistente ativa os vários elementos de configuração.

Uma confirmação do bom andamento será exibida na forma de um banner

![appliance10](../images/appliance10.png)

> **Important**
>
> Os módulos da bateria devem ser despertados para aplicar o conjunto de
> Configuração.

A página de equipamento informa se os itens ainda não foram
foi ativado no módulo. Por favor, consulte a documentação do
para ativá-lo manualmente ou aguardar o próximo ciclo de
despertar.

![appliance11](../images/appliance11.png)

> **Tip**
>
> É possível ativar automaticamente o aplicativo do jogo.
> configuração recomendada ao incluir um novo módulo, consulte
> a seção de configuração do plug-in para obter mais detalhes.

Configuração de módulos
=========================

É aqui que você encontrará todas as informações sobre seu módulo

![node01](../images/node01.png)

A janela possui várias guias :

Resumo
------

Fornece um resumo completo do seu nó com várias informações
neste, como por exemplo o estado dos pedidos que permite conhecer
se o nó estiver aguardando informações ou a lista de nós vizinhos.

> **Tip**
>
> Nesta guia, é possível receber alertas em caso de detecção
> possível de um problema de configuração, o Jeedom indicará a marcha
> seguir para corrigir. Não confunda um alerta com um
> erro, na maioria dos casos, o alerta é simples
> recomendação.

Valeurs
-------

![node02](../images/node02.png)

Aqui você encontrará todos os comandos e estados possíveis em seu
módulo. Eles são ordenados por instância e classe de comando e indexam.
O « mapping » de Comandos é entièrement basé sur ces Informação.

> **Tip**
>
> Forçar atualização de um valor. Os módulos de bateria
> atualize um valor apenas no próximo ciclo de ativação. Ele é
> No entanto, é possível ativar manualmente um módulo, consulte o
> Documentação do módulo.

> **Tip**
>
> É possível ter mais pedidos aqui do que no Jeedom, é
> completamente normal. Em Jeedom, os pedidos foram pré-selecionados
> para você.

> **Important**
>
> Alguns módulos não enviam seus estados automaticamente, é necessário
> neste caso, ative a atualização manual em 5 minutos no ou
> valores desejados. Recomenda-se deixar automaticamente o
> Atualizando. O abuso de atualização manual pode afetar
> fortemente o desempenho da rede Z-Wave, use apenas para
> os valores recomendados na documentação específica do Jeedom.
> ![node16](../images/node16.png) O conjunto de valores (índice) de
> a instância de um comando de classe será remontada, ativando o
> atualização manual no menor índice da instância do
> comando de classe. Repita para cada instância, se necessário.

Configurações
----------

![node03](../images/node03.png)

Aqui você encontrará todas as possibilidades de configuração para
parâmetros do seu módulo, bem como a capacidade de copiar o
configuração de outro nó já em vigor.

Quando um parâmetro é modificado, a linha correspondente fica amarela,
![node04](../images/node04.png) le paramètre é en attente d'être
appliqué.

Se o módulo aceitar o parâmetro, a linha se tornará transparente novamente.

Se, no entanto, o módulo recusar o valor, a linha ficará vermelha
com o valor aplicado retornado pelo módulo.
![node05](../images/node05.png)

Na inclusão, um novo módulo é detectado com os parâmetros por
defeito do fabricante. Em alguns módulos, a funcionalidade não
não estará ativo sem modificar um ou mais parâmetros.
Consulte a documentação do fabricante e nossas recomendações
para configurar corretamente seus novos módulos.

> **Tip**
>
> Os módulos na pilha aplicarão as alterações de parâmetro
> somente no próximo ciclo de despertar. No entanto, é possível
> ativar manualmente um módulo, consulte a documentação do módulo.

> **Tip**
>
> A ordem **Retomar de ...** permite retomar a configuração
> de outro módulo idêntico, no módulo atual.

![node06](../images/node06.png)

> **Tip**
>
> A ordem **Aplicar em ...** permite aplicar o
> configuração atual do módulo em um ou mais módulos
> idêntico.

![node18](../images/node18.png)

> **Tip**
>
> A ordem **Atualizar configurações** forçar o módulo a atualizar
> os parâmetros salvos no módulo.

Se nenhum arquivo de configuração estiver definido para o módulo, um
O assistente manual permite aplicar parâmetros ao módulo.
![node17](../images/node17.png) Veillez vous référer à o documentation
do fabricante para saber a definição do índice, valor e tamanho.

Associations
------------

É aqui que você encontra a administração dos grupos de associação de seu
module.

![node07](../images/node07.png)

Os módulos Z-Wave podem controlar outros módulos Z-Wave, sem
passar por nenhum controlador Jeedom. A relação entre um módulo de
controle e outro módulo é chamado de associação.

Para controlar outro módulo, o módulo de controle precisa
manter uma lista de dispositivos que receberão o controle de
ordens. Essas listas são chamadas de grupos de associação e são
sempre vinculado a determinados eventos (por exemplo, o botão pressionado, o
gatilhos do sensor etc.).

No caso de ocorrer um evento, todos os dispositivos
registrado no grupo de associação relevante receberá um pedido
Basic.

> **Tip**
>
> Consulte a documentação do módulo para entender as diferentes
> possíveis grupos de associação e seu comportamento.

> **Tip**
>
> A maioria dos módulos possui um grupo de associação reservado
> para o controlador principal, é usado para remontar o
> informações para o controlador. É geralmente chamado : **Report** ou
> **LifeLine**.

> **Tip**
>
> Seu módulo pode não ter nenhum grupo.

> **Tip**
>
> A modificação dos grupos de associação de um módulo na pilha será
> aplicado ao próximo ciclo de ativação. No entanto, é possível
> ativar manualmente um módulo, consulte a documentação do módulo.

Para descobrir com quais outros módulos o módulo atual está associado,
basta clicar no menu **Associado a quais módulos**

![node08](../images/node08.png)

Todos os módulos que usam o módulo atual, bem como os nomes dos
grupos de associação serão exibidos.

**Associações de várias instâncias**

algum módulo suporta um comando de classe de associações de várias instâncias.
Quando um módulo suporta este CC, é possível especificar com
qual corpo queremos criar a associação

![node09](../images/node09.png)

> **Important**
>
> Certos módulos devem estar associados à instância 0 do controlador
> principal, a fim de funcionar bem. Por esse motivo, o controlador
> está presente com e sem instância 0.

Sistemas
--------

Tabulação agrupando os parâmetros do sistema do módulo.

![node10](../images/node10.png)

> **Tip**
>
> Os módulos de bateria são ativados em ciclos regulares, chamados
> Intervalo de ativação. O intervalo de ativação é um
> compromisso entre a duração máxima da bateria e as respostas
> desejado do dispositivo. Para maximizar a vida de seu
> módulos, adapte o valor Wakeup Interval, por exemplo, a 14400
> segundos (4h), veja ainda mais dependendo dos módulos e de seu uso.
> ![node11](../images/node11.png)

> **Tip**
>
> Os módulos **Interrupteur** e **Variateur** pode implementar um
> Classe de ordem especial chamada **SwitchAll** 0x27. Você pode
> mudar o comportamento aqui. Dependendo do módulo, várias opções são
> disponível. A ordem **Ligar / Desligar** pode ser lançado via
> seu módulo controlador principal.

Actions
-------

Permite que você execute determinadas ações no módulo.

![node12](../images/node12.png)

Certas ações estarão ativas, dependendo do tipo de módulo e seu
possibilidades ou de acordo com o estado atual do módulo, como por exemplo
se presumido morto pelo controlador.

> **Important**
>
> Não use ações em um módulo se você não souber o que
> que fazemos. Algumas ações são irreversíveis. Acções
> pode ajudar a resolver problemas com um ou mais módulos
> Z-Wave.

> **Tip**
>
> O **Regeneração da detecção de nó** pode detectar o
> módulo para recuperar o último conjunto de parâmetros. Esta ação
> é necessário quando você é informado de que uma atualização de parâmetro e
> ou o comportamento do módulo é necessário para a operação adequada. O
> A regeneração da detecção do nó implica uma reinicialização do
> rede, o assistente executa automaticamente.

> **Tip**
>
> Se você tiver vários módulos idênticos dos quais é necessário
> para executar o **Regeneração da detecção de nó**, Ele é
> possível iniciá-lo uma vez para todos os módulos idênticos.

![node13](../images/node13.png)

> **Tip**
>
> Se um módulo de bateria não estiver mais acessível e você desejar
> excluí-lo, que a exclusão não ocorra, você pode iniciar
> **Remover nó fantasma** Um assistente executará diferentes
> ações para remover o chamado módulo fantasma. Esta ação envolve
> reinicie a rede e pode levar alguns minutos para ser
> concluído.

![node14](../images/node14.png)

Depois de iniciado, é recomendável fechar a tela de configuração do
módulo e monitore a remoção do módulo através da tela de integridade
Z-Wave.

> **Important**
>
> Somente módulos na bateria podem ser excluídos através deste assistente.

Statistiques
------------

Essa guia fornece algumas estatísticas de comunicação com o nó.

![node15](../images/node15.png)

Pode ser de interesse no caso de módulos que são supostamente mortos pelo
controlador "morto".

inclusão / exclusão
=====================

Quando sai da fábrica, um módulo não pertence a nenhuma rede Z-Wave.

Inclusão moda
--------------

O módulo deve ingressar em uma rede Z-Wave existente para se comunicar
com os outros módulos desta rede. Esse processo é chamado
**Inclusion**. Os dispositivos também podem deixar uma rede.
Esse processo é chamado **Exclusion**. Ambos os processos são iniciados
pelo controlador principal da rede Z-Wave.

![addremove01](../images/addremove01.png)

Este botão permite alternar para o modo de inclusão para adicionar um módulo
à sua rede Z-Wave.

Você pode escolher o modo de inclusão depois de clicar no botão
**Inclusion**.

![addremove02](../images/addremove02.png)

Desde a aparência do Z-Wave +, é possível proteger o
trocas entre o controlador e os nós. Portanto, é recomendável
faça inclusões no modo **Seguro**.

Se, no entanto, um módulo não puder ser incluído no modo seguro, por favor
incluí-lo no modo **Não seguro**.

Uma vez no modo de inclusão : Jeedom diz a você.

\ [DICA \] Um módulo 'não seguro' pode solicitar módulos 'não
seguro ". Um módulo 'não seguro' não pode solicitar um módulo
'seguro ". Um módulo 'seguro' pode solicitar módulos 'não
seguro ', desde que o transmissor o suporte.

![addremove03](../images/addremove03.png)

Depois que o assistente é iniciado, você deve fazer o mesmo no seu módulo
(consulte a documentação para mudar para o modo
inclusion).

> **Tip**
>
> Até você ter a faixa para a cabeça, você não está no modo
> Inclusão.

Se você clicar no botão novamente, sair do modo de inclusão.

> **Tip**
>
> Recomenda-se, antes da inclusão de um novo módulo que seria
> "novo "no mercado, para lançar o pedido **Módulos de configuração** via
> tela de configuração do plugin. Esta ação irá recuperar
> todas as versões mais recentes dos arquivos de configuração
> mapeamento de comandos openzwave e Jeedom.

> **Important**
>
> Durante uma inclusão, é recomendável que o módulo esteja próximo
> do controlador principal, a menos de um metro do seu jeedom.

> **Tip**
>
> Alguns módulos requerem uma inclusão no modo
> **Seguro**, por exemplo, para fechaduras de portas.

> **Tip**
>
> Observe que a interface móvel também fornece acesso à inclusão,
> o painel móvel deve ter sido ativado.

> **Tip**
>
> Se o módulo já pertence a uma rede, siga o processo
> exclusão antes de incluí-lo em sua rede. Caso contrário, a inclusão de
> este módulo falhará. Também é recomendável executar uma
> exclusão antes da inclusão, mesmo que o produto seja novo, fora
> papelão.

> **Tip**
>
> Depois que o módulo estiver em sua localização final, você deverá iniciar
> a ação cuida da rede, a fim de solicitar todos os módulos de
> atualizar todos os vizinhos.

Modo de exclusão
--------------

![addremove04](../images/addremove04.png)

Este botão permite entrar no modo de exclusão, para remover um
módulo da sua rede Z-Wave, você deve fazer o mesmo com o seu
módulo (consulte a documentação para alternar para o modo
exclusion).

![addremove05](../images/addremove05.png)

> **Tip**
>
> Até você ter a faixa para a cabeça, você não está no modo
> Exclusão.

Se você clicar no botão novamente, sairá do modo de exclusão.

> **Tip**
>
> Observe que a interface móvel também fornece acesso à exclusão.

> **Tip**
>
> Um módulo não precisa ser excluído pelo mesmo controlador em
> que foi incluído anteriormente. Daí o fato de recomendarmos
> executar uma exclusão antes de cada inclusão.

Synchroniser
------------

![addremove06](../images/addremove06.png)

Botão para sincronizar os módulos da rede Z-Wave com o
Equipamento Jeedom. Os módulos estão associados ao controlador principal,
o equipamento no Jeedom é criado automaticamente quando é
inclusão. Eles também são excluídos automaticamente quando excluídos.,
se a opção **Excluir automaticamente dispositivos excluídos** est
ativado.

Se você incluiu módulos sem o Jeedom (requer um dongle com
bateria como o Aeon-labs Z-Stick GEN5), a sincronização será
necessário após conectar a chave, uma vez iniciado o daemon e
fonctionnel.

> **Tip**
>
> Se você não possui a imagem ou o Jeedom não reconheceu seu módulo,
> este botão pode ser usado para corrigir (desde que a entrevista com o
> módulo está completo).

> **Tip**
>
> Se na sua tabela de roteamento e / ou na tela de integridade do Z-Wave, você
> ter um ou mais módulos nomeados com seus **nome genérico**, la
> sincronização remediará esta situação.

O botão Sincronizar é visível apenas no modo especialista :
![addremove07](../images/addremove07.png)

Redes Z-Wave
==============

![network01](../images/network01.png)

Aqui você encontrará informações gerais sobre sua rede Z-Wave.

![network02](../images/network02.png)

Resumo
------

A primeira guia fornece o resumo básico da sua rede Z-Wave,
você encontrará em particular o estado da rede Z-Wave, bem como o número
itens na fila.

**Informations**

-   Fornece informações gerais sobre a rede, a data de
    inicialização, o tempo necessário para obter a rede em um estado
    diz funcional.

-   O número total de nós na rede, bem como o número que dorme
    no momento.

-   O intervalo de solicitação está associado à atualização manual. Ele
    está predefinido no mecanismo Z-Wave em 5 minutos.

-   Os vizinhos do controlador.

**Etat**

![network03](../images/network03.png)

Um conjunto de informações sobre o estado atual da rede, nomeadamente :

-   Estado atual, talvez **Driver Inicializado**, **Topologia carregada**
    onde **Ready**.

-   Cauda de saída, indica o número de mensagens na fila
    controlador esperando para ser enviado. Este valor é geralmente
    alta durante a inicialização da rede quando o status ainda está em
    **Driver Inicializado**.

Quando a rede atingir pelo menos **Topologia carregada**, des
mecanismos internos ao servidor Z-Wave forçarão atualizações no
valores, é completamente normal ver o número de
mensagens. Isso retornará rapidamente para 0.

> **Tip**
>
> Diz-se que a rede está funcional quando atinge o status
> **Topologia carregada**, isto é, o conjunto de nós do setor
> completaram suas entrevistas. Dependendo do número de módulos, o
> distribuição de bateria / setor, a escolha do dongle USB e do PC no qual
> ativar o plug-in Z-Wave, a rede alcançará esse estado entre um
> e cinco minutos.

Uma rede **Ready**, significa que todos os nós do setor e da pilha têm
completaram sua entrevista.

> **Tip**
>
> Dependendo dos módulos que você possui, é possível que a rede
> nunca alcança status por si só **Ready**. Os controles remotos,
> por exemplo, não acorde por conta própria e não irá complementar
> nunca a entrevista deles. Nesse tipo de caso, a rede é completamente
> operacional e mesmo que os controles remotos não tenham completado sua
> entrevista, eles garantem sua funcionalidade dentro da rede.

**Capacidades**

Usado para descobrir se o controlador é um controlador principal ou
secondaire.

**Sistema**

Exibe várias informações do sistema.

-   Informações sobre a porta USB usada.

-   Versão da biblioteca OpenZwave

-   Versão da biblioteca Python-OpenZwave

Actions
-------

![network05](../images/network05.png)

Aqui você encontrará todas as ações possíveis para todos os seus
Rede Z-Wave. Cada ação é acompanhada de uma breve descrição.

> **Important**
>
> Algumas ações são realmente arriscadas ou até irreversíveis, a equipe
> A Jeedom não pode ser responsabilizada em caso de má
> manipulação.

> **Important**
>
> Alguns módulos requerem inclusão no modo seguro, por
> exemplo para fechaduras de portas. A inclusão segura deve ser
> lançado através da ação desta tela.

> **Tip**
>
> Se uma ação não puder ser iniciada, ela será desativada até
> quando pode ser executado novamente.

Statistiques
------------

![network06](../images/network06.png)

Aqui você encontrará estatísticas gerais de todos os seus
Rede Z-Wave.

Gráfico de rede
-------------------

![network07](../images/network07.png)

Essa guia fornece uma representação gráfica dos diferentes
links entre nós.

Explicação da legenda da cor :

-   **Noir** : O controlador principal, geralmente representado
    como Jeedom.

-   **Vert** : Comunicação direta com o controlador, ideal.

-   **Blue** : Para controladores, como controles remotos, eles são
    associado ao controlador primário, mas não tem vizinhos.

-   **Jaune** : Todas as estradas têm mais de um salto antes de chegar
    para o controlador.

-   **Gris** : A entrevista ainda não está concluída, os links serão
    realmente conhecido quando a entrevista é concluída.

-   **Rouge** : presumidamente morto, ou sem vizinho, não participa / não mais
    malha de rede.

> **Tip**
>
> Somente equipamentos ativos serão exibidos no gráfico de rede.

A rede Z-Wave consiste em três tipos diferentes de nós com
três funções principais.

A principal diferença entre os três tipos de nós é sua
conhecimento da tabela de roteamento de rede e, posteriormente, sua
capacidade de enviar mensagens para a rede:

Tabela de roteamento
----------------

Cada nó é capaz de determinar em quais outros nós estão.
Comunicação direta. Esses nós são chamados vizinhos. Durante
inclusão e / ou posteriormente, mediante solicitação, o nó pode
para informar o controlador da lista de vizinhos. Graças a estes
informações, o controlador é capaz de criar uma tabela que possui
todas as informações sobre possíveis vias de comunicação em
Uma rede.

![network08](../images/network08.png)

As linhas da tabela contêm os nós de origem e as colunas
conter nós de destino. Consulte a legenda para
entender as cores das células que indicam os links entre dois
nós.

Explicação da legenda da cor :

-   **Vert** : Comunicação direta com o controlador, ideal.

-   **Blue** : Pelo menos 2 rotas com um salto.

-   **Jaune** : Menos de 2 rotas com um salto.

-   **Gris** : A entrevista ainda não está concluída, será realmente
    atualizado após a conclusão da entrevista.

-   **Orange** : Todas as estradas têm mais de um salto. Pode causar
    latências.

> **Tip**
>
> Somente equipamentos ativos serão exibidos no gráfico de rede.

> **Important**
>
> Um módulo supostamente morto, não participa / não mais da rede da rede.
> Será marcado aqui com um ponto de exclamação vermelho em um triângulo.

> **Tip**
>
> Você pode iniciar manualmente a atualização do vizinho, por módulo
> ou para toda a rede usando os botões disponíveis no
> Tabela de roteamento.

Santé
=====

![health01](../images/health01.png)

Esta janela resume o status da sua rede Z-Wave :

![health02](../images/health02.png)

Você tem aqui :

-   **Module** : o nome do seu módulo, um clique nele permite que você
    acessar diretamente.

-   **ID** : ID do seu módulo na rede Z-Wave.

-   **Notification** : último tipo de troca entre o módulo e o
    Controlador

-   **Groupe** : indica se a configuração do grupo está ok
    (controlador pelo menos em um grupo). Se você não tem nada, é porque
    o módulo não suporta a noção de grupo, isso é normal

-   **Constructeur** : indica se a recuperação de informações
    identificação do módulo está ok

-   **Voisin** : indica se a lista de vizinhos foi recuperada

-   **Statut** : Indica o status da entrevista (estágio de consulta) do
    module

-   **Batterie** : nível da bateria do módulo (um plugue
    indica que o módulo é alimentado pela rede elétrica).

-   **Hora de acordar** : para módulos de bateria, fornece a
    frequência em segundos dos instantes em que o módulo
    acorde automaticamente.

-   **Pacote total** : exibe o número total de pacotes recebidos ou
    enviado com sucesso para o módulo.

-   **%OK** : exibe a porcentagem de pacotes enviados / recebidos
    com sucesso.

-   **Temporisation** : exibe o atraso médio do envio de pacotes em ms.

-   **Última notificação** : Data da última notificação recebida de
    módulo e a próxima hora de ativação programada para módulos
    quem dorme.

    -   Também permite informar se o nó ainda não está
        acordei uma vez desde o lançamento do demônio.

    -   E indica se um nó não acordou como esperado.

-   **Ping** : Envie uma série de mensagens para o módulo para
    testar seu bom funcionamento.

> **Important**
>
> O equipamento desativado será exibido, mas nenhuma informação do
> o diagnóstico estará presente apenas.

O nome do módulo pode ser seguido por uma ou duas imagens:

![health04](../images/health04.png) Modules supportant la
COMANDO\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../images/health05.png) Modules supportant la
COMMAND\_CLASS\_SECURITY e seguro.

![health06](../images/health06.png) Modules supportant la
COMMAND\_CLASS\_SECURITY e não seguro.

![health07](../images/health07.png) Módulo FLiRS, routeurs esclaves
(módulos de bateria) com audição frequente.

> **Tip**
>
> O comando Ping pode ser usado se o módulo for considerado morto
> "MORTE "para confirmar se este é realmente o caso.

> **Tip**
>
> Os módulos adormecidos só responderão ao Ping quando
> próximo acordar.

> **Tip**
>
> A notificação de tempo limite não significa necessariamente um problema
> com o módulo. Faça ping e, na maioria dos casos, o módulo
> responderá com uma notificação **NoOperation** que confirma um retorno
> Ping frutífero.

> **Tip**
>
> Tempo limite e% OK nos nós das baterias antes da conclusão
> da entrevista não é significativa. Na verdade, o nó não vai
> responda às perguntas do controlador sobre o fato de ele estar dormindo
> profundo.

> **Tip**
>
> O servidor Z-Wave cuida automaticamente do lançamento de testes no
> Módulos de tempo limite após 15 minutos

> **Tip**
>
> O servidor Z-Wave tenta remontar automaticamente os módulos
> presumido morto.

> **Tip**
>
> Um alerta será enviado ao Jeedom se o módulo estiver presumivelmente morto. Você
> pode ativar uma notificação para ser informado o mais
> rapidamente possível. Veja a configuração de Mensagens na tela
> Configuração do Jeedom.

![health03](../images/health03.png)

> **Tip**
>
> Se na sua mesa de roteamento e / ou na tela de integridade do Z-Wave você
> ter um ou mais módulos nomeados com seus **nome genérico**, la
> sincronização remediará esta situação.

> **Tip**
>
> Se na sua mesa de roteamento e / ou na tela de integridade do Z-Wave você
> tem um ou mais módulos nomeados **Unknown**, isso significa
> a entrevista do módulo não foi concluída com êxito. Você tem
> provavelmente um **NOK** na coluna do construtor. Abra os detalhes
> do (s) módulo (s), para experimentar as soluções sugeridas.
> (consulte a seção Solução de problemas e diagnóstico, abaixo)

Status da entrevista
---------------------

Etapa de entrevistar um módulo após iniciar o daemon.

-   **None** Inicialização do processo de procura do nó.

-   **ProtocolInfo** Recupere as informações do protocolo, se isso
    nó está escutando (ouvinte), sua velocidade máxima e suas classes
    de periféricos.

-   **Probe** Faça ping no módulo para ver se está ativado.

-   **WakeUp** Inicie o processo de ativação, se for um
    nó de dormir.

-   **ManufacturerSpecific1** Recupere o nome do fabricante e
    identifica produtos se ProtocolInfo permitir.

-   **NodeInfo** Recuperar informações sobre gerenciamento de classes
    comandos suportados.

-   **NodePlusInfo** Recupere informações sobre o ZWave + no suporte
    classes de comando suportadas.

-   **SecurityReport** Recupere a lista de classes de pedidos que
    requer segurança.

-   **ManufacturerSpecific2** Recupere o nome do fabricante e o
    identificadores de produto.

-   **Versions** Recuperar informações da versão.

-   **Instances** Recuperar informações de classe de várias instâncias
    de ordem.

-   **Static** Recuperar informações estáticas (não muda).

-   **CacheLoad** Efetue ping no módulo durante a reinicialização com o cache de configuração
    do dispositivo.

-   **Associations** Recuperar informações sobre associações.

-   **Neighbors** Recuperar a lista de nós vizinhos.

-   **Session** Recuperar informações da sessão (raramente muda).

-   **Dynamic** Recuperar informações dinâmicas
    (muda frequentemente).

-   **Configuration** Recuperar informações de parâmetro de
    configurações (feitas somente mediante solicitação).

-   **Complete** O processo de entrevista está finalizado para este nó.

Notification
------------

Detalhes das notificações enviadas pelos módulos

-   **Completed** Ação concluída com sucesso.

-   **Timeout** Atraso no relatório relatado ao enviar uma mensagem.

-   **NoOperation** Relate em um teste de nó (Ping) que a mensagem
    foi enviado com sucesso.

-   **Awake** Relatar quando um nó acabou de acordar

-   **Sleep** Relatar quando um nó adormeceu.

-   **Dead** Relatar quando um nó é considerado morto.

-   **Alive** Relatar quando um nó é relançado.

Backups
=======

A parte de backup permitirá gerenciar os backups da topologia
da sua rede. Este é o seu arquivo zwcfgxxx.xml, é o
último estado conhecido da sua rede, é uma forma de cache do seu
rede. Nesta tela você pode :

-   Inicie um backup (um backup é feito a cada parada de reiniciar o
    rede e durante operações críticas). Os últimos 12 backups
    são mantidos

-   Restaurar um backup (selecionando-o na lista
    logo acima)

-   Excluir um backup

![backup01](../images/backup01.png)

Atualizar o OpenZWave
=======================

Após uma atualização do plugin Z-Wave, é possível que o Jeedom
solicitação para atualizar dependências do Z-Wave. Um NOK ao nível de
dependências serão exibidas:

![update01](../images/update01.png)

> **Tip**
>
> Uma atualização das dependências não deve ser feita a cada atualização
> plugin.

A Jeedom deve iniciar a atualização de dependência por conta própria se o
plugin considera que eles são **NOK**. Essa validação é realizada em
depois de 5 minutos.

A duração desta operação pode variar dependendo do seu sistema
(até mais de 1 hora no raspberry pi)

Depois que a atualização das dependências estiver concluída, o daemon será reiniciado
automaticamente após a validação do Jeedom. Essa validação é
feito após 5 minutos.

> **Tip**
>
> Caso a atualização de dependências não ocorra
> não estiver completo, consulte o log **Openzwave\_update** qui
> deve informá-lo sobre o problema.

Lista de módulos compatíveis
============================

Você encontrará a lista de módulos compatíveis
[aqui](https://doc.jeedom.com/pt_PT/zwave/equipement.compatible)

Solução de problemas e diagnóstico
=======================

Meu módulo não foi detectado ou não fornece seus identificadores de produto e tipo
-------------------------------------------------------------------------------

![troubleshooting01](../images/troubleshooting01.png)

Inicie a regeneração da detecção de nó na guia Ações
do módulo.

Se você tiver vários módulos nesse cenário, inicie **Regenerar
detecção de nós desconhecidos** da tela **Rede Zwave** onglet
**Actions**.

Meu módulo é considerado morto pelo controlador Dead
--------------------------------------------------

![troubleshooting02](../images/troubleshooting02.png)

Se o módulo ainda estiver conectado e acessível, siga as soluções
proposto na tela do módulo.

Se o módulo foi cancelado ou está com defeito, você pode
pode excluí-lo da rede usando **excluir o nó com erro**
via guia **Actions**.

Se o módulo foi reparado e um novo módulo
substituição foi entregue, você pode iniciar **Substituir nó com falha**
via guia **Actions**, o controlador aciona a inclusão, então você
deve continuar com a inclusão no módulo. O ID do módulo antigo será
mantido, bem como suas ordens.

Como usar o comando SwitchAll
--------------------------------------

![troubleshooting03](../images/troubleshooting03.png)

Está disponível através do nó do seu controlador. Seu controlador deve
tem os comandos Switch All On e Switch All Off.

Se o seu controlador não aparecer na sua lista de módulos, inicie o
synchronisation.

![troubleshooting04](../images/troubleshooting04.png)

O comando Switch All Class geralmente é suportado em
interruptores e dimmers. Seu comportamento é configurável em
cada módulo que o suporta.

Para que possamos:

-   Desativar o comando Switch All Class.

-   Ativar para ativar e desativar.

-   Ativar apenas.

-   Ativar apenas Desativado.

A escolha das opções depende do fabricante.

Então você tem que reservar um tempo para revisar todas as suas
interruptores / dimmers antes de configurar um cenário, se você não
não apenas luzes piloto.

Meu módulo não possui um comando Cena ou Botão
----------------------------------------------

![troubleshooting05](../images/troubleshooting05.png)

Você pode adicionar o comando na tela de mapeamento de comandos.

Esta é uma ordem **Info** no CC **0x2b** Instância **0** commande
**dados \ [0 \]. val**

O modo de cena deve ser ativado nas configurações do módulo. Veja o
documentação do seu módulo para obter mais detalhes.

Forçar valores de atualização
-------------------------------------

É possível forçar, mediante solicitação, a atualização dos valores
uma instância para um comando de classe específico.

É possível fazer isso através de uma solicitação http ou criar um pedido
na tela de mapeamento de equipamentos.

![troubleshooting06](../images/troubleshooting06.png)

Esta é uma ordem **Action** escolha o **CC** desejado para um
**Instance** dado com o comando **dados \ [0 \]. ForceRefresh ()**

Todos os índices de instância para este comando Class serão colocados
atualizado. Os nós das baterias aguardam o próximo despertar antes de
atualize seu valor.

Você também pode usar por script emitindo uma solicitação http para
Servidor REST Z-Wave.

Substitua ip\_jeedom, node\_id, instance\_id, cc\_id e index

http://token:\#APIKEY\#@ip\_jeedom:8083/ZWaveAPI/Run/devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

O acesso à API REST foi alterado, veja detalhes
[aqui](./restapi.asciidoc).

Transfira os módulos para um novo controlador
------------------------------------------------

Por razões diferentes, pode ser necessário transferir
todos os seus módulos em um novo controlador principal.

Você decide ir de **raZberry** para um **Z-Stick Gen5** ou porque
você tem que fazer uma **Reset** completo do controlador principal.

Aqui estão diferentes etapas para chegar lá sem perder seus cenários,
widgets de valor e histórico:

-   1 \) Faça um backup do Jeedom.

-   2 \) Lembre-se de anotar (captura de tela) seus valores de parâmetro para cada
    módulo, eles serão perdidos devido à exclusão.

-   3 \) Na configuração do Z-Wave, desmarque a opção "Excluir
    excluir automaticamente dispositivos "e fazer backup.
    reinicializações de rede.

-   4a) No caso de um **Reset**, Redefinir o controlador
    principal e reinicie o plugin.

-   4b) Para um novo controlador, pare o Jeedom, desconecte o antigo
    controlador e conecte o novo. Iniciar Jeedom.

-   5 \) Para cada dispositivo Z-Wave, altere o ID do ZWave para **0**.

-   6 \) Abra 2 páginas do plugin Z-Wave em diferentes guias.

-   7 \) (Através da primeira guia) Vá para a página de configuração de um
    módulo que você deseja incluir no novo controlador.

-   8 \) (Via segunda guia) Excluir e incluir
    do módulo. Novos equipamentos serão criados.

-   9 \) Copie o ID Z-Wave do novo equipamento e exclua
    este equipamento.

-   10 \) Volte à guia do módulo antigo (1ª guia) e cole
    o novo ID no lugar do antigo ID.

-   11 \) os parâmetros do ZWave foram perdidos durante a exclusão / inclusão,
    lembre-se de redefinir suas configurações específicas se você não estiver usando o
    valores padrão.

-   11 \) Repita as etapas 7 a 11 para cada módulo a ser transferido.

-   12 \) No final, você não deve mais ter equipamentos no ID 0.

-   13 \) Verifique se todos os módulos estão nomeados corretamente na tela de
    saúde Z-Wave. Inicie a sincronização se não for esse o caso.

Substitua um módulo defeituoso
------------------------------

Como refazer a inclusão de um módulo defeituoso sem perder seu
cenários de valor, widgets e histórico

Se o módulo for considerado "inoperante"" :

-   Observe (captura de tela) seus valores de parâmetro, eles serão perdidos
    após inclusão.

-   Vá para a guia Actions do módulo e ative o comando
    "Substituir nó com falha".

-   O controlador está no modo de inclusão, prossiga com a inclusão de acordo com o
    Documentação do módulo.

-   Redefina seus parâmetros específicos.

Se o módulo não estiver "morto", mas ainda estiver acessível:

-   Na configuração do ZWave, desmarque a opção "Excluir
    dispositivos excluídos automaticamente".

-   Observe (captura de tela) seus valores de parâmetro, eles serão perdidos
    após inclusão.

-   Excluir o módulo defeituoso.

-   Vá para a página de configuração do módulo defeituoso.

-   Abra a página de plug-in do ZWave em uma nova guia.

-   Inclua o módulo.

-   Copie o ID do novo módulo e exclua este equipamento.

-   Volte à guia do módulo antigo e cole o novo ID para
    o local do ID antigo.

-   Redefina seus parâmetros específicos.

Remoção do nó fantasma
----------------------------

Se você perdeu toda a comunicação com um módulo alimentado por bateria e
você deseja excluí-lo da rede, é possível que a exclusão
não é bem-sucedido ou o nó permanece presente na sua rede.

O assistente automático de nó fantasma está disponível.

-   Vá para a guia Actions do módulo para excluir.

-   Ele provavelmente terá um status **CacheLoad**.

-   Comando Iniciar **Remover nó fantasma**.

-   A rede Z-Wave para. O assistente automático modifica o
    Ficheiro **zwcfg** para remover o CC WakeUp do módulo. O
    reinicializações de rede.

-   Feche a tela do módulo.

-   Abra a tela Z-Wave Health.

-   Aguarde o ciclo de inicialização ser concluído (topologia carregada).

-   O módulo normalmente será marcado como supostamente morto.

-   No próximo minuto, você verá o nó desaparecer da tela
    saúde.

-   Se na configuração do Z-Wave, você desmarcou a opção
    "Remover automaticamente dispositivos excluídos ", você precisará
    excluir manualmente o equipamento correspondente.

Este assistente está disponível apenas para módulos de bateria.

Ações pós-inclusão
----------------------

Recomenda-se realizar a inclusão de pelo menos 1M do controlador
principal, mas não será a posição final do seu novo módulo.
Aqui estão algumas boas práticas a seguir após a inclusão de um novo
módulo na sua rede.

Depois que a inclusão é concluída, vários
parâmetros para o nosso novo módulo, a fim de tirar o máximo proveito dele. Lembrete,
módulos, após a inclusão, têm as configurações padrão de
construtor. Aprecie estar ao lado do controlador e da interface
Jeedom para configurar corretamente seu novo módulo. Também será mais
simples ativar o módulo para ver o efeito imediato da mudança.
Alguns módulos possuem documentação específica do Jeedom para você
ajuda com diferentes parâmetros, bem como com os valores recomendados.

Teste seu módulo, valide feedback de informações, feedback de status
e possíveis ações no caso de um atuador.

Durante a entrevista, seu novo módulo procurou seus vizinhos.
No entanto, os módulos da sua rede ainda não conhecem seu
novo módulo.

Mova seu módulo para seu local final. Iniciar a atualização
de seus vizinhos e acordá-lo novamente.

![troubleshooting07](../images/troubleshooting07.png)

Vemos que ele vê um certo número de vizinhos, mas que o
vizinhos não vêem.

Para remediar esta situação, é necessário tomar as medidas necessárias para tratar o problema.
rede, a fim de solicitar a todos os módulos que encontrem seus vizinhos.

Essa ação pode levar 24 horas antes de terminar, seus módulos
na bateria executará a ação somente na próxima vez que acordarem.

![troubleshooting08](../images/troubleshooting08.png)

A opção de tratar a rede duas vezes por semana permite fazer isso
processo sem ação de sua parte, é útil ao configurar
coloca novos módulos e ou quando são movidos.

Sem feedback da condição da bateria
-------------------------------

Os módulos Z-Wave raramente enviam o status da bateria para o
controlador. Alguns o farão na inclusão somente quando
isso atinge 20% ou outro valor limite crítico.

Para ajudá-lo a monitorar melhor o status de suas baterias, a tela Baterias
no menu Análise, fornece uma visão geral do status do seu
pilhas. Um mecanismo de notificação de bateria fraca também é
disponible.

O valor retornado da tela Baterias é o último conhecido no
cache.

Todas as noites, o plug-in Z-Wave solicita que cada módulo atualize
Valor da bateria. Na próxima vez que você acordar, o módulo envia o valor para
Jeedom a ser adicionado ao cache. Então você geralmente tem que esperar até
pelo menos 24 horas antes de obter um valor na tela Baterias.

> **Tip**
>
> É claro que é possível atualizar manualmente o valor
> Bateria através da guia Valores do módulo e aguarde o próximo
> alarme ou ativar manualmente o módulo para obter
> recuperação imediata. O intervalo de ativação do módulo
> é definido na guia Sistema do módulo. Para otimizar a vida de
> baterias, recomenda-se espaçar esse atraso o máximo possível. Por 4h,
> aplicar 14400, 12h 43200. Alguns módulos devem
> ouça regularmente mensagens do controlador, como
> Termostatos. Nesse caso, é necessário pensar em 15 min ou 900. Cada
> módulo é diferente, então não existe uma regra exata, este é o caso
> por caso e por experiência.

> **Tip**
>
> A descarga de uma bateria não é linear, alguns módulos serão
> mostra uma grande perda percentual nos primeiros dias da aposta
> em serviço, não se mova por semanas para esvaziar
> rapidamente uma vez passado 20%.

O controlador está sendo inicializado
----------------------------------------

Ao iniciar o daemon Z-Wave, se você tentar iniciar
imediatamente uma inclusão / exclusão, você corre o risco de receber
message: \* "O controlador está sendo inicializado, por favor
tente novamente em alguns minutos"

> **Tip**
>
> Depois que o daemon é iniciado, o controlador alterna para todos os
> módulos para repetir sua entrevista. Esse comportamento é
> completamente normal no OpenZWave.

Se, no entanto, após alguns minutos (mais de 10 minutos), você tiver
ainda esta mensagem, não é mais normal.

Você precisa tentar as diferentes etapas:

-   Verifique se as luzes da tela de integridade do Jeedom estão verdes.

-   Verifique se a configuração do plug-in está em ordem.

-   Verifique se você selecionou a porta correta para o
    Tecla ZWave.

-   Verifique se a configuração da sua rede Jeedom está correta.
    (Atenção, se você fez uma Restauração de uma instalação DIY para
    imagem oficial, sufixo / jeedom não deve ser incluído)

-   Veja o log do plug-in para ver se há um erro.
    não acordado.

-   Assista ao **Console** Plugin ZWave, para ver se há um erro
    não subiu.

-   Lançar o demônio por **Debug** olhe novamente para o **Console** et
    logs de plug-in.

-   Reinicie completamente o Jeedom.

-   Verifique se você possui um controlador Z-Wave, o
    Razberry são frequentemente confundidos com o EnOcean (erro durante
    a ordem).

Agora devemos iniciar os testes de hardware:

-   O Razberry está bem conectado à porta GPIO.

-   Energia USB é suficiente.

Se o problema persistir, reinicie o controlador:

-   Pare completamente o seu Jeedom através do menu Parar no
    perfil de usuário.

-   Desconecte a energia.

-   Remova o dongle USB ou o Razberry, conforme apropriado, aproximadamente
    5 minutos.

-   Reconecte tudo e tente novamente.

O controlador não responde mais
----------------------------

Não há mais pedidos transmitidos para os módulos, mas retorna
dos estados subiram em direção a Jeedom.

A fila de mensagens do controlador pode estar cheia.
Consulte a tela Z-Wave Network se o número de mensagens pendentes não
qu'augmenter.

Nesse caso, você deve reiniciar o Demon Z-Wave.

Se o problema persistir, você deve redefinir o controlador:

-   Pare completamente o seu Jeedom através do menu Parar no
    perfil de usuário.

-   Desconecte a energia.

-   Remova o dongle USB ou o Razberry, conforme apropriado, aproximadamente
    5 minutos.

-   Reconecte tudo e tente novamente.

Erro durante dependências
---------------------------

Vários erros podem ocorrer ao atualizar
dependências. Você deve consultar o log de atualização de dependência
para determinar qual é exatamente o erro. Geralmente,
o erro está no final do log nas últimas linhas.

Aqui estão os possíveis problemas e suas possíveis soluções:

-   não foi possível instalar o mercurial - abortar

O pacote mercurial não deseja instalar, para corrigir o lançamento no
ssh:

````
    sudo rm /var/lib/dpkg/info/$mercurial* -f
    sudo apt-ge install mercurial
````

-   Vícios parecem bloqueados em 75%

Em 75%, este é o início da compilação da biblioteca openzwave também
empacotador python openzwave. Este passo é muito longo, podemos
no entanto, consulte o progresso através da visualização do log de atualização. Ele
então seja paciente.

-   Erro ao compilar a biblioteca openzwave

````
        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed source if appropriate.
        See <file:///usr/share/doc/gcc-4.9/README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targe 'build' failed
        make: *** [build] Erro 1
````

Este erro pode ocorrer devido à falta de memória RAM durante o
compilation.

Na interface do usuário jeedom, inicie a compilação de dependências.

Uma vez iniciado, no ssh, interrompa esses processos (consumidores em
memória) :

````
    sudo systemctl stop cron
    sudo systemctl stop apache2
    sudo systemctl stop mysql.
````

Para acompanhar o andamento da compilação, adaptamos o
arquivo de log openzwave\_update.

````
    tail -f /var/www/html/log/openzwave_update
````

Quando a compilação estiver concluída e sem erros, reinicie o
serviços que você parou

sudo systemctl start cron sudo systemctl start apache2 sudo systemctl
inicie o mysql

Usando o cartão Razberry em um Raspberry Pi 3
------------------------------------------------------

Para usar um controlador Razberry em um Raspberry Pi 3, o
O controlador Bluetooth interno do Raspberry deve estar desativado.

Adicione esta linha:

````
    dtoverlay=pi3-miniuart-bt
````

No final do arquivo:

````
    /boot/config.txt
````

Em seguida, reinicie o seu Raspberry.

API HTTP
========

O plugin Z-Wave fornece desenvolvedores e usuários
uma API completa para operar a rede Z-Wave por solicitação
HTTP.

Você pode usar todos os métodos expostos pelo
Servidor REST do daemon Z-Wave.

A sintaxe para chamar rotas está neste formato:

URL  =
[http://token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/ \#ROUTE\#](http://token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/#ROUTE#)

-   \#API\_KEY\# corresponde à sua chave de API, específica para
    sua instalação. Para encontrá-lo, vá ao menu «
    Geral », puis « Administration » e « Configuração », en activant
    No modo Expert, você verá uma linha de API Key.

-   \#IP\_JEEDOM\# corresponde ao seu URL de acesso Jeedom.

-   \#PORTDEMON\# corresponde ao número da porta especificado na página de
    configuração do plug-in Z-Wave, por padrão: 8083.

-   \#ROUTE\# corresponde à rota no servidor REST para executar.

Para conhecer todas as rotas, consulte
[github](https://github.com/jeedom/plugin-openzwave) do plugin Z-Wave.

Example: Para executar ping no ID do nó 2

URL  =
http://token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ZWaveAPI/Run/devices\[2\].TestNode()

# FAQ

> **Recebo o erro "Não há espaço suficiente no buffer do fluxo"**
>
> Infelizmente esse erro é de hardware, não há nada que possamos fazer e estamos procurando, no momento, como forçar a reinicialização do daemon no caso desse erro (mas muitas vezes também é necessário desconectar a chave por 5 minutos para que ela reinicie)
