Description
===========

This plugin allows the exploitation of Z-Wave modules through
the OpenZwave library.

Introduction
============

Z-Wave communicates using low power radio technology in the 868.42 MHz frequency band. It is specifically designed for home automation applications. The Z-Wave radio protocol is optimized for low bandwidth exchanges (between 9 and 40 kbit / s) between devices on battery or powered by mains.

Z-Wave operates in the sub-gigahertz frequency range, depending on
regions (868 MHz in Europe, 908 MHz in the US, and other frequencies
according to the ISM bands of the regions). The theoretical range is approximately
30 meters indoors and 100 meters outdoors. The Z-Wave network
uses mesh technology to increase the range and
reliability. Z-Wave is designed to be easily integrated into
low-consumption electronic products, including
batteries such as remote controls, smoke detectors and
Security.

The Z-Wave +, brings certain improvements including a better range and
improves battery life, among other things. The
full backward compatibility with the Z-Wave.

Distances to be Respected with Other Wireless Signal Sources
-----------------------------------------------------------------

Radio receivers must be positioned at a minimum distance of
50 cm from other radio sources.

Examples of radio sources:

-   Ordinateurs

-   Microwave appliances

-   Electronic transformers

-   audio and video equipment

-   Pre-coupling devices for fluorescent lamps

> **Tip**
>
> If you have a USB controller (Z-Stick), it is recommended to
> move it away from the box using a simple 1M USB extension cable per
> Example.

The distance between other wireless transmitters such as phones
Wireless or radio audio transmissions must be at least 3 meters. The
following radio sources should be considered :

-   Interference by switch of electric motors
-   Interference from defective electrical devices
-   Interference from HF welding equipment
-   medical treatment devices

Effective wall thickness
---------------------------

The module locations must be chosen in such a way that
the direct connection line only works on a very short
distance through the material (a wall), in order to avoid as much as possible
mitigations.

![introduction01](../images/introduction01.png)

Metal parts of the building or furniture can block
electromagnetic waves.

Meshing and Routing
-------------------

Mains Z-Wave nodes can transmit and repeat messages
which are not within direct range of the controller. This allows a more
great flexibility of communication, even if there is no connection
direct wireless or if a connection is temporarily unavailable, to
because of a change in the room or building.

![introduction02](../images/introduction02.png)

The controller **Id 1** can communicate directly with nodes 2, 3
and 4. Node 6 is outside of its radio range, however, it is
found in the radio coverage area of node 2. Therefore, the
controller can communicate with node 6 via node 2. Of this
way, the path from the controller through node 2 to node 6, is called
road. In the case where the direct communication between node 1 and the
node 2 is blocked, there is yet another option to communicate with
node 6, using node 3 as another signal repeater.

It becomes obvious that the more sector nodes you have, the more the
routing options increase, and more network stability increases.
The Z-Wave protocol is capable of routing messages by
through a maximum of four repeat nodes. It's a
trade-off between network size, stability and maximum duration
of a message.

> **Tip**
>
> It is strongly recommended at the start of installation to have a ratio
> between sector nodes and node on 2/3 batteries, in order to have a good
> network mesh. Favor micromodules over smart plugs. The
> micro modules will be in a final location and will not be
> disconnected, they also generally have a better range. A voucher
> departure is the lighting of the common areas. It will help well
> distribute the sector modules at strategic locations in your
> home. Then you can add as many modules on the stack
> as desired, if your basic routes are good.

> **Tip**
>
> The **Network graph** as well as **Routing table**
> allow you to view the quality of your network.

> **Tip**
>
> There are repeater modules to fill areas where no module
> sector has no use.

Properties of Z-Wave devices
-------------------------------

|  | Neighbors | Road | Possible functions |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controller | Knows all the neighbors | Has access to the complete routing table | Can communicate with all devices in the network, if a channel exists |
| Slave | Knows all the neighbors | Has no information on the routing table | Cannot reply to the node it received the message. Therefore, cannot send unsolicited messages |
| Routing slaves | Knows all its neighbors | With partial knowledge of the routing table | Can reply to the node it received the message from and can send unsolicited messages to a number of nodes |

In summary:

-   Each Z-Wave device can receive and acknowledge receipt of
    messages

-   Controllers can send messages to all nodes in the
    réseau, sollicités or non « The maître peut parler quand il veut and à
    who he wants »

-   Slaves cannot send unsolicited messages,
    mais seulement une réponse aux demanof «L'esclave ne parle que si
    we ask him »

-   Routing slaves can respond to requests and they are
    allowed to send unsolicited messages to certain nodes that
    le Controller a prédéfini « L'esclave East toujours un esclave, mais
    on authorization, he can speak »

Plugin configuration
=======================

After downloading the plugin, you just need to activate it and
configurer.

![Setup01](../images/configuration01.png)

Once activated, the demon should launch. The plugin is preconfigured
with default values; you normally have nothing more to do.
However you can change the configuration.

Dependencies
-----------

This part allows you to validate and install the required dependencies
the proper functioning of the Zwave plugin (both locally and
deported, here locally) ![configuration02](../images/configuration02.png)

-   A status **OK** confirms dependencies are met.

-   If the status is **NOK**, dependencies will have to be reinstalled
    using the button ![configuration03](../images/configuration03.png)

> **Tip**
>
> Updating dependencies can take more than 20 minutes depending on
> your material. Progress is displayed in real time and a log
> **Openzwave\_update** is accessible.

> **Important**
>
> Updating dependencies is normally to be done only
> If the status is **NOK**, but it is however possible, to adjust
> certain problems, to be called upon to redo the installation of
> Dependencies.

> **Tip**
>
> If you are in remote mode, the dependencies of the local daemon can
> to be NOK, it's completely normal.

Daemon
-----

This part allows you to validate the current state of the demon (s) and
configure automatic management of these.
![Setup04](../images/configuration04.png) The démon local et
all the deported demons will be displayed with their different
informations

-   The **Statut** indicates that the demon is currently running.

-   The **Configuration** indicates if the configuration of the daemon
    is validated.

