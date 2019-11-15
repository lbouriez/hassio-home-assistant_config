import appdaemon.plugins.hass.hassapi as hass

#
# App which set the symfonisk remote
#
# Args:
#   [event] {string} -- Event name that will be fired (ex: deconz_event)
#   [remotes] {list} -- List of the symfonisk remote id in DeconZ (ex: - symfonisk_sound_controller)
#   [sonos] {list} -- List of the sonos media player to control (ex: - media_player.bathroom)
#   [sources] {list} -- Name of the source to play when double clicking (ex: - 'Sonos favoris name')
#   [play_shuffle] {boolean} -- Shuffle play the playlist
#
# Release Notes
#
# Version 1.2:
#   Bug fixes
#
# Version 1.1:
#   Handling volume
#
# Version 1.0:
#   Initial Version

# Define the max time when the volume can change
# There to avoid an unlimited change when
# not receiveing stop event
CHANGE_VOLUME_TIME_MAX = 5
# Define the interval between
# each call to change volume, smaller = faster
CHANGE_VOLUME_INTERVAL = 1

class DeconzSymfoniskRemote(hass.Hass):
    """ [summary]
        [event] {string} -- Event name that will be fired (ex: deconz_event)
        [remotes] {list} -- List of the symfonisk remote id in DeconZ (ex: - symfonisk_sound_controller)
        [sonos] {list} -- List of the sonos media player to control (ex: - media_player.bathroom)
        [sources] {list} -- Name of the source to play when double clicking (ex: - 'Sonos favoris name')
        [play_shuffle] {boolean} -- Shuffle play the playlist
    """

    def initialize(self):
        self.handle_params()
        if 'event' in self.args:
            self.listen_event(self.handle_event, self.args['event'])

    def handle_params(self):
        self.log(self.args)
        self.event_name = "app_daemon_symfonisk"
        self.sonos = self.args.get('sonos')
        self.sources = self.args.get('sources')
        self.remotes = self.args.get('remotes')
        self.play_shuffle = self.args.get('play_shuffle', False)
        self.initial_source = 0
        self.volume_change = False

    def handle_source(self):
        selected_source = self.sources[self.initial_source]
        self.initial_source += 1
        if self.initial_source >= len(self.sources):
            self.initial_source = 0
        return selected_source
    
    def disable_volume_change(self, kwargs):
        self.log("Change volume disabled by " + kwargs["emit"])
        self.volume_change = False

    def handle_volume(self, kwargs):
        self.log("Change volume loop " + kwargs["way"])
        self.call_service("media_player/volume_" + kwargs["way"], entity_id = self.sonos)
        if self.volume_change:
            self.run_in(self.handle_volume, CHANGE_VOLUME_INTERVAL, way = kwargs["way"])

    def handle_event(self, event_name, data, kwargs):
        remote_id = data['id']

        if remote_id in self.remotes:
            if data['event'] == 1002:
                self.log('Button simple click - toggle')
                self.call_service("media_player/media_play_pause", entity_id = self.sonos)
                self.fire_event(self.event_name, entity_id = self.sonos, state="click1")
            elif data['event'] == 1004:
                self.log('Button double click - next track')
                self.call_service("media_player/media_next_track", entity_id = self.sonos)
                self.fire_event(self.event_name, entity_id = self.sonos, state="click2")
            elif data['event'] == 1005:
                self.log('Button triple click - choose source')
                if len(self.sonos) > 1:
                    self.call_service("sonos/join", entity_id = self.sonos, master = self.sonos[0])
                self.call_service("media_player/shuffle_set", entity_id = self.sonos, shuffle = self.play_shuffle)
                self.call_service("media_player/select_source", entity_id = self.sonos, source = self.handle_source())
                self.fire_event(self.event_name, entity_id = self.sonos, state="click3")
            elif data['event'] == 3001:
                self.log('Button volume up')
                self.volume_change = True
                self.handle_volume({'way': 'up'})
                self.run_in(self.disable_volume_change, CHANGE_VOLUME_TIME_MAX, emit = "auto vol up")
                self.fire_event(self.event_name, entity_id = self.sonos, state="volup")
            elif data['event'] == 2001:
                self.log('Button volume down')
                self.volume_change = True
                self.handle_volume({'way': 'down'})
                self.run_in(self.disable_volume_change, CHANGE_VOLUME_TIME_MAX, emit = "auto vol down")
                self.fire_event(self.event_name, entity_id = self.sonos, state="voldown")
            elif data['event'] in [2003, 3003]:
                self.log('Button volume stop')
                self.disable_volume_change({'emit': 'event'})
                self.fire_event(self.event_name, entity_id = self.sonos, state="volstop")
            else:
                self.log('Unkown action: ' + data['event'])
