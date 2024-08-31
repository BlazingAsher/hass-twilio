# Home Assistant Twilio Integration

This is basically the original Home Assistant Twilio integration, but with support for using a Twilio API key instead of using an account secret.

I would have contributed this back to the core repo, but since the integration was made, Home Assistant seems to have tightened the policy around using configuration files to configure service integrations, and I regrettably don't have too much time to look into how to do it that way.

To install this integration, you can use HACS and add this as a custom repository. It will override the default integration and so the Twilio SMS and Call integrations will use the new configuration.

The original Home Assistant code along with my changes are all released under the Apache 2.0 license.
