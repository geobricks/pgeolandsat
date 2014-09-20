from ftplib import FTP
from pgeo.error.custom_exceptions import PGeoException
from pgeo.error.custom_exceptions import errors
from pgeo.utils.date import day_of_the_year_to_date
from bs4 import BeautifulSoup
import urllib
from pgeolandsat.config.landsat_config import config as conf


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