from ftplib import FTP
from pgeo.error.custom_exceptions import PGeoException
from pgeo.error.custom_exceptions import errors
from pgeolandsat.config.landsat_config import config as conf
import sys
import urllib2
import urllib


def list_wrs():
    """
    List the available LANDSAT' World Reference Systems (WRS).
    @return: An array of code/label objects.
    """
    try:
        if conf['source']['type'] == 'FTP':
            ftp = FTP(conf['source']['ftp']['base_url'])
            ftp.login()
            ftp.cwd(conf['source']['ftp']['data_dir'])
            l = ftp.nlst()
            ftp.quit()
            l.sort()
            out = []
            for s in l:
                if 'WRS' in s:
                    out.append({'code': s, 'label': s})
            return out
        else:
            raise PGeoException(errors[512], status_code=512)
    except:
        raise PGeoException(errors[511], status_code=511)


def list_paths(wrs):
    """
    List the available paths for the given WRS.
    @return: An array of code/label objects.
    """
    try:
        if conf['source']['type'] == 'FTP':
            ftp = FTP(conf['source']['ftp']['base_url'])
            ftp.login()
            ftp.cwd(conf['source']['ftp']['data_dir'])
            ftp.cwd(wrs.upper())
            l = ftp.nlst()
            ftp.quit()
            l.sort()
            out = []
            for s in l:
                if '.' not in s:
                    out.append({'code': s, 'label': s})
            return out
        else:
            raise PGeoException(errors[512], status_code=512)
    except:
        raise PGeoException(errors[511], status_code=511)


def list_rows(wrs, path):
    """
    List the available rows for the given WRS and path.
    @return: An array of code/label objects.
    """
    try:
        if conf['source']['type'] == 'FTP':
            ftp = FTP(conf['source']['ftp']['base_url'])
            ftp.login()
            ftp.cwd(conf['source']['ftp']['data_dir'])
            ftp.cwd(wrs.upper())
            if not path.startswith('p'):
                path = 'p' + path
            ftp.cwd(path.lower())
            l = ftp.nlst()
            ftp.quit()
            l.sort()
            out = []
            for s in l:
                if '.' not in s:
                    out.append({'code': s, 'label': s})
            return out
        else:
            raise PGeoException(errors[512], status_code=512)
    except:
        raise PGeoException(errors[511], status_code=511)


def list_dates(wrs, path, row):
    """
    List the available dates for the given WRS, path and row.
    @return: An array of code/label objects.
    """
    try:
        if conf['source']['type'] == 'FTP':
            ftp = FTP(conf['source']['ftp']['base_url'])
            ftp.login()
            ftp.cwd(conf['source']['ftp']['data_dir'])
            ftp.cwd(wrs.upper())
            if not path.startswith('p'):
                path = 'p' + path
            if not row.startswith('r'):
                row = 'r' + row
            ftp.cwd(path.lower())
            ftp.cwd(row.lower())
            l = ftp.nlst()
            ftp.quit()
            l.sort()
            out = []
            for s in l:
                if 'EarthSat' in s:
                    lbl = s[11:15] + '-' + s[15:17] + '-' + s[17:19]
                    out.append({'code': s, 'label': lbl})
            return out
        else:
            raise PGeoException(errors[512], status_code=512)
    except:
        raise PGeoException(errors[511], status_code=511)


def list_layers(wrs, path, row, date):
    """
    List the available dates for the given WRS, path and row.
    @return: An array of code/label objects.
    """
    try:
        if conf['source']['type'] == 'FTP':
            ftp = FTP(conf['source']['ftp']['base_url'])
            ftp.login()
            ftp.cwd(conf['source']['ftp']['data_dir'])
            ftp.cwd(wrs.upper())
            if not path.startswith('p'):
                path = 'p' + path
            if not row.startswith('r'):
                row = 'r' + row
            ftp.cwd(path.lower())
            ftp.cwd(row.lower())
            ftp.cwd(date)
            l = ftp.nlst()
            ftp.quit()
            l.sort()
            out = []
            for s in l:
                if '_nn' in s:
                    file_path = 'ftp://' + conf['source']['ftp']['base_url'] + conf['source']['ftp']['data_dir']
                    file_path += wrs.upper() + '/' + path.lower() + '/' + row.lower() + '/' + date + '/'
                    file_path += s
                    out.append({
                        'file_name': s,
                        'file_path': file_path,
                        'label': s,
                        'size': None
                    })
            return out
        else:
            raise PGeoException(errors[512], status_code=512)
    except:
        raise PGeoException(errors[511], status_code=511)


def connect_to_landsat(username, password):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    params = urllib.urlencode(dict(username=username, password=password))
    f = opener.open("https://earthexplorer.usgs.gov/login/", params)
    data = f.read()
    f.close()
    if data.find('You must sign in as a registered user to download data or place orders for USGS EROS products')>0:
        print 'Authentification failed'
    else:
        print 'Logged in as ' + username + ', congrats!'
    # sys.exit(-1)
    return


def download(username, password):
    print 'logging in...'
    connect_to_landsat(username, password)
    # LC8 191035 2013 160 LGN00
    # LC8 191 035 2013 160 LGN00
    # product + scene + date_asc + station + version
    # product + (path + row) + date_asc + station + version
    product = 'LC8'
    station = 'LGN'
    url = 'http://earthexplorer.usgs.gov/download/4923/'
    url += product
    url += '1910352013160'
    url += station
    url += '00/STANDARD/EE'
    print url
    file_name = '/Volumes/Macintosh HD/Users/simona/Desktop/test.tar.gz'
    print file_name
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status
    f.close()

download('kalimaha', 'Ce09114238')