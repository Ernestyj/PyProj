FROM raychee/python3

RUN yum install -y gcc

######################################
#     Create Log / Data Folder       #
######################################
RUN mkdir -p /src/log

#################################
#   Project Structure Related   #
#################################
COPY environment.yml /environment.yml
RUN conda env update -n root

ENTRYPOINT ["/entrypoint.sh"]
COPY entrypoint.sh /entrypoint.sh

COPY . /src/
