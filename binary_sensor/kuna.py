"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.kuna/
"""
import logging

from homeassistant.components.binary_sensor import BinarySensorDevice

DEPENDENCIES = ['kuna']
DOMAIN = 'kuna'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):

    kuna = hass.data[DOMAIN]

    devices = []

    for camera in kuna.account.cameras:
        device = KunaBinarySensor(kuna, camera)
        devices.append(device)

    add_entities(devices)


class KunaBinarySensor(BinarySensorDevice):

    def __init__(self, kuna, camera):
        self._account = kuna
        self._camera = camera
        self._original_id = self._camera.serial_number
        self._name = '{} Motion'.format(self._camera.name)
        self._unique_id = '{}-Motion'.format(self._camera.serial_number)
        self._device_class = 'motion'

    @property
    def should_poll(self):
        return False

    @property
    def available(self):
        return self._camera.status

    @property
    def unique_id(self):
        """Return the unique ID of the binary sensor."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the class of the binary sensor."""
        return self._device_class

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._camera.recording_active

    def update(self):
        """Read new state data from the library."""
        kuna = self._account
        for camera in kuna.account.cameras:
            if camera.serial_number == self._original_id:
                self._camera = camera

    def update_callback(self):
        """Schedule a state update."""
        self.schedule_update_ha_state(True)

    async def async_added_to_hass(self):
        """Add callback after being added to hass."""
        self._account.add_update_listener(self.update_callback)
