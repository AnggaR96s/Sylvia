FROM gengkapak/hirsute:userbot

#
# Clone repo and prepare working directory
#
RUN git clone -b master https://gitlab.com/anggars/DCLXVI /home/gengkapak/dclxvi/
RUN mkdir /home/gengkapak/dclxvi/bin/
WORKDIR /home/gengkapak/dclxvi/
RUN pip3 install google_trans_new

EXPOSE 80 443

CMD ["python3","-m","userbot"]
