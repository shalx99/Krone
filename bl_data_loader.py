from urllib.request import urlopen
import os
import csv


def load_data(load_all=False):

    if load_all:
        years = list(range(93, 100)) + list(range(0, 19))
    else:
        years = [17, 18]

    prev_year = ''
    for year in years:
        if not prev_year:
            prev_year = year
            continue
        url_b1 = 'http://www.football-data.co.uk/mmz4281/{0:02d}{1:02d}/D1.csv'.format(prev_year, year)
        loadfile(url_b1)

        url_b2 = 'http://www.football-data.co.uk/mmz4281/{0:02d}{1:02d}/D2.csv'.format(prev_year, year)
        loadfile(url_b2)
        prev_year = year


def loadfile(url, verbose=False):
    u = urlopen(url)

    season = url.split('/')[-2]
    data_directory = "./data/" + season + '/'
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
        if verbose:
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


def csv_to_list(file_path):

    season_data = list()
    with open(file_path, encoding='iso-8859-15') as f:
        reader = csv.DictReader(f)

        for line in reader:
            season_data.append(line)

    return season_data


def data_files(verbose=False):
    years = list(range(93, 100)) + list(range(0, 19))
    files = list()
    prev_year = 0
    for year in years:
        if not prev_year:
            prev_year = year
            continue
        files.append('./data/{0:02d}{1:02d}/D1.csv'.format(prev_year, year))
        files.append('./data/{0:02d}{1:02d}/D2.csv'.format(prev_year, year))
        prev_year = year

    if verbose:
        print('Files to scan: {0}'.format(len(files)))

    return files
