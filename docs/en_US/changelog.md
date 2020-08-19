# Changelog Z-Wave

>**Important**
>
>As a reminder if there is no information on the update, it means that it only concerns the updating of documentation, translation or text

# 07/10/2019

- Fixed a bug when stopping the daemon
- Bugfix
- THIS UPDATE NEEDS TO RECOMPILE THE DEPENDENCIES (RELAUNCH)

# 19-09-2019

- Display bug correction

# 10-09-2019

- Fixed a problem with the display of the routing table

# 09-09-2019
- Adapting dependencies for Debian10 Buster
- Modification allowing to separate the outputs on smart implant (this function requires a recompilation of dependencies)

04-02-2019
===
- THIS UPDATE NEEDS TO RECOMPILE THE DEPENDENCIES (RELAUNCH)
- Correction of a bug on multi-instances of thermostats
- Creation of a queue level deprecated on actions for refreshes
- Addition of many confs (to recall the button to recover confs is useful to be up to date without updating the plugin)
- Improved management of encapsulated multichannels
- Addition of CC manufacturer specific
- Simple installation of the CC Soundswitch
- Fix for multiple inclusion of devices <
- Improved CC Switch Binary
- Entering manual parameters is always possible
- Tail enhancement
- Preparation for adding new CCs (notification in particular)
- Addition of codes on the CC alarm for Zipato keypad for the moment
- Correction of the philio in secure mode which during the ringtones generated a timeout of 10 seconds (it is surely necessary to regenerate the detection of the siren or to re-include it)
- Correction of a bug if the log level is none
- THIS UPDATE NEEDS TO RECOMPILE THE DEPENDENCIES

2018-03-17
===

- Change of branch for recovery of confs during syncconf (following a change in the organization of githubs)

2018-01-17 / 2018-01-19
===

-   New Arrivals

    -   Return of the possibility to synchronize confs without updating the plugin

    -   Improvements

    -   Addition of the internal possibility of triggering refreshes on certain specific values and specific modules (used in jeedom confs)

    -   Complete redesign of the function allowing to simulate a value on another command to avoid putting it for a set of modules but specifically (internal Jeedom)

-   Fixed bug

    -   Fixed a bug that caused auto generated confs to be in the old format and therefore unusable

    -   Correction of the bug of the loss of the pending setpoint on the thermostatic valves (goes with point 2 of the improvements)

    -   Reduction of the size of the images to limit the size of the plugin as much as possible (approximately 500 images)

    -   Removal of more used dependencies such as Mercurial Sphinx etc…

    -   Suppression of the purge of the configurations before update (avoids having Zwave icons in place of the images in case of unsuccessful updates for timeout or other)

2017-08-xx
===


-   New Features

    -   Possibility to refresh orders for equipment without
        delete existing ones.

    -   Possibility of creating an information command on the values of
        System tab.

-   Improvements / Enhancements

    -   Support for new modules, ozw definitions
        and orders.

    -   Ability to select the default association
        (without instance) on the modules supporting the
        multi-instance associations.

    -   Verification of the validity of association groups at the end
        of the interview.

    -   Recovery of the last level of the batteries when the daemon starts.

-   Fixed bug

    -   Correction of the migration of the Battery info.

    -   Correction of the battery info feedback in
        the Equipment screen.

    -   Battery type restoration in configurations
        of modules.

    -   Correction of actions on button type values in
        module screen.

    -   Correction of the retrieval of parameter translations.

    -   Correction of empty error on modification of RAW type values
        (RFid code).

    -   Fixed display of pending values
        to be applied.

    -   Suppression of notification of change in value before
        that it is not applied.

    -   No longer display the padlock on the module screen if the module
        does not support Security Command Class.

    -   Application of manual refresh in
        recommended settings.

    -   Badge management assistant for RFID readers.

    -   Correction of the assistant of detection of unknown modules.

    -   Correction of the wizards of "Resume from .." and "Apply
        on ... "in the settings tab.

