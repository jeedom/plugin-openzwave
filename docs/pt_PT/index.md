# OpenZWave plugin

Este plugin permite a exploração de módulos Z-Wave através da biblioteca OpenZwave.

# Introduction

O Z-Wave se comunica usando a tecnologia de rádio de baixa potência na faixa de frequência de 868,42 MHz. Foi projetado especificamente para aplicações de automação residencial. O protocolo de rádio Z-Wave é otimizado para trocas de baixa largura de banda (entre 9 e 40 kbit / s) entre dispositivos com bateria ou alimentados por rede elétrica.

O Z-Wave opera na faixa de frequência sub-gigahertz, de acordo com as regiões (868 MHz na Europa, 908 MHz nos EUA e outras frequências de acordo com as bandas ISM das regiões). O alcance teórico é de cerca de 30 metros em ambientes fechados e 100 metros em ambientes externos. A rede Z-Wave usa tecnologia de malha para aumentar o alcance e a confiabilidade. O Z-Wave foi projetado para ser facilmente integrado a produtos eletrônicos de baixa potência, incluindo dispositivos alimentados por bateria, como controles remotos, detectores de fumaça e sensores de segurança.

O Z-Wave + traz algumas melhorias, incluindo um alcance melhor e melhora a vida útil das baterias, entre outras. Total compatibilidade com o Z-Wave.

## Distâncias a serem respeitadas com outras fontes de sinais sem fio

Os receptores de rádio devem estar posicionados a uma distância mínima de 50 cm de outras fontes de rádio.

Exemplos de fontes de rádio:

-   Ordinateurs
-   Aparelhos de microondas
-   Transformadores eletrônicos
-   equipamento de áudio e vídeo
-   Dispositivos de pré-acoplamento para lâmpadas fluorescentes

> **Dica**
>
> Se você possui um controlador USB (Z-Stick), é recomendável afastá-lo da caixa usando um cabo de extensão USB simples de 1M, por exemplo.

A distância entre outros transmissores sem fio, como telefones sem fio ou transmissões de áudio e rádio, deve ser de pelo menos 3 metros. As seguintes fontes de rádio devem ser consideradas :

-   Interferência por interruptor de motores elétricos
-   Interferência de dispositivos elétricos defeituosos
-   Interferência do equipamento de solda HF
-   dispositivos de tratamento médico

## Espessura eficaz da parede

As localizações dos módulos devem ser escolhidas de forma que a linha de conexão direta funcione apenas a uma distância muito curta do material (uma parede), a fim de evitar atenuações o máximo possível.

![introduction01](../images/introduction01.png)

Peças metálicas do edifício ou mobiliário podem bloquear ondas eletromagnéticas.

## Malha e roteamento

Os nós Z-Wave da rede podem transmitir e repetir mensagens que não estão dentro do alcance direto do controlador. Isso permite maior flexibilidade de comunicação, mesmo se não houver conexão direta sem fio ou se uma conexão estiver temporariamente indisponível, devido a uma alteração na sala ou no prédio.

![introduction02](../images/introduction02.png)

O controlador **Id 1** pode se comunicar diretamente com os nós 2, 3 e 4. O nó 6 está fora de seu alcance de rádio, no entanto, está na área de cobertura de rádio do nó 2. Portanto, o controlador pode se comunicar com o nó 6 via nó 2. Dessa maneira, o caminho do controlador via nó 2 para o nó 6 é chamado de rota. Caso a comunicação direta entre o nó 1 e o nó 2 seja bloqueada, existe ainda outra opção para se comunicar com o nó 6, usando o nó 3 como outro repetidor de sinal.

Torna-se óbvio que quanto mais nós de setor você tiver, mais as opções de roteamento aumentam e mais a estabilidade da rede aumenta. O protocolo Z-Wave é capaz de rotear mensagens através de até quatro nós repetidos. É um compromisso entre o tamanho da rede, a estabilidade e a duração máxima de uma mensagem.

> **Dica**
>
> É altamente recomendável no início da instalação ter uma relação entre nós do setor e nós nas baterias de 2/3, para ter uma boa malha de rede. Favorecer os micromódulos aos plugues inteligentes. Os micródulos estarão em um local final e não serão desconectados, eles também geralmente têm um alcance melhor. Um bom começo é a iluminação de áreas comuns. Isso permitirá que você distribua adequadamente os módulos do setor em locais estratégicos da sua casa. Em seguida, você pode adicionar quantos módulos na pilha desejar, se suas rotas básicas forem boas.

> **Dica**
>
> O **Gráfico de rede** bem como o **Tabela de roteamento** permitem visualizar a qualidade da sua rede.

> **Dica**
>
> Existem módulos repetidores para preencher áreas em que nenhum módulo setorial é útil.

## Propriedades dos dispositivos Z-Wave

|  | Vizinhos | Estrada | Funções possíveis |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controlador | Conhece todos os vizinhos | Tem acesso à tabela de roteamento completa | Pode se comunicar com todos os dispositivos da rede, se houver um canal |
| Escravo | Conhece todos os vizinhos | Não possui informações na tabela de roteamento | Não é possível responder ao nó que recebeu a mensagem. Portanto, não é possível enviar mensagens não solicitadas |
| Escravos de roteamento | Conhece todos os seus vizinhos | Com conhecimento parcial da tabela de roteamento | Pode responder ao nó do qual recebeu a mensagem e pode enviar mensagens não solicitadas para vários nós |

Em resumo:

-   Cada dispositivo Z-Wave pode receber e reconhecer mensagens
-   Les contrôleurs peuvent envoyer des messages à tous les nœuds du réseau, sollicités onde non « O maître peut parler quand il veut e à qui il veut »
-   Les esclaves ne peuvent pas envoyer des messages non sollicités, mais seulement une réponse aux demandes «L'esclave ne parle que si on le lui demande »
-   Les esclaves de routage peuvent répondre à des demandes e ils sont autorisés à envoyer des messages non sollicités à certains nœuds que le contrôleur a prédéfini « L'esclave est toujours un esclave, mais sur autorisation, il peut parler »

# Configuração do plugin

Depois de baixar o plugin, você só precisa ativá-lo e configurá-lo.

![configuration01](../images/configuration01.png)

Uma vez ativado, o demônio deve lançar. O plug-in é pré-configurado com valores padrão; você normalmente não tem mais nada a fazer. No entanto, você pode alterar a configuração.

## Dependências

Esta parte permite validar e instalar as dependências necessárias para o bom funcionamento do plugin Zwave (local e remotamente, aqui localmente) ![configuration02](../images/configuration02.png)

-   Estatuto **Ok** confirma que as dependências foram atendidas.
-   Se o status for **NOK**, dependências terão que ser reinstaladas usando o botão ![configuration03](../images/configuration03.png)

> **Dica**
>
> A atualização de dependências pode levar mais de 20 minutos, dependendo do seu hardware. O progresso é exibido em tempo real e um log **Openzwave\_update** está acessível.

> **IMPORTANTE**
>
> A atualização de dependências normalmente deve ser executada apenas se o Status for **NOK**, no entanto, é possível, resolver certos problemas, ser chamado para refazer a instalação de dependências.

> **Dica**
>
> Se você estiver no modo remoto, as dependências do daemon local podem ser NOK, isso é completamente normal.

## Demônio

Esta parte permite validar o estado atual do (s) daemon (s) e configurar o gerenciamento automático deles. ![configuration04](../images/configuration04.png) O demônio local e todos os demônios deportados serão exibidos com suas informações diferentes