-   The button **(To restart** allows to force the restart of the
    plugin, in normal mode or launch it the first time.

-   The button **Stopped**, visible only if automatic management
    is disabled, forces the demon to stop.

-   The **Automatic management** allows Jeedom to launch automatically
    the demon when Jeedom starts, as well as to restart it in case
    of problem.

-   The **Last launch** is as the name suggests the date of
    last known launch of the demon.

Log
---

This part allows you to choose the level of log as well as to consult it.
the contents.

![Setup05](../images/configuration05.png)

Select the level then save, the daemon will then be restarted
with selected instructions and traces.

Level **Debug** or **Info** may be helpful in understanding
why the demon plants or does not raise a value.

> **Important**
>
> In mode **Debug** the demon is very verbose, it is recommended
> use this mode only if you need to diagnose a problem
> particular. It is not recommended to let the demon run while
> **Debug** permanently, if we use a **SD-Card**. Once the
> debug over, don't forget to return to a lower level
> high as the level **Error** which only goes back to possible
> errors.

Configuration
-------------

This part allows you to configure the general parameters of the plugin
![Setup06](../images/configuration06.png)

-   **Main** :

    -   **Automatically delete excluded devices** :
        The Yes option allows you to delete the devices excluded from the
        Z-Wave network. The No option allows you to keep the equipment
        in Jeedom even if they have been excluded from the network. The equipment
        will have to be manually deleted or reused in it
        assigning a new Z-Wave ID if you are migrating the
        lead controller.

    -   **Apply the recommended configuration set for inclusion** :
        option to apply the set of
        configuration recommended by the Jeedom team (recommended)

    -   **Deactivate the background update of the drives** :
        Do not request a refresh of the drives
        background.

    -   **Cycle (s)** : allows to define the frequency of the lifts
        at Jeedom.

    -   **Z-Wave key port** : the USB port on which your interface
        Z-Wave is connected. If you use the Razberry, you have,
        depending on your architecture (RPI or Jeedomboard) the 2
        possibilities at the end of the list.

    -   **Server Port** (dangerous modification, must have the same
        value on all Z-Wave remote Jeedoms) : allows
        modify the internal communication port of the daemon.

    -   **Backups** : allows you to manage backups of the file
        network topology (see below)

    -   **Config modules** : allows to retrieve, manually,
        OpenZWave configuration files with parameters for
        modules as well as defining module commands for
        their uses.

        > **Tip**
        >
        > Module configurations are retrieved
        > automatically every night.

        > **Tip**
        >
        > Restarting the daemon after updating the
        > module configurations is unnecessary.

        > **Important**
        >
        > If you have an unrecognized module and an update of
        > configuration has just been applied, you can manually
        > start retrieving module configurations.

Once the configurations retrieved, it will take according to the changes
brought:

-   For a new module without configuration or control : exclude and
    re-include the module.

-   For a module for which only the parameters have been updated :
    start the regeneration of the node detection, via the Actions tab
    of the module (the plugin must restart).

-   Pour un Module dont le « mapping » controls a été corrigé : la
    magnifying glass on the controls, see below.

    > **Tip**
    >
    > If in doubt, exclude and re-include the module is recommended.

Do not forget to ![configuration08](../images/configuration08.png) si
you make a change.

> **Important**
>
> If you are using Ubuntu : For the demon to work, you must
> absolutely have ubuntu 15.04 (lower versions have a bug and
> the demon cannot start). Be careful if you place a bet
> up to date from 14.04 it takes once in 15.04 relaunch
> installation of outbuildings.

> **Important**
>
> Selecting the Z-Wave Key Port in automatic detection mode,
> **Auto**, only works for USB dongles.

Mobile Panel
-------------

![Setup09](../images/configuration09.png)

Allows to display or not the mobile panel when you use
the application on a phone.

Equipment configuration
=============================

The configuration of Z-Wave equipment is accessible from the menu
Plugin :

![appliance01](../images/appliance01.png)

Below is an example of a Z-Wave plugin page (presented with
some equipment) :

![appliance02](../images/appliance02.png)

> **Tip**
>
> As in many places on Jeedom, place the mouse on the far left
> brings up a quick access menu (you can, at
> from your profile, always leave it visible).

> **Tip**
>
> The buttons on the top line **Synchroniser**,
> **Zwave Network** and **Santé**, are visible only if you are in
> fashion **Expert**. ![appliance03](../images/appliance03.png)

Main
-------

Here you find all the configuration of your equipment :

![appliance04](../images/appliance04.png)

-   **Name of equipment** : name of your Z-Wave module.

-   **Parent object** : indicates the parent object to which
    belongs equipment.

-   **Category** : equipment categories (it may belong to
    multiple categories).

-   **Activer** : makes your equipment active.

-   **Visible** : makes it visible on the dashboard.

-   **Node ID** : Module ID on the Z-Wave network. This can be
    useful if, for example, you want to replace a faulty module.
    Just include the new module, get its ID, and the
    put in place of the old module ID and finally delete
    the new module.

-   **Module** : this field only appears if there are different types of
    configuration for your module (case for modules that can do
    pilot wires for example). It allows you to choose the
    configuration to use or modify it later

-   **Marque** : manufacturer of your Z-Wave module.

-   **Configuration** : window for configuring the parameters of the
    module

-   **Assistant** : only available on certain modules, you
    helps to configure the module (case on the zipato keyboard for example)

-   **Documentation** : this button allows you to directly open the
    Jeedom documentation concerning this module.

-   **Supprimer** : Allows you to delete an item of equipment and all of these
    attached commands without excluding it from the Z-Wave network.

> **Important**
>
> Deleting an equipment does not result in exclusion from the module
> on the controller. ![appliance11](../images/appliance11.png) Un
> deleted equipment which is still attached to its controller will
> automatically recreated following synchronization.

Commandes
---------

Below you find the list of orders :

![appliance05](../images/appliance05.png)

> **Tip**
>
> Depending on the types and subtypes, some options may be
> absent.

-   the name displayed on the dashboard
-   Icon : in the case of an action allows you to choose an icon to
    display on dashboard instead of text
-   Order value : in the case of an action type command, its
    value can be linked to an info type command, this is where
    it is configured. Example for a lamp the intensity is linked to its
    state, this allows the widget to have the actual state of the lamp.
-   type and subtype.
-   the instance of this Z-Wave command (reserved for experts).
-   the class of the Z-Wave control (reserved for experts).
-   the value index (reserved for experts).
-   the order itself (reserved for experts).
-   "Status feedback value "and" Duration before status feedback" : permet
    to indicate to Jeedom that after a change in the information
    value must return to Y, X min after the change. Example : dans
    the case of a presence detector which emits only during a
    presence detection, it is useful to set for example 0
    value and 4 in duration, so that 4 min after a detection of
    movement (and if there were no new ones) Jeedom
    resets the value of the information to 0 (no more movement detected).

-   Historize : allows to historize the data.
-   Pin up : allows to display the data on the dashboard.
-   Invert : allows to invert the state for binary types.
-   Unit : data unit (can be empty).
-   Min / max : data bounds (may be empty).
-   Advanced configuration (small notched wheels) : displays the advanced configuration of the command (logging method, widget, etc.).

-   Test : Used to test the command.
-   Delete (sign -) : allows to delete the command.

> **Important**
>
> The button **Tester** in the case of an Info type command, will not
> not query the module directly but the value available in the
> jeedom cache. The test will return the correct value only if the
> module in question has transmitted a new value corresponding to the
> definition of the command. It is then completely normal not to
> get results following the creation of a new Info command,
> specially on a battery module that rarely notifies Jeedom.

The **loupe**, available in the general tab, allows you to recreate
all the commands for the current module.
![appliance13](../images/appliance13.png) Si aucune Command n'est
present or if the commands are incorrect the magnifying glass should remedy
the situation.

> **Important**
>
> The **loupe** will delete existing orders. If the orders
> were used in scenarios, you will need to correct your
> scenarios in other places where the controls were operated.

Command Games
-----------------

Some modules have several preconfigured command sets

![appliance06](../images/appliance06.png)

You can select them via the possible choices, if the module
permet.

> **Important**
>
> You must carry out the magnifying glass to apply the new sets of
> Commands.

Documentation and Assistant
--------------------------

For a certain number of modules, specific help for setting up
place as well as parameter recommendations are available.

![appliance07](../images/appliance07.png)

The button **Documentation** provides access to documentation
module specific for Jeedom.

Special modules also have a specific assistant to
to facilitate the application of certain parameters or operations.

The button **Assistant** allows access to the specific assistant screen
of the module.

Recommended configuration
-------------------------

![appliance08](../images/appliance08.png)

Allows you to apply a configuration set recommended by the team
Jeedom.

> **Tip**
>
> When included, modules have the default settings of
> manufacturer and some functions are not activated by default.

The following, as applicable, will be applied to simplify
using the module.

-   **Settings** allowing rapid commissioning of the assembly
    module functionality.

-   **Association groups** required for proper operation.

-   **Wake up interval**, for modules on battery.

-   Activation of **manual refresh** for modules do
    not going back by themselves their changes of states.

To apply the recommended configuration set, click on the button
: **Recommended configuration**, then confirm the application of
recommended configurations.

![appliance09](../images/appliance09.png)

The assistant activates the various configuration elements.

A confirmation of the good progress will be displayed in the form of a banner

![appliance10](../images/appliance10.png)

> **Important**
>
> The battery modules must be awakened to apply the set of
> Setup.

The equipment page informs you if items have not yet been
been activated on the module. Please refer to the documentation of the
module to wake it up manually or wait for the next cycle of
awakening.

![appliance11](../images/appliance11.png)

> **Tip**
>
> It is possible to automatically activate the game application.
> recommended configuration when including a new module, see
> the Plugin configuration section for more details.

Configuration of modules
=========================

This is where you will find all the information about your module

![node01](../images/node01.png)

The window has several tabs :

Summary
------

Provides a full summary of your node with various information
on this one, like for example the state of the requests which makes it possible to know
if the node is waiting for information or the list of neighboring nodes.

> **Tip**
>
> On this tab it is possible to have alerts in case of detection
> possible from a configuration problem, Jeedom will indicate the march
> to follow to correct. Do not confuse an alert with a
> error, the alert is in most cases a simple
> recommendation.

Valeurs
-------

![node02](../images/node02.png)

Here you will find all the possible commands and states on your
module. They are ordered by instance and command class then index.
The « mapping » of Commands East entièrement basé sur ces Information.

> **Tip**
>
> Force update of a value. The battery modules will
> refresh a value only at the next wake-up cycle. It is
> however, it is possible to manually wake up a module, see the
> Module documentation.

> **Tip**
>
> It is possible to have more orders here than on Jeedom, it is
> complitly normal. In Jeedom the orders have been preselected
> for you.

> **Important**
>
> Some modules do not automatically send their states, it is necessary
> in this case activate the manual refresh at 5 minutes on the or
> desired values. It is recommended to automatically leave the
> Refreshing. Abuse of manual refreshment can impact
> strongly the performance of the Z-Wave network, use only for
> the values recommended in the specific Jeedom documentation.
> ![node16](../images/node16.png) The set of values (index) of
> the instance of a class command will be reassembled, activating the
> manual refresh on the smallest index of the instance of the
> class command. Repeat for each instance if necessary.

Settings
----------

![node03](../images/node03.png)

Here you will find all the configuration possibilities for
parameters of your module as well as the ability to copy the
configuration of another node already in place.

When a parameter is modified, the corresponding line turns yellow,
![node04](../images/node04.png) le paramètre East en attente d'être
appliqué.

If the module accepts the parameter, the line becomes transparent again.

If however the module refuses the value, the line will then turn red
with the applied value returned by the module.
![node05](../images/node05.png)

On inclusion, a new module is detected with the parameters by
manufacturer's defect. On some modules, functionality does not
will not be active without modifying one or more parameters.
Refer to the manufacturer's documentation and our recommendations
in order to properly configure your new modules.

> **Tip**
>
> The modules on stack will apply the parameter changes
> only on the next wake-up cycle. It is however possible to
> manually wake up a module, see module documentation.

> **Tip**
>
> The command **Resume from ...** allows you to resume configuration
> from another identical module, on the current module.

![node06](../images/node06.png)

> **Tip**
>
> The command **Apply on ...** allows you to apply the
> current configuration of the module on one or more modules
> identical.

![node18](../images/node18.png)

> **Tip**
>
> The command **Update settings** force the module to update
> the parameters saved in the module.

If no configuration file is defined for the module, a
manual assistant allows you to apply parameters to the module.
![node17](../images/node17.png) Veillez vous référer à the documentation
of the manufacturer to know the definition of the index, value and size.

Associations
------------

This is where you find the management of the association groups of your
module.

![node07](../images/node07.png)

Z-Wave modules can control other Z-Wave modules, without
go through neither Jeedom controller. The relationship between a module of
control and another module is called association.

In order to control another module, the control module needs to
maintain a list of devices that will receive control of
orders. These lists are called association groups and are
always linked to certain events (for example the button pressed, the
sensor triggers, etc.).

In the event that an event occurs, all devices
registered in the relevant association group will receive an order
Basic.

> **Tip**
>
> See the module documentation, to understand the different
> possible association groups and their behavior.

> **Tip**
>
> The majority of modules have an association group which is reserved
> for the main controller, it is used to reassemble the
> information to the controller. It is generally called : **Report** ou
> **LifeLine**.

> **Tip**
>
> Your module may not have any groups.

> **Tip**
>
> The modification of association groups of a module on stack will be
> applied to the next wake-up cycle. It is however possible to
> manually wake up a module, see module documentation.

To find out with which other modules the current module is associated,
just click on the menu **Associated with which modules**

![node08](../images/node08.png)

All the modules using the current module as well as the names of the
association groups will be displayed.

**Multi-instance associations**

some module supports a multi-instance associations class command.
When a module supports this CC, it is possible to specify with
which body we want to create the association

![node09](../images/node09.png)

> **Important**
>
> Certain modules must be associated with instance 0 of the controller
> main in order to work well. For this reason, the controller
> is present with and without instance 0.

Systems
--------

Tab grouping the module's system parameters.

![node10](../images/node10.png)

> **Tip**
>
> The battery modules wake up at regular cycles, called
> Wakeup Interval. The wake-up interval is a
> trade-off between maximum battery life and responses
> desired from the device. To maximize the life of your
> modules, adapt the Wakeup Interval value for example to 14400
> seconds (4h), see even higher depending on the modules and their use.
> ![node11](../images/node11.png)

> **Tip**
>
> Modules **Interrupteur** and **Variateur** can implement a
> Special order class called **SwitchAll** 0x27. You can
> change behavior here. Depending on the module, several options are
> available. The command **SwitchAll On / OFF** can be launched via
> your main controller module.

Actions
-------

Allows you to perform certain actions on the module.

![node12](../images/node12.png)

Certain actions will be active depending on the type of module and its
possibilities or according to the current state of the module such as for example
if presumed dead by the controller.

> **Important**
>
> Do not use actions on a module if you do not know what
> that we do. Some actions are irreversible. The actions
> can help solve problems with one or more modules
> Z-WAVE.

> **Tip**
>
> The **Regeneration of node detection** can detect the
> module to retrieve the last set of parameters. This action
> is required when you are informed that a parameter update and
> or module behavior is required for proper operation. The
> Regeneration of the node detection implies a restart of the
> network, the assistant performs it automatically.

> **Tip**
>
> If you have several identical modules of which it is required
> to execute the **Regeneration of node detection**, It is
> possible to launch it once for all identical modules.

![node13](../images/node13.png)

> **Tip**
>
> If a battery module is no longer reachable and you wish to
> exclude it, that the exclusion does not take place, you can launch
> **Remove ghost node** An assistant will perform different
> actions to remove the so-called ghost module. This action involves
> restart the network and may take several minutes to be
> completed.

![node14](../images/node14.png)

Once launched, it is recommended to close the configuration screen of the
module and monitor the removal of the module via the health screen
Z-Wave.

> **Important**
>
> Only modules on battery can be deleted via this wizard.

Statistiques
------------

This tab gives some communication statistics with the node.

![node15](../images/node15.png)

May be of interest in the case of modules which are presumed dead by the
controller "Dead".

inclusion / exclusion
=====================

When it leaves the factory, a module does not belong to any Z-Wave network.

Inclusion mode
--------------

The module must join an existing Z-Wave network to communicate
with the other modules of this network. This process is called
**Inclusion**. Devices can also leave a network.
This process is called **Exclusion**. Both processes are initiated
by the main controller of the Z-Wave network.

![addremove01](../images/addremove01.png)

This button allows you to switch to inclusion mode to add a module
to your Z-Wave network.

You can choose the inclusion mode after clicking the button
**Inclusion**.

![addremove02](../images/addremove02.png)

Since the appearance of the Z-Wave +, it is possible to secure the
exchanges between the controller and the nodes. It is therefore recommended to
do inclusions in mode **Secured**.

If, however, a module cannot be included in secure mode, please
include it in mode **Insecure**.

Once in inclusion mode : Jeedom tells you.

\ [TIP \] A module 'not secure' can order modules' not
secure '. An 'unsecured' module cannot order a module
'secured'. A 'secure' module can order modules' not
secure 'provided that the transmitter supports it.

![addremove03](../images/addremove03.png)

Once the wizard is launched, you must do the same on your module
(refer to its documentation to switch it to mode
inclusion).

> **Tip**
>
> Until you have the headband, you are not in mode
> Inclusion.

If you click on the button again, you exit the inclusion mode.

> **Tip**
>
> It is recommended, before the inclusion of a new module which would be
> "new "on the market, to launch the order **Config modules** via
> plugin configuration screen. This action will recover
> all the latest versions of the configuration files
> openzwave and the Jeedom command mapping.

> **Important**
>
> During an inclusion, it is advised that the module is near
> from the main controller, less than a meter from your jeedom.

> **Tip**
>
> Some modules require an inclusion in mode
> **Secured**, for example for door locks.

> **Tip**
>
> Note that the mobile interface also gives you access to inclusion,
> the mobile panel must have been activated.

> **Tip**
>
> If the module already belongs to a network, follow the process
> exclusion before including it in your network. Otherwise the inclusion of
> this module will fail. It is also recommended to perform a
> exclusion before inclusion, even if the product is new, out of
> cardboard.

> **Tip**
>
> Once the module in its final location, you must launch
> the action take care of the network, in order to ask all the modules
> refresh all the neighbors.

Exclusion mode
--------------

![addremove04](../images/addremove04.png)

This button allows you to enter exclusion mode, this to remove a
module of your Z-Wave network, you must do the same with your
module (refer to its documentation to switch it to mode
exclusion).

![addremove05](../images/addremove05.png)

> **Tip**
>
> Until you have the headband, you are not in mode
> Exclusion.

If you click on the button again, you will exit exclusion mode.

> **Tip**
>
> Note that the mobile interface also gives you access to the exclusion.

> **Tip**
>
> A module does not need to be excluded by the same controller on
> which it was previously included. Hence the fact that we recommend
> execute an exclusion before each inclusion.

Synchroniser
------------

![addremove06](../images/addremove06.png)

Button to synchronize the modules of the Z-Wave network with the
Jeedom equipment. The modules are associated with the main controller,
the equipment in Jeedom is created automatically when it is
inclusion. They are also automatically deleted when excluded.,
if the option **Automatically delete excluded devices** est
activated.

If you have included modules without Jeedom (requires a dongle with
battery like the Aeon-labs Z-Stick GEN5), synchronization will be
necessary after plugging in the key, once the daemon has started and
fonctionnel.

> **Tip**
>
> If you don't have the image or Jeedom has not recognized your module,
> this button can be used to correct (provided that the interview with the
> module is complete).

> **Tip**
>
> If on your routing table and / or on the Z-Wave health screen, you
> have one or more modules named with their **generic name**, la
> synchronization will remedy this situation.

The Synchronize button is only visible in expert mode :
![addremove07](../images/addremove07.png)

Z-Wave networks
==============

![network01](../images/network01.png)

Here you will find general information about your Z-Wave network.

![network02](../images/network02.png)

Summary
------

The first tab gives you the basic summary of your Z-Wave network,
you will find in particular the state of the Z-Wave network as well as the number
items in the queue.

**Informations**

-   Gives general information about the network, the date of
    startup, the time required to obtain the network in a state
    says functional.

-   The total number of nodes in the network as well as the number that sleep
    in the moment.

-   The request interval is associated with manual refresh. he
    is preset in the Z-Wave engine at 5 minutes.

-   The neighbors of the controller.

**Etat**

![network03](../images/network03.png)

A set of information on the current state of the network, namely :

-   Current state, maybe **Driver Initialized**, **Topology loaded**
    or **Ready**.

-   Outgoing tail, indicates the number of messages queued in the
    controller waiting to be sent. This value is generally
    high during network startup when the status is still in
    **Driver Initialized**.

Once the network has at least reached **Topology loaded**, des
mechanisms internal to the Z-Wave server will force updates to
values, then it is completely normal to see the number of
messages. This will quickly return to 0.

> **Tip**
>
> The network is said to be functional when it reaches the status
> **Topology loaded**, that is to say that the set of sector nodes
> have completed their interviews. Depending on the number of modules, the
> battery / sector distribution, the choice of the USB dongle and the PC on which
> turns the Z-Wave plugin, the network will reach this state between a
> and five minutes.

A network **Ready**, means that all sector and stack nodes have
completed their interview.

> **Tip**
>
> Depending on the modules you have, it is possible that the network
> never reaches status by itself **Ready**. The remote controls,
> for example, do not wake up on their own and will not complement
> never their interview. In this kind of case, the network is completely
> operational and even if the remote controls have not completed their
> interview, they ensure their functionality within the network.

**Capacities**

Used to find out whether the controller is a main controller or
secondaire.

**System**

Displays various system information.

-   Information on the USB port used.

-   OpenZwave library version

-   Version of the Python-OpenZwave library

Actions
-------

![network05](../images/network05.png)

Here you will find all the possible actions for all of your
Z-Wave network. Each action is accompanied by a brief description.

> **Important**
>
> Some actions are really risky or even irreversible, the team
> Jeedom cannot be held responsible in case of bad
> handling.

> **Important**
>
> Some modules require inclusion in secure mode, by
> example for door locks. Secure inclusion must be
> launched via the action of this screen.

> **Tip**
>
> If an action cannot be launched, it will be deactivated until
> when it can be executed again.

Statistiques
------------

![network06](../images/network06.png)

Here you will find general statistics for all of your
Z-Wave network.

Network graph
-------------------

![network07](../images/network07.png)

This tab will give you a graphic representation of the different
links between nodes.

Explanation of the color legend :

-   **Noir** : The main controller, generally represented
    like Jeedom.

-   **Vert** : Direct communication with the controller, ideal.

-   **Blue** : For controllers, like remote controls, they are
    associated with the primary controller, but have no neighbor.

-   **Jaune** : All roads have more than one jump before arriving
    to the controller.

-   **Gris** : The interview is not yet completed, the links will be
    really known once the interview is completed.

-   **Rouge** : presumed dead, or without neighbor, does not participate / no longer in
    network mesh.

> **Tip**
>
> Only active equipment will be displayed in the network graph.

The Z-Wave network consists of three different types of nodes with
three main functions.

The main difference between the three types of nodes is their
knowledge of the network routing table and thereafter their
ability to send messages to the network:

Routing table
----------------

Each node is able to determine which other nodes are in
Direct communication. These nodes are called neighbors. During
inclusion and / or later on request, the node is able
to inform the controller of the list of neighbors. Thanks to these
information, the controller is able to build a table that has
all information on possible routes of communication in
A network.

![network08](../images/network08.png)

The rows of the table contain the source nodes and the columns
contain destination nodes. Refer to the legend for
understand the cell colors that indicate the links between two
knots.

Explanation of the color legend :

-   **Vert** : Direct communication with the controller, ideal.

-   **Blue** : At least 2 routes with a jump.

-   **Jaune** : Less than 2 routes with a jump.

-   **Gris** : The interview is not yet completed, will actually be
    updated after the interview is completed.

-   **Orange** : All roads have more than one jump. Can cause
    latencies.

> **Tip**
>
> Only active equipment will be displayed in the network graph.

> **Important**
>
> A module presumed dead, does not participate / no longer in the networking of the network.
> It will be marked here with a red exclamation point in a triangle.

> **Tip**
>
> You can manually start the neighbor update, by module
> or for the entire network using the buttons available in the
> Routing table.

Santé
=====

![health01](../images/health01.png)

This window summarizes the status of your Z-Wave network :

![health02](../images/health02.png)

You have here :

-   **Module** : the name of your module, a click on it allows you to
    access directly.

-   **ID** : ID of your module on the Z-Wave network.

-   **Notification** : last type of exchange between the module and the
    Controller

-   **Groupe** : indicates if the group configuration is ok
    (controller at least in a group). If you have nothing it is because
    the module does not support the notion of group, this is normal

-   **Constructeur** : indicates whether retrieving information
    module identification is ok

-   **Voisin** : indicates if the list of neighbors has been retrieved

-   **Statut** : Indicates the status of the interview (query stage) of the
    module

-   **Batterie** : battery level of the module (a mains plug
    indicates that the module is powered from the mains).

-   **Wakeup time** : for battery modules, it gives the
    frequency in seconds of the instants when the module
    wake up automatically.

-   **Total package** : displays the total number of packets received or
    successfully sent to the module.

-   **%OK** : displays the percentage of packets sent / received
    with success.

-   **Temporisation** : displays the average packet sending delay in ms.

-   **Last notification** : Date of last notification received from
    module and the next scheduled wake-up time for modules
    who sleep.

    -   It also allows to inform if the node is not yet
        woke up once since launching the demon.

    -   And indicates if a node has not woken up as expected.

-   **Ping** : Send a series of messages to the module to
    test its proper functioning.

> **Important**
>
> Disabled equipment will be displayed but no information from
> diagnosis will only be present.

The name of the module can be followed by one or two images:

![health04](../images/health04.png) Modules supportant la
COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../images/health05.png) Modules supportant la
COMMAND\_CLASS\_SECURITY and secure.

