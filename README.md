# update 2025
You can use the plex integration: https://www.home-assistant.io/integrations/plex/
This will display both your plexamp server, and plexamp clients
You can then see the play/pause status of the plexamp server, as well as pause/resume playback

I can't remember why this didn't work for me before (which lead to the creation of this repo)
It might be something to do with 'scanning for clients': https://www.home-assistant.io/integrations/plex/#button (I have an automation to 'press' that button every minute)

I'll leave the old information, just in case :)

# plexamp_homeassistant
A guide mainly to myself for how to connect PlexAmp and HomeAssistant

## PlexAmp
https://www.plex.tv/plexamp/
https://github.com/odinb/bash-plexamp-installer

## HomeAssistant
https://www.home-assistant.io/
https://tteck.github.io/Proxmox/
Homeassistant OS: `bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/vm/haos-vm.sh)"`

## HomeAssistant Plex Integration
https://www.home-assistant.io/integrations/plex/

## My own 'integration'

### For HomeAssistant:

1. Download the directory: `python_scripts`
2. Move the contents to /config/python_scripts/.
3. Add to your /config/configuration.yaml:
```
shell_command:
    get_plexamp_playing_status: /config/python_scripts/get_plexamp_playing_status.py <plexamp_ip>
    pause_plexamp: /config/python_scripts/pause_plexamp.py <plexamp_ip>
```

Create a Toggle helper from the HomeAssistant UI:
1. Go to Settings
2. Devices & Services
3. Helpers tab
4. Create helper
5. Toggle
6. Name it 'is plexamp playing'

Create an automation
1. Add a time pattern trigger for every second * * *
2. Add an action to call a service.  Call a shel command 'get_plexamp_playing_status'.  Add response variable to 'is_plexamp_playing'
3. Add an action, if/then/else. Within the 'if', create a template, use this: `{{ is_plexamp_playing['stdout'] == '1' }}`. Within the 'then' call service 'input boolean: turn on' and select 'input_boolean.is_plexamp_playing'. Do the same for the else (but you're calling service 'input boolean: turn off'
4. Here is the yaml:
```
alias: get plexamp playing status
description: ""
trigger:
  - platform: time_pattern
    hours: "*"
    minutes: "*"
    seconds: "*"
condition: []
action:
  - service: shell_command.get_plexamp_playing_status
    data: {}
    response_variable: is_plexamp_playing
  - if:
      - condition: template
        value_template: "{{ is_plexamp_playing['stdout'] == '1' }}"
    then:
      - service: input_boolean.turn_on
        data: {}
        target:
          entity_id: input_boolean.is_plexamp_playing
    else:
      - service: input_boolean.turn_off
        data: {}
        target:
          entity_id: input_boolean.is_plexamp_playing
mode: single
```

## Summary
Now you have a toggle that will turn on and off when you're playing music on PlexAmp.  
I have created automations to turn on my Receiver if PlexAmp is playing.  Or to pause PlexAmp if the Receiver source is changed (using the Plex/HomeAssistant integration)

## Things to note
I only have one PlexAmp so I don't have any device checks within the Python code.  If you have multiple PlexAmps, I suspect playing any of them will make the toggle switch to 'on'.  You may be able to work around this by adding some python code to check device ID.
I've not specified how to use the 'pause_plexamp.py' script in an automation (because I'm assuming that will be different for different people), but it should be straightforward enough.  When you call the script, plexamp should get paused

There are also the following PlexAmp APIs that may be helpful to you:
- /resources (which is for Plex discovery protocol GDM)
- /player/playback/play
- /player/playback/pause
- /player/playback/stop
- /player/playback/skipNext
- /player/playback/skipPrevious
- /player/playback/playPause
- /player/playback/playMedia????
- /player/playback/createPlayQueue????
- /player/playback/seekTo?offset=1
- /player/playback/skipTo?key=???&playQueueItemID=???
- /player/playback/setParameters?repeat=???
- /player/playback/setParameters?volume=0
- /player/playback/setParameters?volume=100
- /player/playback/setParameters?shuffle=(true/false)
- /player/playback/setParameters?speed=???