-   O **Estado** indica que o demônio está atualmente em execução.
-   O **Configuração** indica se a configuração do daemon é válida.
-   O botão **(Re) iniciar** permite forçar o reinício do plug-in, no modo normal ou iniciá-lo pela primeira vez.
-   O botão **Preso**, visível apenas se o gerenciamento automático estiver desativado, força o demônio a parar.
-   O **Gerenciamento automático** permite que o Jeedom inicie o daemon automaticamente quando o Jeedom for iniciado, bem como reinicie-o no caso de um problema.
-   O **último lançamento** é como o nome indica a data do último lançamento conhecido do demônio.

## Log

Esta parte permite escolher o nível do log e consultar seu conteúdo.

![configuration05](../images/configuration05.png)

Selecione o nível e salve; o daemon será reiniciado com as instruções e os rastreios selecionados.

O nível **Depurar** onde **Informações** pode ser útil para entender por que o demônio planta ou não sobe um valor.

> **IMPORTANTE**
>
> No modo **Depurar** o demônio é muito detalhado, é recomendável usar esse modo apenas se você precisar diagnosticar um problema específico. Não é recomendado deixar o demônio correr enquanto **Depurar** permanentemente, se usarmos um **Cartão SD**. Quando a depuração terminar, não se esqueça de retornar a um nível inferior, como o nível **Erro** que remonta apenas a possíveis erros.

## Configuration

Esta parte permite que você configure os parâmetros gerais do plugin ![configuration06](../images/configuration06.png)

-   **Geral** :
    -   **Remover automatiquement les périphériques exclus** :A opção Sim permite excluir dispositivos excluídos da rede Z-Wave. A opção Não permite manter o equipamento no Jeedom, mesmo que ele tenha sido excluído da rede. O equipamento
        terá que ser excluído manualmente ou reutilizado atribuindo a ele um novo ID do Z-Wave se você estiver migrando do controlador principal.
    -   **Aplique o conjunto de configurações recomendado para inclusão** : opção para aplicar diretamente o conjunto de configurações recomendado pela equipe Jeedom para inclusão (recomendado)
    -   **Desativar a atualização em segundo plano das unidades** : Não solicite atualização de unidades em segundo plano.
    -   **Ciclo (s)** : permite definir a frequência de elevadores para jeedom.
    -   **Porta de chave Z-Wave** : a porta USB na qual sua interface Z-Wave está conectada. Se você usa o Razberry, possui, dependendo da sua arquitetura (RPI ou Jeedomboard), as 2 possibilidades no final da lista.
    -   **Porta do servidor** (modificação perigosa, deve ter o mesmo valor em todos os Jeedoms remotos Z-Wave) : permite modificar a porta de comunicação interna do daemon.
    -   **Backups** : permite gerenciar backups do arquivo de topologia de rede (veja abaixo)
    -   **Módulos de configuração** : permite recuperar, manualmente, os arquivos de configuração do OpenZWave com os parâmetros dos módulos, bem como a definição dos comandos dos módulos para seus usos.

        > **Dica**
        >
        > As configurações do módulo são recuperadas automaticamente todas as noites.

        > **Dica**
        >
        > Reiniciar o daemon após atualizar as configurações do módulo é inútil.

        > **IMPORTANTE**
        >
        > Se você possui um módulo não reconhecido e uma atualização de configuração acaba de ser aplicada, você pode iniciar manualmente a recuperação das configurações do módulo.

Depois que as configurações forem recuperadas, dependendo das alterações feitas:

-   Para um novo módulo sem configuração ou controle : excluir e incluir novamente o módulo.
-   Para um módulo para o qual apenas os parâmetros foram atualizados : inicie a regeneração da detecção do nó, na guia Actions do módulo (o plugin deve reiniciar).
-   Pour un module dont le « mapping » de commandes a été corrigé : a lupa nos controles, veja abaixo.

    > **Dica**
    >
    > Em caso de dúvida, é recomendável excluir e incluir novamente o módulo.

Não esqueça de ![configuration08](../images/configuration08.png) se você fizer uma mudança.

> **IMPORTANTE**
>
> Se você estiver usando o Ubuntu : Para que o daemon funcione, você deve ter o ubuntu 15.04 (as versões inferiores possuem um erro e o daemon não pode ser iniciado). Tenha cuidado se você atualizar a partir de 14.04 leva uma vez em 15.04 reiniciar a instalação de dependências.

> **IMPORTANTE**
>
> Selecionando a porta de chave Z-Wave no modo de detecção automática, **Carro**, só funciona para dongles USB.

## Painel Móvel

![configuration09](../images/configuration09.png)

Permite exibir ou não o painel móvel quando você usa o aplicativo em um telefone.

# Configuração do equipamento

A configuração do equipamento Z-Wave pode ser acessada no menu do plug-in :

![appliance01](../images/appliance01.png)

Abaixo um exemplo de uma página de plug-in do Z-Wave (apresentada com alguns equipamentos) :

![appliance02](../images/appliance02.png)

> **Dica**
>
> Como em muitos lugares do Jeedom, posicionar o mouse na extremidade esquerda permite que um menu de acesso rápido apareça (você pode, a partir do seu perfil, deixá-lo sempre visível).

> **Dica**
>
> Os botões na linha superior **Sincronizar**, **Rede Zwave** e **Saúde**, são visíveis apenas se você estiver no modo **Especialista**. ![appliance03](../images/appliance03.png)

## Geral

Aqui você encontra toda a configuração do seu equipamento :

![appliance04](../images/appliance04.png)

-   **Nome de equipamentos** : nome do seu módulo Z-Wave.
-   **Objeto pai** : indica o objeto pai ao qual o equipamento pertence.
-   **Categoria** : categorias de equipamentos (pode pertencer a várias categorias).
-   **Ativar** : torna seu equipamento ativo.
-   **Visivél** : torna visível no painel.
-   **ID do nó** : ID do módulo na rede Z-Wave. Isso pode ser útil se, por exemplo, você quiser substituir um módulo com defeito. Basta incluir o novo módulo, recuperar seu ID e colocá-lo no lugar do ID do módulo antigo e, finalmente, excluir o novo módulo.
-   **Módulo** : esse campo aparece apenas se houver diferentes tipos de configuração para o seu módulo (caso de módulos que podem fazer fios piloto, por exemplo). Permite escolher a configuração a ser usada ou modificada posteriormente

-   **Fazer** : fabricante do seu módulo Z-Wave.
-   **Configuração** : janela de configuração do módulo
-   **Assistente** : disponível apenas em determinados módulos, ele ajuda a configurar o módulo (estojo no teclado zipato, por exemplo)
-   **Documentação** : esse botão permite abrir diretamente a documentação do Jeedom referente a este módulo.
-   **Remover** : Permite excluir um item de equipamento e todos esses comandos anexados sem excluí-lo da rede Z-Wave.

> **IMPORTANTE**
>
> A exclusão do equipamento não leva à exclusão do módulo do controlador. ![appliance11](../images/appliance11.png) O equipamento excluído que ainda estiver conectado ao seu controlador será recriado automaticamente após a sincronização.

## Commandes

Abaixo você encontra a lista de pedidos :

![appliance05](../images/appliance05.png)

> **Dica**
>
> Dependendo dos tipos e subtipos, algumas opções podem estar ausentes.

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
-   "Valor do feedback do status "e" Duração antes do feedback do status" : permite indicar a Jeedom que após uma alteração nas informações, seu valor deve retornar a Y, X min após a alteração. Exemplo : no caso de um detector de presença que emite apenas durante uma detecção de presença, é útil definir, por exemplo, 0 em valor e 4 em duração, de modo que 4 minutos após uma detecção de movimento (e se , não havia novos) Jeedom redefine o valor das informações para 0 (mais movimento detectado).
-   Historicizar : permite historiar os dados.
-   Display : permite exibir os dados no painel.
-   Inverter : permite inverter o estado para tipos binários.
-   Unidade : unidade de dados (pode estar vazia).
-   Min / max : limites de dados (podem estar vazios).
-   Configuração avançada (pequenas rodas dentadas) : exibe a configuração avançada do comando (método de registro, widget etc.).