![health06](../images/health06.png) Modules supportant la
COMMAND\_CLASS\_SECURITY and not secure.

![health07](../images/health07.png) Module FLiRS, routeurs esclaves
(battery modules) with frequent listening.

> **Tip**
>
> The Ping command can be used if the module is presumed dead
> "DEATH "to confirm if this is really the case.

> **Tip**
>
> Sleeping modules will only respond to Ping when
> next wake up.

> **Tip**
>
> Timeout notification does not necessarily mean a problem
> with the module. Ping and in most cases the module
> will respond with a Notification **NoOperation** which confirms a return
> fruitful Ping.

> **Tip**
>
> Timeout and% OK on nodes on batteries before completion
> of their interview is not significant. Indeed the knot does not go
> answer the controller's questions about the fact that he is asleep
> deep.

> **Tip**
>
> The Z-Wave server automatically takes care of launching tests on the
> Timeout modules after 15 minutes

> **Tip**
>
> Z-Wave server automatically tries to remount modules
> presumed dead.

> **Tip**
>
> An alert will be sent to Jeedom if the module is presumed dead. You
> can activate a notification to be informed the most
> quickly possible. See the Messages configuration in the screen
> Jeedom Configuration.

![health03](../images/health03.png)

> **Tip**
>
> If on your routing table and / or on the Z-Wave health screen you
> have one or more modules named with their **generic name**, la
> synchronization will remedy this situation.

