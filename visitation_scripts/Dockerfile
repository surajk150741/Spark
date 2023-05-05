FROM iad.ocir.io/bmmp5bv7olp2/spark-3.3_datamech_lib:latest

RUN mkdir apps

#RUN copy python_nb_converted apps

COPY python_nb_converted/ apps/python_nb_converted/
RUN apt-get install cloud-guest-utils -y
RUN apt install fdisk -y
RUN echo df -Th
#RUN growpart /dev/sda 3
#RUN xfs_growfs /dev/sda3
RUN echo "hello world"