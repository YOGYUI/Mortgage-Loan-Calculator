import os
import _io
import xml.etree.ElementTree as ElementTree


def ensurePathExist(path: str):
    targetpath = os.path.abspath(path)
    if not os.path.isdir(targetpath):
        if os.name == 'nt':
            pathsplit = targetpath.split('\\')
            ptemp = str(pathsplit[0]) + '\\'
        else:
            pathsplit = targetpath.split('/')
            ptemp = str(pathsplit[0]) + '/'
        for i in range(len(pathsplit) - 1):
            p = pathsplit[i + 1]
            ptemp = os.path.join(ptemp, p)
            ptemp = os.path.abspath(ptemp)
            if not os.path.isdir(ptemp):
                os.mkdir(ptemp)


def writeXmlFile(elem: ElementTree.Element, path: str = '', fp: _io.TextIOWrapper = None, level: int = 0):
    if fp is None:
        _fp = open(path, 'w', encoding='utf-8')
        _fp.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n')
    else:
        _fp = fp
    _fp.write('\t' * level)
    _fp.write('<' + elem.tag)
    for key in elem.keys():
        fp.write(' ' + key + '="' + elem.attrib[key] + '"')
    if len(list(elem)) > 0:
        _fp.write('>\n')
        for child in list(elem):
            writeXmlFile(child, fp=_fp, level=level+1)
        _fp.write('\t' * level)
        _fp.write('</' + elem.tag + '>\n')
    else:
        if elem.text is not None:
            txt = elem.text
            txt = txt.replace('\r', '')
            txt = txt.replace('\n', '')
            txt = txt.replace('\t', '')
            if len(txt) > 0:
                _fp.write('>' + txt + '</' + elem.tag + '>\n')
            else:
                _fp.write('/>\n')
        else:
            _fp.write('/>\n')
    if level == 0:
        _fp.close()


def money_string_to_readable_text(value: int):
    v = value
    result = ''

    m = v // 10 ** 12
    if m > 0:
        result += '{:,}조 '.format(m)

    v -= m * 10 ** 12
    m = v // 10 ** 8
    if m > 0:
        result += '{:,}억 '.format(m)

    v -= m * 10 ** 8
    m = v // 10 ** 4
    if m > 0:
        result += '{:,}만 '.format(m)

    v -= m * 10 ** 4
    if v > 0:
        result += '{:,}'.format(v)

    return result.strip()