> **Tip**
>
> If on your routing table and / or on the Z-Wave health screen you
> have one or more modules named **Unknown**, it means that
> module interview was not successfully completed. You have
> probably a **NOK** in the constructor column. Open the detail
> of the module (s), to try out the suggested solutions.
> (see section Troubleshooting and diagnostics, below)

Interview status
---------------------

Step of interviewing a module after starting the daemon.

-   **None** Initialization of the node search process.

-   **ProtocolInfo** Retrieve protocol information, if this
    node is listening (listener), its maximum speed and its classes
    of peripherals.

-   **Probe** Ping the module to see if it is awake.

-   **WakeUp** Start the wake-up process, if it is a
    sleeping knot.

-   **ManufacturerSpecific1** Retrieve the name of the manufacturer and
    ids products if ProtocolInfo allows.

-   **NodeInfo** Retrieve information on class management
    supported commands.

-   **NodePlusInfo** Retrieve ZWave + info on support
    supported command classes.

-   **SecurityReport** Retrieve the list of order classes which
    require security.

-   **ManufacturerSpecific2** Retrieve the name of the manufacturer and the
    product identifiers.

-   **Versions** Retrieve version information.

-   **Instances** Retrieve multi-instance class information
    control.

-   **Static** Retrieve static information (does not change).

