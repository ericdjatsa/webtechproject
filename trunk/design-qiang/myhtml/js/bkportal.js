
var _sUserAgent = navigator.userAgent;
var _isOpera = _sUserAgent.indexOf('Opera') > -1;
var _isIE = _sUserAgent.indexOf('compatible') > -1
        && _sUserAgent.indexOf('MSIE') > -1
        && !_isOpera;

var Cookie = new function() {
    var _cookieStr = null;
    var _cookieObj = {};
    var _cached = false;

    function _loadCoki() {
        _cached = true;
        _cookieStr = document.cookie;
        var cookies = _cookieStr.split(';');
        var cookie,name,value;
        for(var i = 0,ilen = cookies.length; i < ilen; i++) {
            cookie = cookies[i].replace(/^\s+|\s+$/ig, '');
            name = cookie.substr(0, cookie.indexOf('='));
            value = cookie.substr(name.length + 1);
            _cookieObj[name] = decodeURIComponent(value);
        }
    }

    this.get = function(name) {
        if(_cached) {//已经缓存
            if(name in _cookieObj) {
                return _cookieObj[name];
            }
            return null;
        }
        try {//避免发生死循环
            _loadCoki();
        }
        catch(e) {
            _cached = true;
        }
        return this.get(name);
    };

    this.reload = function(name) {
        _cached = false;
        _cookieObj = {};
        return this.get(name);
    };

    this.set = function(name, value, userOptions) {
        var options = {
            expires : 60 * 60 * 24,
            path : '/',
            domain : 'pplive.com',
            secure : ''
        };
        for(var p in userOptions) {
            options[p] = userOptions[p];
        }
        var date;
        if(typeof options.expires == 'number') {
            date = new Date();
            date.setTime(date.getTime() + options.expires * 1000);
        }
        else {
            date = options.expires;
        }
        var expires = '; expires=' + date.toUTCString();
        var path = '; path=' + options.path;
        var domain = '; domain=' + options.domain;
        var secure = options.secure ? '; secure' : '';
        document.cookie = [name,'=',encodeURIComponent(value),
            expires,path,domain,secure].join('');
        _cookieObj[name] = encodeURIComponent(value);
    };

    this.del = function(name, userOptions) {
        var options = userOptions || {};
        options.expires = -1;
        this.set(name, '', options);
    };

    this.clear = function() {
        for(var p in _cookieObj) {
            try {
                this.del(p);
            }
            catch(e) {
                continue;
            }
        }
        _cookieObj = {};
    };
};


function urlencode(_url) {
    _url = _url.replace(/(:)/g, "%3A")
            .replace(/(\/)/g, "%2F")
            .replace(/(\?)/g, "%3F")
            .replace(/(\=)/g, "%3D")
            .replace(/(\&)/g, "%26");
    return _url;
}


//判断字符串是否为空
function isblank(str) {
    return strtrim(str) == '';
}

function strtrim(str) {
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

function getRandomNum() {
    return new Date().getTime() + Math.random() * 1000000000 + "" + Math.random() * 1000000000;
}

function utf16to8(str) {
    var out, i, len, c;

    out = "";
    len = str.length;
    for(i = 0; i < len; i++) {
        c = str.charCodeAt(i);
        if((c >= 0x0001) && (c <= 0x007F)) {
            out += str.charAt(i);
        } else if(c > 0x07FF) {
            out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
            out += String.fromCharCode(0x80 | ((c >> 6) & 0x3F));
            out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
        } else {
            out += String.fromCharCode(0xC0 | ((c >> 6) & 0x1F));
            out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
        }
    }
    return out;
}

function utf8to16(str) {
    var out, i, len, c;
    var char2, char3;

    out = "";
    len = str.length;
    i = 0;
    while(i < len) {
        c = str.charCodeAt(i++);
        switch(c >> 4)
                {
            case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
        // 0xxxxxxx
            out += str.charAt(i - 1);
            break;
            case 12: case 13:
        // 110x xxxx   10xx xxxx
            char2 = str.charCodeAt(i++);
            out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
            break;
            case 14:
            // 1110 xxxx  10xx xxxx  10xx xxxx
                char2 = str.charCodeAt(i++);
                char3 = str.charCodeAt(i++);
                out += String.fromCharCode(((c & 0x0F) << 12) |
                                           ((char2 & 0x3F) << 6) |
                                           ((char3 & 0x3F) << 0));
                break;
        }
    }

    return out;
}

var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var base64DecodeChars = new Array(
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
        52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
        -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
        -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);
//客户端Base64编码
function base64encode(str) {
    var out, i, len;
    var c1, c2, c3;

    len = str.length;
    i = 0;
    out = "";
    while(i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if(i == len)
        {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt((c1 & 0x3) << 4);
            out += "==";
            break;
        }
        c2 = str.charCodeAt(i++);
        if(i == len)
        {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt((c2 & 0xF) << 2);
            out += "=";
            break;
        }
        c3 = str.charCodeAt(i++);
        out += base64EncodeChars.charAt(c1 >> 2);
        out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
        out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
        out += base64EncodeChars.charAt(c3 & 0x3F);
    }
    return out;
}
    //客户端Base64解码
function base64decode(str) {
    var c1, c2, c3, c4;
    var i, len, out;

    len = str.length;
    i = 0;
    out = "";
    while(i < len) {
        /* c1 */
        do {
            c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
        } while(i < len && c1 == -1);
        if(c1 == -1)
            break;

        /* c2 */
        do {
            c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
        } while(i < len && c2 == -1);
        if(c2 == -1)
            break;

        out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));

        /* c3 */
        do {
            c3 = str.charCodeAt(i++) & 0xff;
            if(c3 == 61)
                return out;
            c3 = base64DecodeChars[c3];
        } while(i < len && c3 == -1);
        if(c3 == -1)
            break;

        out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));

        /* c4 */
        do {
            c4 = str.charCodeAt(i++) & 0xff;
            if(c4 == 61)
                return out;
            c4 = base64DecodeChars[c4];
        } while(i < len && c4 == -1);
        if(c4 == -1)
            break;
        out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
    }
    return out;
}


