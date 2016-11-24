#!/usr/bin/python2
# coding: utf-8

import sys
import cgi

quack = sys.stdout.write

quack(r'''<!DOCTYPE HTML>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style>
table#logmain {
    width: 100%;
    white-space: nowrap;
}
tr td:nth-child(1),
tr td:nth-child(3) {
    text-align: right;
}
tr td:nth-child(2) {
    text-align: left;
}
tr td:nth-child(4) {
    white-space: normal;
    width: 100%;
}
tr.goo {
    color: gray;
}
tr.action td:nth-child(2)::before {
    content: '* ';
}
tr.action td:nth-child(2) {
    font-weight: bold
}
</style>
<body lang="zh-Hans-CN">
<table id="logmain" style="width: 100%" cellpadding="0" cellspacing="4">
''')

def row(klass='', td=[], useraw=[])
    return '<tr class="' + cgi.escape(klass, True) ">" + ''.join(
        '<td%s>%s</td>' % (tdfield if (i in useraw) else cgi.escape(tdfield))
        for i, tdfield in enumerate(td)) + '</tr>'

line = sys.stdin.readline()
while line:
    try:
        line=line.rstrip("\n").rstrip("\r")
        time=line[:23]
        sraw=line[25:]
        if sraw.startswith(":: "):
            # what's this?
            quack(row('goo', [time, '', '', sraw[3:]]))
        else:
            raw=sraw.split(None, 3)
            if raw[0]=='PING':
                pass
            
            if raw[1]=="PRIVMSG":
                dest=raw[2]
                if not dest.startswith("#"):
                    pass
                nick=raw[0].split("!", 1)[0][1:]
                msg=raw[3][1:]
                if msg.startswith("\001ACTION "):
                    msg=msg.strip("\001").lstrip("ACTION ")
                    klass='action privmsg'
                else:
                    klass='privmsg'
                quack(row(klass, [time, dest, nick, msg]))
            elif raw[1]=="JOIN":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                dest=raw[2]
                quack(row('join', [time, dest, nick, '<b>[<i>%s</i>]</b> 加入 %s' % (cgi.escape(ident), cgi.escape(dest))], [3]))
            elif raw[1]=="PART":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                dest=raw[2]
                if len(raw)>=4:
                    desc=" <b>(%s)</b>" % cgi.escape(raw[3].lstrip(":").strip())
                else:
                    desc=""
                quack("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\"><b>%s</b></td><td style=\"width: 100%%\"><b>[<i>%s</i>]</b> 离开 %s%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(ident), cgi.escape(dest), desc))
            elif raw[1]=="QUIT":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                if len(raw)>=2:
                    desc=" <b>(%s)</b>" % cgi.escape(sraw.split(None, 2)[2].lstrip(":").strip())
                else:
                    desc=""
                quack("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\"></td><td style=\"text-align: right\"><b>%s</b></td><td style=\"width: 100%%\"><b>[<i>%s</i>]</b> 退出%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(nick), cgi.escape(ident), desc))
            elif raw[1]=="NICK":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                newnick=sraw.split(None, 2)[2][1:]
                quack("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\"></td><td style=\"text-align: right\"><b>%s</b></td><td style=\"width: 100%%\"><b>[<i>%s</i>]</b> 更改昵称为 <b>%s</b></td></tr>\r\n" % (cgi.escape(time), cgi.escape(nick), cgi.escape(ident), cgi.escape(newnick)))
            elif raw[1]=="MODE":
                nick=raw[0].split("!", 1)[0][1:]
                dest=raw[2]
                newmode=raw[3].lstrip(":").strip()
                quack("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\"><b>%s</b></td><td style=\"width: 100%%\">设定模式 <b>(%s)</b></td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(newmode)))
            elif raw[1]=="TOPIC":
                nick=raw[0].split("!", 1)[0][1:]
                dest=raw[2]
                newtopic=raw[3].lstrip(":").strip()
                quack("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\"><b>%s</b></td><td style=\"width: 100%%; white-space: normal\">设定话题: <b>%s</b></td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(newtopic)))
    except Exception as e:
        quack("<tr><td colspan=\"4\" style=\"color: red\">解析出错: %s</td></tr>\r\n" % cgi.escape(str(e)))
    line=sys.stdin.readline()
quack("</table>\r\n</body>\r\n</html>\r\n")

# vim: et ft=python sts=4 sw=4 ts=4
