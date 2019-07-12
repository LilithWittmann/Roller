# What's this?

In this folder, you can specify production-specific settings that are used with
Travis CI, and that you should then also use with your deployment pipeline.

When you start the project from our cookiecutter template, the contents of these
files will pretty much be the same as the ones for a dev environment
(`local_settings.py` in the parent folder from here). However, this might not be
what you need later in your project, and it's a good idea to separate out these
production-specific settings into their own files, to not collide with what you
(or other devs) might need for their local setup.

**IMPORTANT**: This is *not* a place to store sensitive information like actual
database passwords, sensitive API keys or other information! You should always
transmit this data in an encrypted fashion and only use it on your production
server. **Never** store it here, or it'll accidentally end up in version control
and sensitive information will be compromised. Thanks :)