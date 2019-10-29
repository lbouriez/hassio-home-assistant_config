import appdaemon.plugins.hass.hassapi as hass

class RemoteControl(hass.Hass):

    def initialize(self):
        self.event_name = "app_daemon_remote"
        if 'event' in self.args:
            self.listen_event(self.handle_event, self.args['event'])

    def handle_event(self, event_name, data, kwargs):
        if data['id'] == self.args['id']:
            self.log(data['event'])
            if data['event'] == 1002:
                self.log('Button on short release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="on", detail="sr")
            if data['event'] == 1001:
                self.log('Button on hold')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="on", detail="hold")
            if data['event'] == 1003:
                self.log('Button on long release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="on", detail="lr")
            elif data['event'] == 2002:
                self.log('Button dim up short release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="dimup", detail="sr")
            elif data['event'] == 2001:
                self.log('Button dim up hold')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="dimup", detail="hold")
            elif data['event'] == 2003:
                self.log('Button dim up long release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="dimup", detail="lr")
            elif data['event'] == 3002:
                self.log('Button dim down short release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="dimdown", detail="sr")
            elif data['event'] == 3001:
                self.log('Button dim down hold')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="dimdown", detail="hold")
            elif data['event'] == 3003:
                self.log('Button dim down long release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="dimdown", detail="lr")
            elif data['event'] == 4002:
                self.log('Button off short release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="off", detail="sr")
            elif data['event'] == 4001:
                self.log('Button off hold')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="off", detail="hold")
            elif data['event'] == 4003:
                self.log('Button off long release')
                self.fire_event(self.event_name, entity_id = self.args['id'], state="off", detail="lr")