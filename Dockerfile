FROM pizza420/z3:4.5.0

# need ethereum + solc + pip web3
RUN apt-get update && apt-get install -y python-pip git python2.7 lsof \
    software-properties-common python-software-properties pandoc psmisc \
  && add-apt-repository ppa:ethereum/ethereum \
  && apt-get update \
  && apt-get install -y ethereum solc

# Not sure why this is broken but whatevs
#RUN rm -f /usr/bin/pip && ln -s /usr/local/bin/pip /usr/bin/pip \

# download maian
COPY . /MAIAN
WORKDIR /MAIAN
# add python as Debian alternatives source for /usr/bin/python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
#RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

RUN pip install -r requirements.txt 
# copy start script
COPY /run.sh /app/run.sh

# execute start script
CMD ["sh", "/app/run.sh"]
