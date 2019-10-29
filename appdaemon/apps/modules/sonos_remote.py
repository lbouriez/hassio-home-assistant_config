import appdaemon.plugins.hass.hassapi as hass

class SonosRemote(hass.Hass):

    def initialize(self):
        self.sonos = self.args['sonos']
        if 'event' in self.args:
            self.listen_event(self.handle_event, self.args['event'])

    def handle_event(self, event_name, data, kwargs):
        if data['id'] == self.args['id']:
            if data['event'] == 1002:
                self.log('Button toggle')
                self.call_service("media_player/media_play_pause", entity_id = self.sonos)

            elif data['event'] == 2002:
                self.log('Button volume up')
                self.call_service("media_player/volume_up", entity_id = self.sonos)

            elif data['event'] == 3002:
                self.log('Button volume down')
                self.call_service("media_player/volume_down", entity_id = self.sonos)

            elif data['event'] == 4002:
                self.log('Button previous')
                self.call_service("media_player/media_previous_track", entity_id = self.sonos)

            elif data['event'] == 5002:
                self.log('Button next')
                self.call_service("media_player/media_next_track", entity_id = self.sonos)