2017-06-20
===

-   New Features

    -   N / A

-   Improvements / Enhancements

    -   Add all the module configurations to the
        new format.

-   Fixed bug

    -   Do not test if a nodeId exists during the deletion
        of an association.

    -   Restoring the pending deposit notification on
        thermostats.

    -   Sending Pending Activation Scene 1.

    -   No longer display the padlock in the health screen on
        modules not supporting the Security Command Class.

    -   Repetition of value on the remote controls before the end of
        the interview (kyefob, minimote).

    -   Modify a parameter of type list by value via a
        Action command.

    -   Modify a parameter on a module without defined configuration.

2017-06-13
===

-   New Features

    -   N / A

-   Improvements / Enhancements

    -   Addition of Fibaro US module configuration

-   Fixed bug

    -   N / A

2017-05-31
===

-   New Features

    -   N / A

-   Improvements / Enhancements

    -   N / A

-   Fixed bug

    -   Correction of the assignment of values in RAW format of codes
        for RFid reader.

2017-05-23
===

-   New Features

    -   Removal of master / slave mode. Replaced by plugin
        Jeedom Link.

    -   Use of a private API key to the ZWave plugin.

    -   New format of the configuration files in the mapping of
        order with jeedom.

    -   Automatic conversion of existing orders to new
        format when installing the plugin.

    -   Added support for the Central Scene Command Class.

    -   Added support for Barrier Operator Command Class.

-   Improvements / Enhancements

    -   Complete overhaul of the REST server using TORNADO.

        -   Modification of all existing roads,
            scripts will need to be adapted if using the ZWave API.

        -   Reinforcement of security, only calls are listened to on
            the REST server.

        -   Using the required ZWave API key to launch
            REST requests.

    -   Disabling (temporary) health tests.

    -   (Temporary) deactivation of the update engine
        module configurations.

    -   Deactivation of the Heal Network function automatically
        twice a week (decrease in exchanges with
        The controller).

    -   Openzwave library code optimizations.

        -   Fibaro FGK101 no longer has to complete the interview to announce
            a change of state.

        -   The release button command (Stop of a shutter) no longer forces
            updating all the module values
            (decrease in message queue).

        -   Possibility to notify values in the Class of
            Alarm command (ringtone selection on sirens)

    -   More daily demand for battery level (less than
        messages, saving on batteries).

    -   The battery level is sent directly to the battery screen on
        receiving level report.

-   Fixed bug

    -   Refreshing of all instances following a
        CC Switch ALL broadcast.

2016-08-26
===

-   New Features

    -   Aucune

-   Improvements / Enhancements

    -   RPI3 detection in dependency update.

    -   Activate the default non-secure inclusion mode.

-   Fixed bug

    -   Test manufacturer information in the health screen does
        no more NOK.

    -   Loss of check boxes in the Commands tab of the
        equipment page.

2016-08-17
===

-   New Features

    -   Relaunch of the demon if detection of the controller in timeout during
        controller initialization.

-   Improvements / Enhancements

    -   OpenZWave library update 1.4.2088.

    -   Spelling correction.

    -   Redesign of the equipment screen with tabs.

-   Fixed bug

    -   Problem displaying certain modules on the routing table
        and Network Graph.

    -   Vision Secure modules that do not return to standby
        during the interview.

    -   Installation of dependencies in a loop (github side problem).

2016-07-11
===

-   New Features

    -   Support for restoration of the last known level on
        dim them.

    -   Distinction of FLiRS modules in the health screen.

    -   Added request to update return routes
        to the controller.

    -   Assistant to apply the configuration parameters of a
        module to several other modules.

    -   Identification of the Zwave + supporting modules
        COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO.

    -   Display of the security status of modules supporting
        COMMAND\_CLASS\_SECURITY.

    -   Addition of the possibility to select instance 0 of the
        controller for multi-instance associations.

    -   Securing all calls to the REST server.

    -   Automatic dongle detection, in the configuration page
        plugin.

    -   Inclusion dialog with choice of inclusion mode for
        simplify secure inclusion.

    -   Taking into account deactivated equipment within the
        Z-Wave motor.

        -   Gray display in the health screen without analysis on
            the knot.

        -   Hidden in the Network Table and Network Graph.

        -   Disabled nodes, exclude health tests.