-   Teste : permite testar o comando.
-   Excluir (assinar -) : permite excluir o comando.

> **IMPORTANTE**
>
> O botão **Teste** no caso de um comando do tipo Info, não consultará o módulo diretamente, mas o valor disponível no cache Jeedom. O teste retornará o valor correto apenas se o módulo em questão tiver transmitido um novo valor correspondente à definição do comando. Portanto, é completamente normal não obter um resultado após a criação de um novo comando Info, especialmente em um módulo alimentado por bateria que raramente notifica o Jeedom.

O **lupa**, disponível na guia geral, permite recriar todos os comandos do módulo atual. ![appliance13](../images/appliance13.png) Se nenhum comando estiver presente ou se os comandos estiverem errados, a lupa deve remediar a situação.

> **IMPORTANTE**
>
> O **lupa** excluirá os pedidos existentes. Se os comandos foram usados em cenários, você precisará corrigi-los nos outros locais onde os comandos foram usados.

## Jogos de Comando

Alguns módulos possuem vários conjuntos de comandos pré-configurados

![appliance06](../images/appliance06.png)

Você pode selecioná-los através das opções possíveis, se o módulo permitir.

> **IMPORTANTE**
>
> Você deve ampliar para aplicar os novos conjuntos de comandos.

## Documentação e Assistente

Para um certo número de módulos, estão disponíveis ajuda específica para a instalação e recomendações de parâmetros.

![appliance07](../images/appliance07.png)

O botão **Documentação** fornece acesso a documentação específica do módulo para Jeedom.

Módulos específicos também têm um assistente específico para facilitar a aplicação de determinados parâmetros ou operações.

O botão **Assistente** dá acesso à tela de assistente específica do módulo.

## Configuração recomendada

![appliance08](../images/appliance08.png)

Aplique um conjunto de configurações recomendado pela equipe Jeedom.

> **Dica**
>
> Quando incluídos, os módulos possuem os parâmetros padrão do fabricante e certas funções não são ativadas por padrão.

Os seguintes elementos, conforme aplicável, serão aplicados para simplificar o uso do módulo.

-   **Configurações** permitindo comissionamento rápido de todas as funcionalidades do módulo.
-   **Grupos d'association** necessário para o funcionamento adequado.
-   **Intervalo de despertar**, para módulos com bateria.
-   Ativação de **atualização manual** para módulos que não sobem sozinhos, seu estado muda.

Para aplicar o conjunto de configurações recomendado, clique no botão : **Configuração recommandée**, depois confirme a aplicação das configurações recomendadas.

![appliance09](../images/appliance09.png)

O assistente ativa os vários elementos de configuração.

Uma confirmação do bom andamento será exibida na forma de um banner

![appliance10](../images/appliance10.png)

> **IMPORTANTE**
>
> Os módulos de bateria devem ser despertados para aplicar o conjunto de configurações.

A página do equipamento informa se os elementos ainda não foram ativados no módulo. Consulte a documentação do módulo para ativá-lo manualmente ou aguarde o próximo ciclo de ativação.

![appliance11](../images/appliance11.png)

> **Dica**
>
> É possível ativar automaticamente a aplicação do conjunto de configurações recomendado ao incluir um novo módulo, consulte a seção Configuração do plug-in para obter mais detalhes.

# Configuração de módulos

É aqui que você encontrará todas as informações sobre seu módulo

![node01](../images/node01.png)

A janela possui várias guias :

## Resumo

Fornece um resumo completo do seu nó com várias informações, como o status das solicitações, que permitem saber se o nó está aguardando informações ou a lista de nós vizinhos.

> **Dica**
>
> Nesta guia, é possível receber alertas em caso de possível detecção de um problema de configuração, o Jeedom informará o procedimento a seguir para corrigir. Não confunda um alerta com um erro, na maioria dos casos, o alerta é uma recomendação simples.

## Valeurs

![node02](../images/node02.png)

Você encontrará aqui todos os comandos e estados possíveis em seu módulo. Eles são ordenados por instância e classe de comando e indexam. O « mapping » des commandes est entièrement basé sur ces informations.

> **Dica**
>
> Forçar atualização de um valor. Os módulos da bateria atualizarão um valor somente no próximo ciclo de ativação. No entanto, é possível ativar manualmente um módulo, consulte a documentação do módulo.

> **Dica**
>
> É possível ter mais pedidos aqui do que no Jeedom, isso é completamente normal. No Jeedom, os pedidos foram pré-selecionados para você.

> **IMPORTANTE**
>
> Alguns módulos não enviam seus estados automaticamente; nesse caso, é necessário ativar a atualização manual em 5 minutos no (s) valor (es) desejado (s). É recomendável deixar a atualização automaticamente. O abuso da atualização manual pode afetar fortemente o desempenho da rede Z-Wave, use apenas os valores recomendados na documentação específica do Jeedom. ![node16](../images/node16.png) O conjunto de valores (índice) da instância de um comando de classe será remontado, ativando a atualização manual no menor índice da instância do comando de classe. Repita para cada instância, se necessário.

## Configurações

![node03](../images/node03.png)

Aqui você encontrará todas as possibilidades para configurar os parâmetros do seu módulo, bem como a possibilidade de copiar a configuração de outro nó já existente.

Quando um parâmetro é modificado, a linha correspondente fica amarela, ![node04](../images/node04.png) a configuração está aguardando para ser aplicada.

Se o módulo aceitar o parâmetro, a linha se tornará transparente novamente.

Se, no entanto, o módulo recusar o valor, a linha ficará vermelha com o valor aplicado retornado pelo módulo. ![node05](../images/node05.png)

Na inclusão, um novo módulo é detectado com as configurações padrão do fabricante. Em alguns módulos, as funcionalidades não estarão ativas sem modificar um ou mais parâmetros. Consulte a documentação do fabricante e nossas recomendações para configurar corretamente seus novos módulos.

> **Dica**
>
> Os módulos de bateria aplicarão alterações de parâmetro apenas no próximo ciclo de ativação. No entanto, é possível ativar manualmente um módulo, consulte a documentação do módulo.

> **Dica**
>
> A ordem **Retomar de** permite retomar a configuração de outro módulo idêntico, no módulo atual.

![node06](../images/node06.png)

> **Dica**
>
> A ordem **Aplicar em** permite aplicar a configuração atual do módulo a um ou mais módulos idênticos.

![node18](../images/node18.png)

> **Dica**
>
> A ordem **Atualizar configurações** força o módulo a atualizar os parâmetros salvos no módulo.

Se nenhum arquivo de configuração estiver definido para o módulo, um assistente manual permitirá aplicar parâmetros ao módulo. ![node17](../images/node17.png) Consulte a documentação do fabricante para obter a definição do índice, valor e tamanho.

##Associations

É aqui que você encontra o gerenciamento dos grupos de associação do seu módulo.

![node07](../images/node07.png)

Os módulos Z-Wave podem controlar outros módulos Z-Wave, sem passar pelo controlador ou Jeedom. O relacionamento entre um módulo de controle e outro módulo é chamado de associação.

Para controlar outro módulo, o módulo de comando precisa manter uma lista de dispositivos que receberão o controle de comando. Essas listas são chamadas de grupos de associação e estão sempre vinculadas a determinados eventos (por exemplo, o botão pressionado, o sensor é acionado etc.).

No caso de um evento, todos os dispositivos registrados no grupo de associação em questão receberão um comando Básico.

> **Dica**
>
> Consulte a documentação do módulo para entender os diferentes grupos de possíveis associações e seu comportamento.

> **Dica**
>
> A maioria dos módulos possui um grupo de associação que é reservado para o controlador principal, usado para enviar informações ao controlador. É geralmente chamado : **Relatório** onde **LifeLine**.

