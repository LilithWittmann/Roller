# We are using the Debian-based python base image here to be able to use PyPi wheels.

FROM python:3.6-slim-stretch

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED="1"

# Add unstable branch to sources.list to be able to install pipenv, then update package lists
RUN echo "deb http://deb.debian.org/debian unstable main non-free contrib" | tee -a /etc/apt/sources.list && \
    echo "deb-src http://deb.debian.org/debian unstable main non-free contrib" | tee -a /etc/apt/sources.list
RUN apt-get update
# Install system package dependencies
RUN apt-get install -y libgdal20 wait-for-it pipenv

# Copy Pipfile and Pipfile.lock to /tmp, and startup.sh to / for starting up the app
COPY Pipfile /tmp
COPY Pipfile.lock /tmp
COPY startup.sh /

# Install Python deps via pipenv, using the copied Pipfile. Install into system, not into a virtualenv.
RUN PIPENV_PIPFILE=/tmp/Pipfile pipenv install --dev --system

# IF NEEDED: Install data science packages:
# RUN pip install --no-cache-dir jupyter seaborn pandas

# IF NEEDED: Install yarn and node to package frontend code, then delete files not needed anymore:
# Install third party repo for yarn and node
# RUN apt-get install -y curl gnupg apt-transport-https
# RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
# RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list
# RUN curl -sSL https://deb.nodesource.com/setup_8.x | bash -
# RUN apt-get update
# RUN apt-get install -y yarn nodejs
# RUN yarn
# RUN rm -rf node_modules /usr/local/share/.cache/yarn

# Clean up
RUN apt-get remove -y curl gnupg
RUN apt-get remove -y yarn nodejs
RUN apt-get autoremove -y
RUN rm -rf /var/lib/apt/lists/* && apt-get clean