-   **CacheLoad** Ping the module during reboot with config cache
    of the device.

-   **Associations** Retrieve information on associations.

-   **Neighbors** Retrieve the list of neighboring nodes.

-   **Session** Retrieve session information (rarely changes).

-   **Dynamic** Retrieve dynamic information
    (changes frequently).

-   **Configuration** Retrieve parameter information from
    configurations (only made on request).

-   **Complete** The interview process is finished for this node.

Notification
------------

Details of notifications sent by modules

-   **Completed** Action successfully completed.

-   **Timeout** Delay report reported when sending a message.

-   **NoOperation** Report on a node test (Ping), that the message
    has been successfully sent.

-   **Awake** Report when a node has just woken up

-   **Sleep** Report when a node has fallen asleep.

-   **Dead** Report when a node is presumed dead.

-   **Alive** Report when a node is relaunched.

Backups
=======

The backup part will allow you to manage the backups of the topology
from your network. This is your zwcfgxxx file.xml, it is the
last known state of your network, it is a form of cache of your
network. From this screen you can :

-   Start a backup (a backup is made at each stop restarting the
    network and during critical operations). The last 12 backups
    are kept

-   Restore a backup (by selecting it from the list
    just above)

-   Delete a backup

![backup01](../images/backup01.png)

Update OpenZWave
=======================