> **Dica**
>
> Seu módulo pode não ter nenhum grupo.

> **Dica**
>
> A modificação dos grupos de associação de um módulo de bateria será aplicada ao próximo ciclo de ativação. No entanto, é possível ativar manualmente um módulo, consulte a documentação do módulo.

Para saber a quais outros módulos o módulo atual está associado, basta clicar no menu **Associado a quais módulos**

![node08](../images/node08.png)

Todos os módulos que usam o módulo atual, bem como o nome dos grupos de associação, serão exibidos.

**Associações multi-instances**

Algum módulo suporta um comando de classe de associações de várias instâncias. Quando um módulo suporta esse CC, é possível especificar com qual instância se deseja criar a associação

![node09](../images/node09.png)

> **IMPORTANTE**
>
> Alguns módulos devem estar associados à instância 0 do controlador principal para funcionar corretamente. Por esse motivo, o controlador está presente com e sem a instância 0.

## Sistemas

Tabulação agrupando os parâmetros do sistema do módulo.

![node10](../images/node10.png)

> **Dica**
>
> Os módulos de bateria são ativados em ciclos regulares, chamados Wakeup Interval. O intervalo de ativação é um compromisso entre a duração máxima da bateria e as respostas desejadas do dispositivo. Para maximizar a vida útil de seus módulos, adapte o valor do Intervalo de ativação, por exemplo, a 14.400 segundos (4h), veja ainda mais, dependendo dos módulos e de seu uso. ![node11](../images/node11.png)

> **Dica**
>
> Os módulos **Switch** e **Dimmer** pode implementar uma classe de comando especial chamada **SwitchAll** 0x27. Você pode mudar o comportamento aqui. Dependendo do módulo, várias opções estão disponíveis. A ordem **SwitchAll On/OFF** pode ser iniciado através do seu módulo controlador principal.

## Actions

Permite que você execute determinadas ações no módulo.

![node12](../images/node12.png)

Certas ações serão ativadas de acordo com o tipo de módulo e suas possibilidades ou de acordo com o estado atual do módulo, como se ele fosse considerado morto pelo controlador.

> **IMPORTANTE**
>
> Não use ações em um módulo se você não souber o que está fazendo. Algumas ações são irreversíveis. As ações podem ajudar a resolver problemas com um ou mais módulos Z-Wave.

> **Dica**
>
> O **Regeneração da detecção de nó** permite detectar o módulo para aceitar os últimos conjuntos de parâmetros. Essa ação é necessária quando você for informado de que uma atualização de parâmetros e / ou comportamento do módulo é necessária para o funcionamento adequado. A regeneração da detecção do nó implica um reinício da rede, o assistente realiza automaticamente.

> **Dica**
>
> Se você possui vários módulos idênticos, necessários para executar o **Regeneração da detecção de nó**, é possível iniciá-lo uma vez para todos os módulos idênticos.

![node13](../images/node13.png)

> **Dica**
>
> Se um módulo em uma pilha não estiver mais acessível e você quiser excluí-lo, e a exclusão não ocorrer, você poderá iniciar **Remover le noeud fantôme** Um assistente executará várias ações para remover o chamado módulo fantasma. Essa ação envolve reiniciar a rede e pode levar alguns minutos para ser concluída.

![node14](../images/node14.png)

Depois de iniciado, é recomendável fechar a tela de configuração do módulo e monitorar a exclusão do módulo através da tela de integridade do Z-Wave.

> **IMPORTANTE**
>
> Somente módulos na bateria podem ser excluídos através deste assistente.

## Statistiques

Essa guia fornece algumas estatísticas de comunicação com o nó.

![node15](../images/node15.png)

Pode ser interessante no caso de módulos que são considerados mortos pelo controlador "Dead".

# Inclusão / exclusão

Quando sai da fábrica, um módulo não pertence a nenhuma rede Z-Wave.

## Inclusão moda

O módulo deve ingressar em uma rede Z-Wave existente para se comunicar com os outros módulos desta rede. Esse processo é chamado **Inclusão**. Os dispositivos também podem deixar uma rede. Esse processo é chamado **Exclusão**. Ambos os processos são iniciados pelo controlador principal da rede Z-Wave.

![addremove01](../images/addremove01.png)

Este botão permite alternar para o modo de inclusão para adicionar um módulo à sua rede Z-Wave.

Você pode escolher o modo de inclusão depois de clicar no botão
**Inclusão**.

![addremove02](../images/addremove02.png)

Desde o surgimento do Z-Wave +, é possível garantir trocas entre o controlador e os nós. Portanto, é recomendável fazer as inclusões no modo **Seguro**.

Se, no entanto, um módulo não puder ser incluído no modo seguro, inclua-o no modo seguro **Não seguro**.

Uma vez no modo de inclusão : Jeedom diz a você.

>**Dica**
>
>Um módulo 'não seguro' pode solicitar módulos 'não seguros''. Um módulo 'não seguro' não pode solicitar um módulo 'seguro''. Um módulo 'seguro' pode solicitar módulos 'não seguros', desde que o transmissor o suporte.

![addremove03](../images/addremove03.png)

Depois que o assistente é iniciado, você deve fazer o mesmo no seu módulo (consulte a documentação para mudar para o modo de inclusão).

> **Dica**
>
> Contanto que você não tenha o banner, você não está no modo de inclusão.

Se você clicar no botão novamente, sair do modo de inclusão.

> **Dica**
>
> É recomendável, antes da inclusão de um novo módulo que seria "novo" no mercado, lançar o pedido **Módulos de configuração** através da tela de configuração do plugin. Esta ação recuperará todas as versões mais recentes dos arquivos de configuração do openzwave, bem como o mapeamento de comandos do Jeedom.

> **IMPORTANTE**
>
> Durante uma inclusão, é aconselhável que o módulo esteja próximo ao controlador principal ou a menos de um metro da sua jeedom.

> **Dica**
>
> Alguns módulos requerem uma inclusão no modo **Seguro**, por exemplo, para fechaduras de portas.

> **Dica**
>
> Observe que a interface móvel também fornece acesso à inclusão, o painel móvel deve ter sido ativado.

> **Dica**
>
> Se o módulo já pertence a uma rede, siga o processo de exclusão antes de incluí-lo na sua rede. Caso contrário, a inclusão deste módulo falhará. Também é recomendável executar uma exclusão antes da inclusão, mesmo que o produto seja novo, pronto para uso.

> **Dica**
>
> Uma vez que o módulo esteja em sua localização final, é necessário iniciar a ação para cuidar da rede, a fim de solicitar a todos os módulos que atualizem todos os vizinhos.

## Modo de exclusão

![addremove04](../images/addremove04.png)

Este botão permite alternar para o modo de exclusão, para remover um módulo da sua rede Z-Wave, você deve fazer o mesmo com o seu módulo (consulte a documentação para alterá-lo para o modo de exclusão).

![addremove05](../images/addremove05.png)

> **Dica**
>
> Contanto que você não tenha o banner, você não está no modo de exclusão.

Se você clicar no botão novamente, sairá do modo de exclusão.

> **Dica**
>
> Observe que a interface móvel também fornece acesso à exclusão.

> **Dica**
>
> Um módulo não precisa ser excluído pelo mesmo controlador no qual foi incluído anteriormente. Daí o fato de ser recomendado executar uma exclusão antes de cada inclusão.

## Synchroniser

![addremove06](../images/addremove06.png)

Botão que permite sincronizar os módulos de rede Z-Wave com o equipamento Jeedom. Os módulos são associados ao controlador principal, os dispositivos no Jeedom são criados automaticamente quando são incluídos. Eles também são excluídos automaticamente quando excluídos, se a opção **Remover automatiquement les périphériques exclus** está ativado.

