"""Support for Twilio.
This file has been modified from the original to add support for Twilio's API Key and Secret.
"""

from aiohttp import web
from twilio.rest import Client
import voluptuous as vol

from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_entry_flow
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

CONF_ACCOUNT_SID = "account_sid"
CONF_AUTH_TOKEN = "auth_token"
CONF_API_KEY = "api_key"
CONF_API_SECRET = "api_secret"

DATA_TWILIO = DOMAIN

RECEIVED_DATA = f"{DOMAIN}_data_received"

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(DOMAIN): vol.Schema(
            {
                vol.Required(CONF_ACCOUNT_SID): cv.string,
                vol.Optional(CONF_AUTH_TOKEN): cv.string,
                vol.Optional(CONF_API_KEY): cv.string,
                vol.Optional(CONF_API_SECRET): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Twilio component."""
    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]

    if conf.get(CONF_AUTH_TOKEN):
        hass.data[DATA_TWILIO] = Client(
            conf.get(CONF_ACCOUNT_SID), conf.get(CONF_AUTH_TOKEN)
        )
    elif conf.get(CONF_API_KEY) and conf.get(CONF_API_SECRET):
        hass.data[DATA_TWILIO] = Client(
            conf.get(CONF_API_KEY),
            conf.get(CONF_API_SECRET),
            conf.get(CONF_ACCOUNT_SID),
        )
    else:
        raise HomeAssistantError("Invalid Twilio configuration")
    return True


async def handle_webhook(
    hass: HomeAssistant, webhook_id: str, request: web.Request
) -> web.Response:
    """Handle incoming webhook from Twilio for inbound messages and calls."""
    data = dict(await request.post())
    data["webhook_id"] = webhook_id
    hass.bus.async_fire(RECEIVED_DATA, dict(data))

    return web.Response(text="")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure based on config entry."""
    webhook.async_register(
        hass, DOMAIN, "Twilio", entry.data[CONF_WEBHOOK_ID], handle_webhook
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])
    return True


async_remove_entry = config_entry_flow.webhook_async_remove_entry