Following an update of the Z-Wave plugin it is possible that Jeedom will
request to update Z-Wave dependencies. A NOK at the level of
dependencies will be displayed:

![update01](../images/update01.png)

> **Tip**
>
> An update of the dependencies is not to be done with each update
> plugin.

Jeedom should launch the dependency update on its own if the
plugin considers that they are **NOK**. This validation is carried out at
after 5 minutes.

The duration of this operation may vary depending on your system
(up to more than 1 hour on raspberry pi)

Once the dependencies update is complete, the daemon will restart
automatically upon validation of Jeedom. This validation is
done after 5 minutes.

> **Tip**
>
> In the event that updating dependencies does not occur
> not complete, please consult the log **Openzwave\_update** qui
> should inform you about the problem.

List of compatible modules
============================

You will find the list of compatible modules
[here](https://doc.jeedom.com/en_US/zwave/equipement.compatible)

Troubleshooting and diagnosis
=======================

My module is not detected or does not provide its product and type identifiers
-------------------------------------------------------------------------------

![troubleshooting01](../images/troubleshooting01.png)

Start the Regeneration of the node detection from the Actions tab
of the module.

If you have several modules in this scenario, launch **Regenerate
detection of unknown nodes** from the screen **Zwave network** onglet
**Actions**.

My module is presumed dead by the Dead controller
--------------------------------------------------

![troubleshooting02](../images/troubleshooting02.png)

If the module is still plugged in and reachable, follow the solutions
proposed in the module screen.

If the module has been canceled or is really defective, you
can exclude it from the network using **delete the node in error**
via tab **Actions**.

If the module has been repaired and a new module
replacement has been delivered you can launch **Replace failed node**
via tab **Actions**, the controller triggers the inclusion then you
must proceed with inclusion on the module. The id of the old module will be
kept as well as his orders.

How to use the SwitchAll command
--------------------------------------

![troubleshooting03](../images/troubleshooting03.png)

It is available via your controller node. Your controller should
have Switch All On and Switch All Off commands.

If your controller does not appear in your module list, launch the
synchronisation.

![troubleshooting04](../images/troubleshooting04.png)

The Switch All Class Command is generally supported on
switches and dimmers. Its behavior is configurable on
each module that supports it.

So we can either:

-   Deactivate the Switch All Class Command.

-   Activate for On and Off.

-   Activate On only.

-   Activate Off only.

The choice of options depends on the manufacturer.

So you have to take the time to review all of its
switches / dimmers before setting up a scenario if you don't
not only pilot lights.

My module does not have a Scene or Button command
----------------------------------------------

![troubleshooting05](../images/troubleshooting05.png)

You can add the command in the command mapping screen.

This is an order **Info** in CC **0x2b** Instance **0** commande
**data \ [0 \]. val**

Scene mode must be activated in module settings. See it
documentation of your module for more details.

Force refresh values
-------------------------------------

It is possible to force on request the refreshment of the values
an instance for a specific class command.

It is possible to do via an http request or create an order
in the equipment mapping screen.

![troubleshooting06](../images/troubleshooting06.png)

This is an order **Action** choose the **CC** desired for a
**Instance** given with the command **data \ [0 \]. ForceRefresh ()**

All the instance indexes for this Class command will be put
up to date. The knots on batteries will wait for their next awakening before
update their value.

You can also use by script by issuing an http request to
Z-Wave REST server.

Replace ip\_jeedom, node\_id, instance\_id, cc\_id and index

http://token:\#APIKEY\#@ip\_jeedom:8083/ZWaveAPI/Run/devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

Access to the REST API has changed, see details
[here](./restapi.asciidoc).

Transfer the modules to a new controller
------------------------------------------------

For different reasons, you may have to transfer
all of your modules on a new main controller.

You decide to go from **raZberry** has a **Z-Stick Gen5** or because
that, you have to perform a **Reset** complete of main controller.

Here are different steps to get there without losing your scenarios,
value widgets and history:

-   1 \) Make a Jeedom backup.