Se você incluiu módulos sem o Jeedom (requer um dongle de bateria como o Aeon-labs Z-Stick GEN5), a sincronização será necessária após a conexão da chave, assim que o daemon for iniciado e estiver operacional.

> **Dica**
>
> Se você não possui a imagem ou o Jeedom não reconheceu seu módulo, esse botão pode ser usado para corrigir (desde que a entrevista do módulo esteja concluída).

> **Dica**
>
> Se na sua tabela de roteamento e / ou na tela de integridade do Z-Wave, você tiver um ou mais módulos nomeados com seus respectivos **nome genérico**, sincronização remediará esta situação.

O botão Sincronizar é visível apenas no modo especialista :
![addremove07](../images/addremove07.png)

# Redes Z-Wave

![network01](../images/network01.png)

Aqui você encontrará informações gerais sobre sua rede Z-Wave.

![network02](../images/network02.png)

## Resumo

A primeira guia fornece o resumo básico da sua rede Z-Wave, você encontrará, em particular, o status da rede Z-Wave, bem como o número de elementos na fila.

**Informação**

-   Fornece informações gerais sobre a rede, a data de início, o tempo necessário para obter a rede no chamado estado funcional.
-   O número total de nós na rede, bem como o número que está inativo no momento.
-   O intervalo de solicitação está associado à atualização manual. É predefinido no mecanismo Z-Wave em 5 minutos.
-   Os vizinhos do controlador.

**Estado**

![network03](../images/network03.png)

Um conjunto de informações sobre o estado atual da rede, nomeadamente :

-   Estado atual, talvez **Driver Inicializado**, **Topologia carregada** onde **Pronto**.
-   Fila de saída, indica o número de mensagens na fila no controlador aguardando para serem enviadas. Esse valor geralmente é alto durante a inicialização da rede quando o status ainda está em **Driver Inicializado**.

Quando a rede atingir pelo menos **Topologia carregada**, Se os mecanismos internos do servidor Z-Wave forçarem atualizações de valores, é, portanto, completamente normal ver o número de mensagens aumentar. Isso retornará rapidamente para 0.

> **Dica**
>
> Diz-se que a rede está funcional quando atinge o status **Topologia carregada**, isto é, todos os nós do setor concluíram suas entrevistas. Dependendo do número de módulos, da distribuição da bateria / setor, da escolha do dongle USB e do PC no qual o plug-in Z-Wave está sendo executado, a rede alcançará esse estado entre um e cinco minutos.

Uma rede **Pronto**, significa que todos os nós do setor e da bateria concluíram sua entrevista.

> **Dica**
>
> Dependendo dos módulos que você possui, a rede pode nunca atingir o status sozinha **Pronto**. Os controles remotos, por exemplo, não acordam sozinhos e nunca terminam sua entrevista. Nesse tipo de caso, a rede está totalmente operacional e, mesmo que os controles remotos não tenham concluído sua entrevista, eles garantem sua funcionalidade dentro da rede.

**Capacidades**

Usado para descobrir se o controlador é um controlador primário ou secundário.

**Sistema**

Exibe várias informações do sistema.

-   Informações sobre a porta USB usada.
-   Versão da biblioteca OpenZwave
-   Versão da biblioteca Python-OpenZwave

## Actions

![network05](../images/network05.png)

Aqui você encontrará todas as ações possíveis para toda a sua rede Z-Wave. Cada ação é acompanhada de uma breve descrição.

> **IMPORTANTE**
>
> Certas ações são realmente arriscadas ou até irreversíveis; a equipe da Jeedom não pode ser responsabilizada no caso de manuseio inadequado.

> **IMPORTANTE**
>
> Alguns módulos requerem inclusão no modo seguro, por exemplo, para trancas de portas. A inclusão segura deve ser iniciada por meio da ação nesta tela.

> **Dica**
>
> Se uma ação não puder ser iniciada, ela será desativada até que possa ser executada novamente.

## Statistiques

![network06](../images/network06.png)

Aqui você encontrará estatísticas gerais de toda a sua rede Z-Wave.

## Gráfico de rede

![network07](../images/network07.png)

Essa guia fornece uma representação gráfica dos diferentes links entre os nós.

Explicação da legenda da cor :

-   **Preto** : O controlador principal, geralmente representado como Jeedom.
-   **Verde** : Comunicação direta com o controlador, ideal.
-   **Azul** : Para controladores, como controles remotos, eles estão associados ao controlador primário, mas não têm vizinhos.
-   **Amarelo** : Todas as estradas têm mais de um salto antes de chegar ao controlador.
-   **Cinza** : A entrevista ainda não está concluída, os links serão realmente conhecidos quando a entrevista for concluída.
-   **Vermelho** : presumidamente morto, ou sem um vizinho, não participa / não mais da rede da rede.

> **Dica**
>
> Somente equipamentos ativos serão exibidos no gráfico de rede.

A rede Z-Wave consiste em três tipos diferentes de nós com três funções principais.

A principal diferença entre os três tipos de nós é o conhecimento da tabela de roteamento de rede e, posteriormente, a capacidade de enviar mensagens para a rede.

## Tabela de roteamento

Cada nó é capaz de determinar quais outros nós estão em comunicação direta. Esses nós são chamados vizinhos. Durante a inclusão e / ou posteriormente mediante solicitação, o nó pode informar o controlador da lista de vizinhos. Graças a essas informações, o controlador é capaz de criar uma tabela com todas as informações sobre as rotas de comunicação possíveis em uma rede.

![network08](../images/network08.png)

As linhas da tabela contêm os nós de origem e as colunas contêm os nós de destino. Consulte a legenda para entender as cores das células que indicam os links entre dois nós.

Explicação da legenda da cor :

-   **Verde** : Comunicação direta com o controlador, ideal.
-   **Azul** : Pelo menos 2 rotas com um salto.
-   **Amarelo** : Menos de 2 rotas com um salto.
-   **Cinza** : A entrevista ainda não está concluída, na verdade será atualizada assim que a entrevista for concluída.
-   **Laranja** : Todas as estradas têm mais de um salto. Pode causar latências.

> **Dica**
>
> Somente equipamentos ativos serão exibidos no gráfico de rede.

> **IMPORTANTE**
>
> Um módulo supostamente morto, não participa / não mais da rede da rede. Será marcado aqui com um ponto de exclamação vermelho em um triângulo.

> **Dica**
>
> Você pode iniciar manualmente a atualização do vizinho, por módulo ou para toda a rede, usando os botões disponíveis na tabela de roteamento.

# Santé

![health01](../images/health01.png)

Esta janela resume o status da sua rede Z-Wave :

![health02](../images/health02.png)

Você tem aqui :

-   **Módulo** : o nome do seu módulo, clique nele para acessá-lo diretamente.
-   **ID** : ID do seu módulo na rede Z-Wave.
-   **Notificação** : último tipo de troca entre o módulo e o controlador
-   **Grupo** : indica se a configuração do grupo está correta (controlador pelo menos em um grupo). Se você não tem nada, é que o módulo não suporta a noção de grupo, é normal
-   **Fabricante** : indica se a recuperação das informações de identificação do módulo está correta
-   **Vizinho** : indica se a lista de vizinhos foi recuperada
-   **Estado** : Indica o status da entrevista do módulo (estágio de consulta)
-   **Bateria** : nível da bateria do módulo (um plugue de rede indica que o módulo é alimentado pela rede elétrica).
-   **Hora de acordar** : para módulos com bateria, fornece a frequência em segundos dos instantes em que o módulo é ativado automaticamente.
-   **Pacote total** : exibe o número total de pacotes recebidos ou enviados com sucesso para o módulo.
-   **% Ok** : exibe a porcentagem de pacotes enviados / recebidos com sucesso.
-   **Atraso de tempo** : exibe o atraso médio do envio de pacotes em ms.
-   **Última notificação** : Data da última notificação recebida do módulo e a hora da próxima ativação agendada, para os módulos que dormem.
    -   Também permite informar se o nó não acordou uma vez desde o lançamento do daemon.
    -   E indica se um nó não acordou como esperado.
