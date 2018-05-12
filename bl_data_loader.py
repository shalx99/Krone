from urllib.request import urlopen
import os

def load_data():
    loadfile("http://www.football-data.co.uk/mmz4281/1718/D1.csv")
    loadfile("http://www.football-data.co.uk/mmz4281/1718/D2.csv")

    
def loadfile(url):
    u = urlopen(url)

    data_directory = "./data/"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    file_name = data_directory + url.split('/')[-1]

    try:
        file_size = os.path.getsize(file_name)
    except OSError:
        print ('Warning: {} data file is missing completely'.format(file_name))
        file_size = 0

    remote_file_size = int(u.getheader('Content-Length'))

    if file_size == remote_file_size:
        print('Data file {} is up to date'.format(file_name))

    else:
        f = open(file_name, 'wb')
        print("Downloading: {} Bytes: {}".format(file_name, remote_file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buff = u.read(block_sz)
            if not buff:
                break

            file_size_dl += len(buff)
            f.write(buff)

        f.close()

    return file_name
