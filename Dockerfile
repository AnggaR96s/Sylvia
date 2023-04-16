FROM gengkapak/kinetic:userbot

#
# Clone repo and prepare working directory
#
RUN git clone -b master https://github.com/AnggaR96s/Sylvia /home/gengkapak/dclxvi/
RUN mkdir /home/gengkapak/dclxvi/bin/
WORKDIR /home/gengkapak/dclxvi/

EXPOSE 80 443

CMD ["python3","-m","userbot"]