-   **Ping** : Permite enviar uma série de mensagens ao módulo para testar seu funcionamento adequado.

> **IMPORTANTE**
>
> O equipamento desativado será exibido, mas nenhuma informação de diagnóstico estará presente.

O nome do módulo pode ser seguido por uma ou duas imagens:

![health04](../images/health04.png) Modules supportant la COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../images/health05.png) Modules supportant la COMMAND\_CLASS\_SECURITY e securisé.

![health06](../images/health06.png) Modules supportant la COMMAND\_CLASS\_SECURITY e non Seguro.

![health07](../images/health07.png) Módulo FLiRS, routeurs esclaves (modules à piles) à écoute fréquente.

> **Dica**
>
> O comando Ping pode ser usado se o módulo for considerado morto "DEATH" para confirmar se esse é realmente o caso.

> **Dica**
>
> Os módulos adormecidos só responderão ao Ping na próxima vez que acordarem.

> **Dica**
>
> A notificação de tempo limite não significa necessariamente um problema com o módulo. Inicie um ping e, na maioria dos casos, o módulo responderá com uma notificação **NoOperation** o que confirma um retorno proveitoso do ping.

> **Dica**
>
> O atraso e% de OK nos nós com baterias antes da conclusão da entrevista não são significativos. Na verdade, o nó não responderá aos interrogatórios do controlador sobre o fato de estar em sono profundo.

> **Dica**
>
> O servidor Z-Wave cuida automaticamente do lançamento de testes nos módulos no Timeout após 15 minutos

> **Dica**
>
> O servidor Z-Wave tenta remontar automaticamente os módulos que são considerados mortos.

> **Dica**
>
> Um alerta será enviado para Jeedom se o módulo for considerado morto. Você pode ativar uma notificação para ser informado o mais rápido possível. Veja a configuração de mensagens na tela de configuração do Jeedom.

![health03](../images/health03.png)

> **Dica**
>
> Se na sua tabela de roteamento e / ou na tela de integridade do Z-Wave você tiver um ou mais módulos nomeados com seus respectivos **nome genérico**, sincronização remediará esta situação.

> **Dica**
>
> Se na sua tabela de roteamento e / ou na tela de integridade do Z-Wave você tiver um ou mais módulos denominados **Desconhecido**, isso significa que a entrevista do módulo não foi concluída com êxito. Você provavelmente tem um **NOK** na coluna do construtor. Abra os detalhes do (s) módulo (s), para experimentar as soluções sugeridas (consulte a seção Solução de problemas e diagnóstico, abaixo).

## Status da entrevista

Etapa de entrevistar um módulo após iniciar o daemon.

-   **Nenhuma** Inicialização do processo de procura do nó.
-   **ProtocolInfo** Recupere informações de protocolo, se este nó estiver escutando (ouvinte), sua velocidade máxima e suas classes de dispositivos.
-   **Sonda** Faça ping no módulo para ver se está ativado.
-   **WakeUp** Inicie o processo de ativação, se for um nó em suspensão.
-   **FabricanteSpecific1** Recupere o nome do fabricante e os IDs do produto se ProtocolInfo permitir.
-   **NodeInfo** Recuperar informações sobre o suporte de classes de comando suportadas.
-   **NodePlusInfo** Recupere informações do ZWave + sobre suporte para classes de comando suportadas.
-   **SecurityReport** Recupere a lista de classes de pedidos que requerem segurança.
-   **FabricanteSpecific2** Recupere o nome do fabricante e os identificadores do produto.
-   **Versões** Recuperar informações da versão.
-   **Instâncias** Recuperar informações da classe de comando de várias instâncias.
-   **Estático** Recuperar informações estáticas (não muda).
-   **CacheLoad** Efetue ping no módulo durante a reinicialização com o cache de configuração do dispositivo.
-   **Associações** Recuperar informações sobre associações.
-   **Vizinhos** Recuperar a lista de nós vizinhos.
-   **Sessão** Recuperar informações da sessão (raramente muda).
-   **Dinâmico** Recuperar informações dinâmicas (muda frequentemente).
-   **Configuração** Recuperar informações de parâmetro de configuração (feitas somente mediante solicitação).
-   **Concluir** O processo de entrevista está finalizado para este nó.

## Notification

Detalhes das notificações enviadas pelos módulos

-   **Concluído** Ação concluída com sucesso.
-   **Tempo limite** Atraso no relatório relatado ao enviar uma mensagem.
-   **NoOperation** Relate em um teste do nó (Ping) que a mensagem foi enviada com sucesso.
-   **Desperta** Relatar quando um nó acabou de acordar
-   **Dormir** Relatar quando um nó adormeceu.
-   **Morto** Relatar quando um nó é considerado morto.
-   **Vivo** Relatar quando um nó é relançado.

# Backups

A parte de backup permitirá que você gerencie os backups da sua topologia de rede. Este é o seu arquivo zwcfgxxx.xml, constitui o último estado conhecido da sua rede, é uma forma de cache da sua rede. Nesta tela você pode :

-   Iniciar um backup (um backup é feito a cada reinicialização da rede e durante operações críticas). Os últimos 12 backups são mantidos
-   Restaurar um backup (selecionando-o na lista logo acima)
-   Excluir um backup

![backup01](../images/backup01.png)

# Atualizar o OpenZWave

Após uma atualização do plug-in Z-Wave, é possível que o Jeedom solicite a atualização das dependências do Z-Wave. Uma dependência NOK será exibida:

![update01](../images/update01.png)

> **Dica**
>
> Uma atualização das dependências não deve ser feita com cada atualização do plugin.

O Jeedom deve iniciar a atualização de dependência por si só se o plug-in considerar que eles são **NOK**. Esta validação é realizada após 5 minutos.

A duração desta operação pode variar dependendo do seu sistema (até mais de 1 hora no raspberry pi)

Depois que a atualização das dependências for concluída, o daemon será reiniciado automaticamente após a validação do Jeedom. Esta validação é realizada após 5 minutos.

> **Dica**
>
> Caso a atualização das dependências não seja concluída, consulte o log **Openzwave\_update** quem deve informá-lo sobre o problema.

# Lista de módulos compatíveis

