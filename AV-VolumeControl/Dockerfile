#publicly available docker image "python" on docker hub will be pulled
FROM python:3.6

ADD AVSpotifyVolume.py /

# Erweiterungen
RUN pip3 install requests
RUN pip3 install fritzconnection

# Trigger Python script
CMD ["python","-u","./AVSpotifyVolume.py"]