-   Improvements / Enhancements

    -   Optimization of sanitary controls.

    -   Network graph optimization.

    -   Improved main controller detection for
        group test.

    -   Update to the OpenZWave library 1.4.296.

    -   Optimization of the background cooling of the drives.

    -   Optimized background refresh for
        engines.

    -   Adaptation for Jeedom core 2.3

    -   Health screen, column name modification and warning
        in the event of non-communication with a module.

    -   Optimization of the REST server.

    -   Correction of the spelling of the screens, thank you @ Juan-Pedro
        aka: kiko.

    -   Updating the plugin documentation.

-   Fixed bug

    -   Correction of possible problems when updating
        module configurations.

    -   Network graph, calculation of jumps on the controller id
        principal and not assume ID 1.

    -   Management of the button add a group association.

    -   Display of False values in the Configuration tab.

    -   No longer assume the current date on the state of the batteries if not received
        equipment report.

2016-05-30
===

-   New Features

    -   Added option to enable / disable controls
        sanitary on all modules.

    -   Adding a Notifications tab to view the last 25
        controller notifications.

    -   Adding a route to recover the health of a node.
        ip\_jeedom:8083 / ZWaveAPI / Run / devices \ [node\_id \]. GetHealth()

    -   Adding a route to retrieve the last notification
        of a knot.
        ip\_jeedom:8083 / ZWaveAPI / Run / devices \ [node\_id \]. GetLastNotification()

-   Improvements / Enhancements

    -   Allow the selection of FLiRS modules during
        direct associations.

    -   Allow the selection of all instances of modules during
        direct associations.

    -   OpenZWave python wrapper update to version 0.3.0.

    -   OpenZWave 1.4.248 library update.

    -   Do not display an expired wakeup warning for
        battery powered modules.

    -   Validation that a module is identical at the ids level for
        allow copying of parameters.

    -   Simplification of the wizard for copying parameters.

    -   Hide non-occurring system tab values
        to be displayed.

    -   Display of the description of the controller capabilities.

    -   Documentation update.

    -   Correction of the spelling of the documentation, thank you
        @Juan-Pedro aka: kiko.

-   Fixed bug

    -   Spelling correction.

    -   Fixed inclusion in secure mode.

    -   Correction of asynchronous call. (error: \ [Errno 32 \]
        Broken pipe)

2016-05-04
===

-   New Features

    -   Added option to turn off background refresh
        dimmers.

    -   Display of associations with which a module is associated
        (find usage).

    -   Added support for CC MULTI\_INSTANCE\_ASSOCIATION.

    -   Adding an info notification when applying
        Set\_Point in order to use the setpoint requested under
        cmd info form.

    -   Adding a recommended configuration wizard.

    -   Add option to activate / deactivate the assistant
        recommended configuration when including
        new modules.

    -   Add option to activate / deactivate the update of
        module configurations each night.

    -   Addition of a route to manage multiple association instances.

    -   Add missing Query Stage.

    -   Added validation of the selection of the USB Dongle to the
        starting the demon.

    -   Addition of validation and test of callback at startup
        of the demon.

    -   Added option to turn off automatic update
        module config.

    -   Adding a route to modify the log traces at runtime
        the REST server. Note: no effect on the OpenZWave level.
        <http://ip_jeedom:8083/ZWaveAPI/Run/ChangeLogLevel(level>) level
        ⇒ 40:Error, 20: Debug 10 Info