Você encontrará a lista de módulos compatíveis
[aqui](https://doc.jeedom.com/pt_PT/zwave/equipement.compatible)

# Solução de problemas e diagnóstico

## Meu módulo não foi detectado ou não fornece seus identificadores de produto e tipo

![troubleshooting01](../images/troubleshooting01.png)

Inicie a regeneração da detecção de nó na guia Actions do módulo.

Se você tiver vários módulos nesse cenário, inicie **Regenerar a detecção de nós desconhecidos** da tela **Rede Zwave** separador **Estoque**.

## Meu módulo é considerado morto pelo controlador Dead

![troubleshooting02](../images/troubleshooting02.png)

Se o módulo ainda estiver conectado e acessível, siga as soluções propostas na tela do módulo.

Se o módulo foi cancelado ou está com defeito, você pode excluí-lo da rede usando **excluir o nó com erro** via guia **Estoque**.

Se o módulo foi reparado e um novo módulo de substituição foi entregue, você pode iniciar **Substituir nó com falha** via guia **Estoque**, Se o controlador acionar a inclusão, você deverá prosseguir com a inclusão no módulo. O id do módulo antigo será mantido, bem como seus comandos.

## Como usar o comando SwitchAll

![troubleshooting03](../images/troubleshooting03.png)

Está disponível através do nó do seu controlador. Seu controlador deve ter os comandos Switch All On e Switch All Off.

Se o seu controlador não aparecer na sua lista de módulos, inicie a sincronização.

![troubleshooting04](../images/troubleshooting04.png)

Classe Switch All Command geralmente é suportado em switches e drives. Seu comportamento é configurável em cada módulo que o suporta.

Para que possamos:

-   Desativar o comando Switch All Class.
-   Ativar para ativar e desativar.
-   Ativar apenas.
-   Ativar apenas Desativado.

A escolha das opções depende do fabricante.

Portanto, você deve reservar um tempo para revisar todos os seus interruptores / dimmers antes de configurar um cenário, se você não controlar apenas as luzes.

## Meu módulo não possui um comando Cena ou Botão

![troubleshooting05](../images/troubleshooting05.png)

Você pode adicionar o comando na tela de mapeamento de comandos.

Esta é uma ordem **Informações** no CC **0x2b** Instância **0** commande
**dados \ [0 \]. val**

O modo de cena deve ser ativado nas configurações do módulo. Consulte a documentação do seu módulo para obter mais detalhes.

## Forçar valores de atualização

É possível forçar a solicitação para atualizar os valores de uma instância para um comando de classe específico.

É possível fazer isso através de uma solicitação http ou criar um pedido na tela de mapeamento de equipamentos.

![troubleshooting06](../images/troubleshooting06.png)

Esta é uma ordem **Ação** escolha o **CC** desejado para um **Instância** dado com o comando **dados \ [0 \]. ForceRefresh ()**

Todos os índices de instância para este comando Class serão atualizados. Os nós das baterias aguardam seu próximo despertar antes de realizar a atualização de seu valor.

Você também pode usar por script enviando uma solicitação http ao servidor REST Z-Wave.
Substitua ip\_jeedom, node\_id, instance\_id, cc\_id e index

``http://token:\#APIKEY\#@ip\_jeedom:8083/ZWaveAPI/Run/devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()``

## Transfira os módulos para um novo controlador

Por razões diferentes, pode ser necessário transferir todos os seus módulos para um novo controlador principal.

Você decide ir de **raZberry** para um **Z-Stick Gen5** ou porque, você precisa executar uma **Reset** completo do controlador principal.

Aqui estão diferentes etapas para chegar lá sem perder seus valiosos cenários, widgets e histórico:

-   1 \) Faça um backup do Jeedom.
-   2 \) Lembre-se de anotar (screenshot) seus valores de parâmetros para cada módulo, eles serão perdidos após a exclusão.
-   3 \) Na configuração do Z-Wave, desmarque a opção "Excluir automaticamente dispositivos excluídos" e salve. Reinicializações de rede.
-   4a) No caso de um **Reset**, Redefina o controlador principal e reinicie o plug-in.
-   4b) Para um novo controlador, pare o Jeedom, desconecte o antigo e conecte o novo. Iniciar Jeedom.
-   5 \) Para cada dispositivo Z-Wave, altere o ID do ZWave para **0**.
-   6 \) Abra 2 páginas do plugin Z-Wave em diferentes guias.
-   7 \) (Via primeira guia) Vá para a página de configuração de um módulo que você deseja incluir no novo controlador.
-   8 \) (Via segunda guia) Excluir e incluir o módulo. Novos equipamentos serão criados.
-   9 \) Copie o ID do Z-Wave do novo dispositivo e exclua este dispositivo.
-   10 \) Volte à guia do módulo antigo (1ª guia) e cole o novo ID no lugar do antigo ID.
-   11 \) Os parâmetros do ZWave foram perdidos durante a exclusão / inclusão, lembre-se de redefinir seus parâmetros específicos se você não usar os valores padrão.
-   11 \) Repita as etapas 7 a 11 para cada módulo a ser transferido.
-   12 \) No final, você não deve mais ter equipamentos no ID 0.
-   13 \) Verifique se todos os módulos estão nomeados corretamente na tela de integridade do Z-Wave. Inicie a sincronização se não for esse o caso.

## Substitua um módulo defeituoso

Como refazer a inclusão de um módulo com falha sem perder seus cenários, widgets e históricos de valor

Se o módulo for considerado "inoperante"" :

-   Observe (captura de tela) seus valores de parâmetro, eles serão perdidos após a inclusão.
-   Vá para a guia Actions do módulo e ative o comando "Substituir Nó com Falha".
-   O controlador está no modo de inclusão, prossiga para a inclusão de acordo com a documentação do módulo.
-   Redefina seus parâmetros específicos.

Se o módulo não estiver "morto", mas ainda estiver acessível:

-   Na configuração do ZWave, desmarque a opção "Remover automaticamente dispositivos excluídos".
-   Observe (captura de tela) seus valores de parâmetro, eles serão perdidos após a inclusão.
-   Excluir o módulo defeituoso.
-   Vá para a página de configuração do módulo defeituoso.
-   Abra a página de plug-in do ZWave em uma nova guia.
-   Inclua o módulo.
-   Copie o ID do novo módulo e exclua este equipamento.
-   Volte à guia do módulo antigo e cole o novo ID no lugar do antigo ID.
-   Redefina seus parâmetros específicos.

## Remoção do nó fantasma

Se você perdeu toda a comunicação com um módulo de bateria e deseja excluí-lo da rede, é possível que a exclusão não seja bem-sucedida ou que o nó permaneça presente na sua rede.

O assistente automático de nó fantasma está disponível.

-   Vá para a guia Actions do módulo para excluir.
-   Ele provavelmente terá um status **CacheLoad**.
-   Comando Iniciar **Remover nœud fantôme**.
-   A rede Z-Wave para. Assistente automático modifica o arquivo **zwcfg** remover o CC WakeUp do módulo. Reinicializações de rede.
-   Feche a tela do módulo.
-   Abra a tela Z-Wave Health.
-   Aguarde o ciclo de inicialização ser concluído (topologia carregada).
-   O módulo normalmente será marcado como supostamente morto.
-   No próximo minuto, você verá o nó desaparecer da tela de integridade.
-   Se na configuração do Z-Wave, você desmarcou a opção "Excluir automaticamente dispositivos excluídos", será necessário excluir manualmente o equipamento correspondente.

Este assistente está disponível apenas para módulos de bateria.

## Ações pós-inclusão

Recomenda-se realizar a inclusão de pelo menos 1M do controlador principal, ou essa não será a posição final do seu novo módulo. Aqui estão algumas boas práticas a seguir após a inclusão de um novo módulo em sua rede.

Depois que a inclusão estiver concluída, devemos aplicar um certo número de parâmetros ao nosso novo módulo para tirar o máximo proveito dele. Lembrete, os módulos, após a inclusão, têm as configurações padrão do fabricante. Aproveite a vantagem de estar próximo ao controlador e interface Jeedom para configurar corretamente seu novo módulo. Também será mais fácil ativar o módulo para ver o efeito imediato da alteração. Alguns módulos possuem documentação específica do Jeedom para ajudá-lo com os diferentes parâmetros, bem como os valores recomendados.

Teste seu módulo, confirme o feedback, feedback de status e possíveis ações no caso de um atuador.

Durante a entrevista, seu novo módulo procurou seus vizinhos. No entanto, os módulos em sua rede ainda não conhecem seu novo módulo.

Mova seu módulo para seu local final. Inicie a atualização de seus vizinhos e acorde novamente.

![troubleshooting07](../images/troubleshooting07.png)

Vemos que ele vê um certo número de vizinhos, mas que os vizinhos não o vêem.

Para remediar essa situação, é necessário iniciar a ação de cuidar da rede, a fim de solicitar a todos os módulos que encontrem seus vizinhos.

Essa ação pode levar 24 horas antes de ser concluída. Seus módulos de bateria executam a ação somente na próxima vez que acordarem.