-   2 \) Remember to write down (screenshot) your parameter values for each
    module, they will be lost due to exclusion.

-   3 \) In the Z-Wave configuration, uncheck "Delete
    automatically exclude devices "and back up.
    network reboots.

-   4a) In the case of a **Reset**, Reset the controller
    main and restart the plugin.

-   4b) For a new controller, stop Jeedom, disconnect the old one
    controller and plug in the new. Start Jeedom.

-   5 \) For each Z-Wave device, change the ZWave ID to **0**.

-   6 \) Open 2 pages of the Z-Wave plugin in different tabs.

-   7 \) (Via the first tab) Go to the configuration page of a
    module you want to include in the new controller.

-   8 \) (Via second tab) Exclude then include
    of the module. New equipment will be created.

-   9 \) Copy the Z-Wave ID of the new equipment, then delete
    this equipment.

-   10 \) Return to the tab of the old module (1st tab) then paste
    the new ID in place of the old ID.

-   11 \) ZWave parameters were lost during exclusion / inclusion,
    remember to reset your specific settings if you are not using the
    default values.

-   11 \) Repeat steps 7 to 11 for each module to be transferred.

-   12 \) At the end, you should no longer have equipment in ID 0.

-   13 \) Check that all the modules are correctly named in the screen of
    health Z-Wave. Start Synchronization if this is not the case.

Replace a faulty module
------------------------------

How to redo the inclusion of a faulty module without losing your
value scenarios, widgets and history

If the module is assumed to be "Dead" :

-   Note (screenshot) your parameter values, they will be lost
    following inclusion.

-   Go to the actions tab of the module and launch the command
    "Replace failed node".

-   The controller is in inclusion mode, proceed with inclusion according to the
    Module documentation.

-   Reset your specific parameters.

If the module is not presumed to be "Dead" but is still accessible:

-   In the ZWave configuration, uncheck "Delete
    automatically excluded devices".

-   Note (screenshot) your parameter values, they will be lost
    following inclusion.

-   Exclude the faulty module.

-   Go to the configuration page of the faulty module.

-   Open the ZWave plugin page in a new tab.

-   Include the module.

-   Copy the ID of the new module, then delete this equipment.

-   Return to the tab of the old module then paste the new ID to
    the place of the old ID.

-   Reset your specific parameters.

Ghost node removal
----------------------------

If you have lost all communication with a battery-powered module and
you want to exclude it from the network, it is possible that the exclusion
does not succeed or the node remains present in your network.

Automatic ghost node assistant is available.

-   Go to the actions tab of the module to delete.

-   He will probably have a status **CacheLoad**.

-   Start command **Remove ghost node**.

-   Z-Wave network stops. The automatic assistant modifies the
    File **zwcfg** to remove the CC WakeUp from the module. The
    network reboots.

-   Close the module screen.

-   Open the Z-Wave Health screen.

-   Wait for the start-up cycle to be completed (topology loaded).

-   The module will normally be marked as presumed dead.

-   The next minute you should see the node disappear from the screen
    health.

-   If in the Z-Wave configuration, you have unchecked the option
    "Automatically remove excluded devices ", you'll need to
    manually delete the corresponding equipment.

This wizard is only available for battery modules.

Post-inclusion actions
----------------------

It is recommended to perform the inclusion at least 1M from the controller
main, but it will not be the final position of your new module.
Here are some good practices to follow following the inclusion of a new
module in your network.

Once inclusion is complete, a number of
parameters to our new module in order to get the most out of it. Reminder,
modules, following inclusion, have the default settings of
constructor. Enjoy being next to the controller and the interface
Jeedom to properly configure your new module. It will also be more
simple to wake up the module to see the immediate effect of the change.
Some modules have specific Jeedom documentation in order for you
help with different parameters as well as recommended values.

Test your module, validate information feedback, status feedback
and possible actions in the case of an actuator.

During the interview, your new module looked for its neighbors.
However, the modules in your network do not yet know your
new module.

Move your module to its final location. Start the update
of his neighbors and wake him up again.

![troubleshooting07](../images/troubleshooting07.png)

We see that he sees a certain number of neighbors but that the
neighbors don't see it.

To remedy this situation, the action must be taken to treat the
network, in order to ask all the modules to find their neighbors.

This action can take 24 hours before being finished, your modules
on battery will perform the action only the next time they wake up.

![troubleshooting08](../images/troubleshooting08.png)

The option to treat the network twice a week allows you to do this
process without action on your part, it is useful when setting up
places new modules and or when they are moved.

