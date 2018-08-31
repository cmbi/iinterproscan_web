FROM interproscan

# Install pip
RUN apt-get update
RUN apt-get install -y python3-pip

# Python requirements
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements /usr/src/app
RUN pip3 install --no-cache-dir -r requirements

# Python code
COPY . /usr/src/app