![troubleshooting08](../images/troubleshooting08.png)

A opção de cuidar da rede duas vezes por semana permite que você faça esse processo sem nenhuma ação de sua parte; é útil na instalação de novos módulos e / ou na movimentação deles.

## Sem feedback da condição da bateria

Os módulos Z-Wave raramente enviam o status da bateria ao controlador. Alguns o farão na inclusão somente quando atingir 20% ou outro valor limite crítico.

Para ajudá-lo a monitorar melhor o status de suas baterias, a tela Baterias no menu Análise fornece uma visão geral do status de suas baterias. Um mecanismo de notificação de bateria fraca também está disponível.

O valor retornado da tela Baterias é o último conhecido no cache.

Todas as noites, o plug-in Z-Wave solicita que cada módulo atualize o valor da bateria. Na próxima vez que você acordar, o módulo envia o valor para o Jeedom para ser adicionado ao cache. Portanto, você geralmente precisa esperar pelo menos 24 horas antes de obter um valor na tela Baterias.

> **Dica**
>
> É claro que é possível atualizar manualmente o valor da bateria através da guia Valores do módulo, aguardar a próxima ativação ou ativar manualmente o módulo para obter um aumento imediato. O intervalo de ativação do módulo é definido na guia Sistema do módulo. Para otimizar a vida útil das suas baterias, é recomendável espaçar esse atraso o maior tempo possível. Por 4h, aplique 14400, 12h 43200. Certos módulos devem ouvir regularmente as mensagens do controlador, como termostatos. Nesse caso, você deve pensar em 15 minutos, ou seja, 900. Cada módulo é diferente, portanto não existe uma regra exata, é caso a caso e de acordo com a experiência.

> **Dica**
>
> A descarga de uma bateria não é linear, alguns módulos mostram uma grande porcentagem de perda nos primeiros dias de comissionamento e, em seguida, não se movem por semanas para esvaziar rapidamente uma vez acima dos 20%.

## O controlador está sendo inicializado

Ao iniciar o daemon Z-Wave, se você tentar iniciar imediatamente uma inclusão / exclusão, poderá receber esta mensagem: \* "O controlador está inicializando, tente novamente em alguns minutos"

> **Dica**
>
> Após o início do daemon, o controlador continua todos os módulos para repetir a entrevista. Esse comportamento é completamente normal no OpenZWave.

Se, no entanto, após alguns minutos (mais de 10 minutos), você ainda tiver esta mensagem, ela não será mais normal.

Você precisa tentar as diferentes etapas:

-   Verifique se as luzes da tela de integridade do Jeedom estão verdes.
-   Verifique se a configuração do plug-in está em ordem.
-   Verifique se você selecionou a porta correta para a chave ZWave.
-   Verifique se a configuração da sua rede Jeedom está correta. (Atenção, se você fez uma restauração de uma instalação de bricolage em relação à imagem oficial, o sufixo / jeedom não deve aparecer lá)
-   Veja o log do plug-in para ver se um erro não foi relatado.
-   Assista ao **Console** Plugin ZWave, para verificar se um erro não foi relatado.
-   Lançar o demônio por **Depurar** olhe novamente para o **Console** e logs de plug-in.
-   Reinicie completamente o Jeedom.
-   Verifique se você possui um controlador Z-Wave, o Razberry geralmente é confundido com o EnOcean (erro ao fazer o pedido).

Agora devemos iniciar os testes de hardware:

-   O Razberry está bem conectado à porta GPIO.
-   Energia USB é suficiente.

Se o problema persistir, reinicie o controlador:

-   Pare completamente o seu Jeedom através do menu Parar no perfil do usuário.
-   Desconecte a energia.
-   Remova o dongle USB ou o Razberry, conforme apropriado, cerca de 5 minutos.
-   Reconecte tudo e tente novamente.

## O controlador não responde mais

Não são mais transmitidos pedidos aos módulos, mas os retornos de status são enviados de volta ao Jeedom.

A fila de mensagens do controlador pode estar cheia. Veja a tela Z-Wave Network se o número de mensagens pendentes aumentar apenas.

Nesse caso, você deve reiniciar o Demon Z-Wave.

Se o problema persistir, você deve redefinir o controlador:

-   Pare completamente o seu Jeedom através do menu Parar no perfil do usuário.
-   Desconecte a energia.
-   Remova o dongle USB ou o Razberry, conforme apropriado, cerca de 5 minutos.
-   Reconecte tudo e tente novamente.

## Erro durante dependências

Vários erros podem ocorrer ao atualizar dependências. Verifique o log de atualização de dependência para determinar qual é exatamente o erro. Geralmente, o erro está no final do log nas últimas linhas.

Aqui estão os possíveis problemas e suas possíveis soluções:

-   não foi possível instalar o mercurial - abortar

O pacote mercurial não deseja instalar, para corrigir o lançamento no ssh:

````
    sudo rm /var/lib/dpkg/info/$mercurial* -f
    sudo apt-ge install mercurial
````

-   Vícios parecem bloqueados em 75%

Em 75%, este é o início da compilação da biblioteca openzwave, bem como do wrapper python openzwave. Esta etapa é muito longa, no entanto, é possível visualizar o progresso através da visualização do log de atualização. Então você só precisa ser paciente.

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

Este erro pode ocorrer devido à falta de memória RAM durante a compilação.

Na interface do usuário jeedom, inicie a compilação de dependências.

Uma vez iniciado, no ssh, interrompa esses processos (consumidores na memória) :

````
    sudo systemctl stop cron
    sudo systemctl stop apache2
    sudo systemctl stop mysql.
````

Para acompanhar o andamento da compilação, adaptamos o arquivo de log openzwave\_update.

````
    tail -f /var/www/html/log/openzwave_update
````

Quando a compilação estiver concluída e sem erros, reinicie os serviços que você parou

````
sudo systemctl start cron sudo systemctl start apache2 sudo systemctl
start mysql
````

## Usando o cartão Razberry em um Raspberry Pi 3

Para usar um controlador Razberry em um Raspberry Pi 3, o controlador Bluetooth interno do Raspberry deve estar desativado.

Adicione esta linha:

````
    dtoverlay=pi3-miniuart-bt
````

No final do arquivo:

````
    /boot/config.txt
````

Em seguida, reinicie o seu Raspberry.

# API HTTP

O plug-in Z-Wave fornece aos desenvolvedores e usuários uma API completa para poder operar a rede Z-Wave via solicitação HTTP.

Você pode usar todos os métodos expostos pelo servidor REST do daemon Z-Wave.

A sintaxe para chamar rotas está neste formato:

URL  = ``http://token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/\#ROUTE\#``

-   \#API\_KEY\# corresponde à sua chave API, específica para sua instalação. Pour la trouver, il faut aller dans le menu « Geral », puis « Administration » e « Configuração », en activant le mode Expert, vous verrez alors une ligne Clef API.
-   \#IP\_JEEDOM\# corresponde ao seu URL de acesso Jeedom.
-   \#PORTDEMON\# corresponde ao número da porta especificado na página de configuração do plugin Z-Wave, por padrão: 8083.
-   \#ROUTE\# corresponde à rota no servidor REST para executar.

Para conhecer todas as rotas, consulte
[github](https://github.com/jeedom/plugin-openzwave) do plugin Z-Wave.

Example: Para executar ping no ID do nó 2

URL  = ``http://token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ZWaveAPI/Run/devices\[2\].TestNode()``

# FAQ

> **Recebo o erro "Não há espaço suficiente no buffer do fluxo"**
>
> Infelizmente esse erro é de hardware, não há nada que possamos fazer e estamos procurando, no momento, como forçar a reinicialização do daemon no caso desse erro (mas muitas vezes também é necessário desconectar a chave por 5 minutos para que ela reinicie)
