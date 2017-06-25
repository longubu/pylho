# pylho: Personal package to make my life easier
Non-general purpose package that facilitates my personal workflow for analyzing
data and working on ds/ml projects.

Note, this is *not* mean't to be a general utility package used across
different projects, such as general io functions. Projects should be
self-contained and not depend on external personal packages.

## Modules
- [Alerts](alerts): Functions to send alerts via online/mobile messaging
- [Colors](colors): Helper functions for selecting color palettes.
- [Terminal](terminal): Utility functions for dealing with bash terminal
- [Debug](debug): Functions useful for debugging.
- [Log_Off_User](log_off_user): Function to log off any bash user (use !who to look for user's id#). Note: requires sudo access to log off other users.