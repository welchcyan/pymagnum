import urllib2
import sys

sysCharType = sys.getfilesystemencoding()


class Crawler:

    def __init__(self):
        pass

    def get_raw_content(self, url, encoding='utf-8'):
        # type: (str, str) -> str
        _response = urllib2.urlopen(url)
        _content = _response.read().decode(encoding).encode(sysCharType)
        return _content

    def get_latest_daily(self, symbol):
        # type: (str) -> list
        _result = self.get_raw_content("http://hq.sinajs.cn/list="+symbol, encoding='gbk')
        result = _result.split('"')[1].split(',')
        result[0] = symbol
        return result

    def get_latest_dailys(self, symbols):
        # type: (list) -> list
        symbols_str = ""
        for sym in symbols:
            symbols_str += sym + ","
        _resultList = self.get_raw_content("http://hq.sinajs.cn/list="+symbols_str, encoding='gbk')
        result_list = []
        index = 0
        for line in _resultList.splitlines():
            row = line.split('"')[1].split(',')
            row[0] = symbols[index]
            index += 1
            result_list += [row]

        return result_list



