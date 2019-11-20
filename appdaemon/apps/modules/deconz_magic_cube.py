"""
Recreating xiaomi aqara binary sensor platform for cube
https://www.home-assistant.io/components/binary_sensor.xiaomi_aqara/
https://github.com/iago1460/fast-deploy/blob/master/config_template/appdaemon/apps/cube.py
"""
import appdaemon.plugins.hass.hassapi as hass
from enum import Enum

class Action(str, Enum):
    FLIP90 = 'flip90'
    FLIP180 = 'flip180'
    MOVE = 'move'  # = slide
    TAP_TWICE = 'tap_twice'
    SHAKE_AIR = 'shake_air'
    ALERT = 'alert'  # = wake?
    FREE_FALL = 'free_fall'
    ROTATE = 'rotate'

class DeconzMagicCube(hass.Hass):
    
    def initialize(self):
        self.event_name = "app_daemon_magic_cube"
        if 'event' in self.args:
            self.listen_event(self.handle_event, self.args['event'])

    def handle_event(self, event_name, data, kwargs):
        if data['id'] == self.args['id']:
            self.sensor_name = "sensor." + self.args['id']
            if data['event'] in [1000, 2000, 3000, 4000, 5000, 6000]:
                self.log('Magic move')
                to_side = data['event'] // 1000
                self.set_state(self.sensor_name, state = to_side)
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.MOVE)
            elif data['event'] in [1001, 2002, 3003, 4004, 5005, 6006]:
                to_side = data['event'] % 1000
                self.set_state(self.sensor_name, state = to_side)
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.TAP_TWICE)
                self.log('Magic tap twice to ' + str(to_side))
            elif data['event'] in [1006, 2005, 3004, 4003, 5002, 6001]:
                self.log('Magic flip 180')
                from_side = data['event'] % 1000
                to_side = data['event'] // 1000
                self.set_state(self.sensor_name, state = to_side, attributes={'from_side': from_side})
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.FLIP180)
            elif data['event'] in [1002, 1003, 1004, 1005, 2001, 2003, 2004, 2006, 3001, 3002, 3005, 3006, 4001, 4002, 4005, 4006, 5001, 5003, 5004, 5006, 6002, 6003, 6004, 6005]:
                self.log('Magic flip 90')
                from_side = data['event'] % 1000
                to_side = data['event'] // 1000
                self.set_state(self.sensor_name, state = to_side, attributes={'from_side': from_side})
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.FLIP90)
            elif data['event'] == 7007:
                self.log('Magic shake')
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.SHAKE_AIR)
            elif data['event'] == 7008:
                self.log('Magic drop')
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.FREE_FALL)
            elif data['event'] == 7000:
                self.log('Magic alert')
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.ALERT)
            else:
                degrees = data['event'] / 100
                self.fire_event(self.event_name, entity_id = self.args['id'], action_type = Action.ROTATE, action_value = degrees)
                self.log('Magic rotate to ' + str(degrees))