No battery condition feedback
-------------------------------

Z-Wave modules very rarely send their battery status to the
controller. Some will do it at inclusion then only when
this reaches 20% or another critical threshold value.

To help you better monitor the status of your batteries, the Batteries screen
under the Analysis menu gives you an overview of the status of your
Battery. A low battery notification mechanism is also
disponible.

The value returned from the Batteries screen is the last known in the
cache.

Every night, the Z-Wave plugin asks each module to refresh
Battery value. The next time you wake up, the module sends the value to
Jeedom to be added to the cache. So you usually have to wait until
at least 24 hours before obtaining a value in the Batteries screen.

> **Tip**
>
> It is of course possible to manually refresh the value
> Battery via the Values tab of the module then either wait for the next
> alarm or manually waking up the module to obtain a
> immediate recovery. The Wake-up Interval of the module
> is defined in the System tab of the module. To optimize the life of
> your batteries, it is recommended to space this delay as much as possible. For 4h,
> apply 14400, 12h 43200. Some modules must
> listen regularly to messages from the controller such as
> Thermostats. In this case, it is necessary to think of 15 min or 900. Each
> module is different, so there is no exact rule, this is the case
> by case and by experience.

> **Tip**
>
> The discharge of a battery is not linear, some modules will
> show a large percentage loss in the first days of bet
> in service, then do not move for weeks to empty
> quickly once past 20%.

Controller is being initialized
----------------------------------------

When you start the Z-Wave daemon, if you try to start
immediately an inclusion / exclusion, you risk getting this
message: \* "The controller is being initialized, please
try again in a few minutes"

> **Tip**
>
> After the daemon starts, the controller switches to all of the
> modules to repeat their interview. This behavior is
> completely normal in OpenZWave.

If however after several minutes (more than 10 minutes), you have
still this message, it's not normal anymore.

You have to try the different steps:

-   Make sure that the Jeedom health screen lights are green.

-   Make sure the plugin configuration is in order.

-   Make sure you have selected the correct port for the
    ZWave key.

-   Make sure your Jeedom Network configuration is correct.
    (Attention if you have made a Restore from a DIY installation to
    official image, suffix / jeedom should not be included)

-   Look at the plugin log to see if an error is
    not up.

-   Look the **Console** ZWave plugin, to see if an error
    did not go up.

-   Launch the Demon by **Debug** look again at the **Console** et
    plugin logs.

-   Completely restart Jeedom.

-   Make sure you have a Z-Wave controller, the
    Razberry are often confused with EnOcean (error during
    the command).

We must now start the hardware tests:

-   The Razberry is well connected to the GPIO port.

-   USB power is sufficient.

If the problem still persists, reset the controller:

-   Completely stop your Jeedom via the stop menu in the
    user profile.

-   Disconnect the power.

-   Remove the USB dongle or Razberry as appropriate, approximately
    5 minutes.

-   Re connect everything and try again.

The controller no longer responds
----------------------------

No more orders are transmitted to the modules, but returns
of states went up towards Jeedom.

Controller message queue may be full.
See the Z-Wave Network screen if the number of pending messages does not
qu'augmenter.

In this case you have to restart the Demon Z-Wave.

If the problem persists, you must reset the controller:

-   Completely stop your Jeedom via the stop menu in the
    user profile.

-   Disconnect the power.

-   Remove the USB dongle or Razberry as appropriate, approximately
    5 minutes.

-   Re connect everything and try again.

Error during dependencies
---------------------------

Several errors can occur when updating
Dependencies. You must consult the dependency update log
in order to determine what exactly is the error. Generally,
the error is at the end of the log in the last few lines.

Here are the possible problems and their possible solutions:

-   could not install mercurial - abort

The mercurial package does not want to install, to correct launch in
ssh:

````
    sudo rm /var/lib/dpkg/info/$mercurial* -f
    sudo apt-gand install mercurial
````

-   Addictions seem blocked on 75%

At 75% this is the start of the compilation of the openzwave library as well
openzwave python wrapper. This step is very long, we can
however consult the progress via the update log view. he
so just be patient.

-   Error when compiling the openzwave library

````
        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed source if appropriate.
        See <file:///usr/share/doc/gcc-4.9/README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targand 'build' failed
        make: *** [build] Error 1
````

This error can occur due to a lack of RAM memory during the
compilation.

From the jeedom UI, launch the compilation of dependencies.

Once launched, in ssh, stop these processes (consumers in
memory) :

````
    sudo systemctl stop cron
    sudo systemctl stop apache2
    sudo systemctl stop mysql.
````

To follow the progress of the compilation, we tailor the
openzwave\_update log file.

````
    tail -f /var/www/html/log/openzwave_update
````

When the compilation is complete and without error, restart the
services you stopped

sudo systemctl start cron sudo systemctl start apache2 sudo systemctl
start mysql

Using the Razberry card on a Raspberry Pi 3
------------------------------------------------------

To use a Razberry controller on a Raspberry Pi 3, the
Raspberry's internal Bluetooth controller must be disabled.

Add this line:

````
    dtoverlay=pi3-miniuart-bt
````

At the end of the file:

````
    /boot/config.txt
````

Then restart your Raspberry.

HTTP API
========

The Z-Wave plugin provides developers and users
a complete API in order to operate the Z-Wave network via request
HTTP.

You can use all of the methods exposed by the
Z-Wave daemon REST server.

The syntax for calling routes is in this form:

URLs =
[http://token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/ \#ROUTE\#](http://token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/#ROUTE#)

-   \#API\_KEY\# corresponds to your API key, specific to
    your installation. To find it, go to the menu «
    Main », puis « Administration » and « Setup », en activant
    Expert mode, you will then see an API Key line.

-   \#IP\_JEEDOM\# corresponds to your Jeedom access url.

-   \#PORTDEMON\# corresponds to the port number specified in the page of
    configuration of the Z-Wave plugin, by default: 8083.

-   \#ROUTE\# corresponds to the route on the REST server to execute.

To know all the routes, please refer
[Github](https://github.com/jeedom/plugin-openzwave) of the Z-Wave plugin.

Example: To ping the node id 2

URLs =
http://token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ZWaveAPI/Run/devices\[2\].TestNode()

# FAQ

> **I get the error "Not enough space in stream buffer"**
>
> Unfortunately this error is hardware, there is nothing we can do and we are looking for the moment how to force a restart of the daemon in the case of this error (but often it is also necessary to unplug the key for 5 min so that it starts again)