-   Improvements / Enhancements

    -   Update of the OpenZWave python wrapper to version 0.3.0b9.

    -   Highlighting groups of associations that are pending
        to be applied.

    -   Update to the OpenZWave library 1.4.167.

    -   Modification of the direct association system.

    -   Documentation update

    -   Ability to start regeneration of node detection
        for all identical modules (make and model).

    -   Display in the health screen if configuration items
        are not applied.

    -   Display in the equipment screen if elements of
        configuration are not applied.

    -   Display in the health screen if a battery module has not
        never woke up.

    -   Display in the health screen if a battery module has exceeded
        the expected wake-up time.

    -   Adding traces upon notification error.

    -   Better recovery of battery status.

    -   Summary / health compliance for battery thermostats.

    -   Better detection of modules on batteries.

    -   Debug mode optimization for the REST server.

    -   Force a switch state update and dimer
        following the sending of a switch all command.

-   Fixed bug

    -   Fixed discovery of association groups.

    -   Correction of the error "Exception KeyError: (91,) in
        'libopenzwave.notif\_callback 'ignored".

    -   Correction of the selection of module documentation for
        modules with multiple profiles.

    -   Management of the action buttons of the module.

    -   Correction of description of generic name of class.

    -   Correction of the backup of the zwcfg file.

2016-03-01
===

-   New Features

    -   Adding the Configuration button via the management screen
        equipment.

    -   Addition of new module interview states.

    -   Editing labels in UIs.

-   Improvements / Enhancements

    -   Better management of module actions buttons.

    -   Documentation Adding sections.

    -   Optimization of the daemon state detection mechanism.

    -   Protest mechanism during the recovery of the
        description of the parameters if it contains characters
        not valid.

    -   Never go back to the battery status information on a
        module connected to the mains.

    -   Documentation update.

-   Fixed bug

    -   Documentation Spelling and grammatical corrections.

    -   Validation of the content of the zwcfg file before applying it.

    -   Installation correction.

2016-02-12
===

-   Improvements / Enhancements

    -   No dead node alert if it is disabled.

-   Fixed bug

    -   Correction of Fibaro pilot wire return of status.

    -   Correction of a bug which recreate the commands during the setting
        up to date.

2016.02.09
===

-   New Features

    -   Addition of push notification in node\_event case, allows
        implementation of a cmd info in CC 0x20 to recover
        event on nodes.

    -   Added ForceRefresh route
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ForceRefresh()
        can be used in orders.

    -   Adding the SwitchAll route
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[1\].commandClasses\[0xF0\].SwitchAll(&lt;int:state&gt;)
        available via the main controller.

    -   Adding the ToggleSwitch route
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ToggleSwitch()
        can be used in orders.

    -   Addition of a push notification in case of presumed dead node.

    -   Ajout de la commande “refresh all parameters” dans
        the Settings tab.

    -   Addition of the parameter information waiting to be applied.

    -   Adding network notification.

    -   Addition of a legend in the network graph.

    -   Addition of the network care function via the routing table.

    -   Automatic ghost node removal with just one click.

    -   Management of actions on node according to the state of the node and the type.

    -   Management of network actions according to network status.

    -   Update of the automatic module configuration all
        the nights.

-   Improvements / Enhancements

    -   Complete refactoring of the REST server code, optimization of
        starting speed, readability, compliance with convention
        naming.

    -   Square logs.

    -   Simplification of the manual 5min refresh management with
        possibility to apply on nodes on batteries.

    -   Update of the OpenZWave library in 1.4

    -   Modification of the health test to revive the presumed nodes
        dead more easily without user actions.

    -   Use of bright colors in the routing table and
        network graph.

    -   Standardization of the colors of the routing table and the
        network graph.

    -   Optimization of information on the Z-Wave health page according to
        the state of the interview.

    -   Better management of read-only or write parameters
        only in the Settings tab.

    -   Improved warning on battery thermostats.

-   Fixed bug

    -   Temperature converted to Celsius returns unit C instead
        from F.

    -   Correction of the refresh of values at startup.

    -   Correction of the Refresh by value in the Values tab.

    -   Correction of generic module names.

    -   Correction of the ping on the nodes in Timeout during the
        health test.
