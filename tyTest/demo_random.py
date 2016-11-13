import random

maybe = '0123456789' \
        'abcdefghijklmnopqrstuvwxyz' \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
        '~!@#$%^&*()_+'

maybesize = len(maybe)
_D, _L, _U, _S = 1, 2, 4, 8
_FULL = _D | _L | _U | _S
_DLU_ = _D | _L | _U


def _rbit(p): return maybe[random.randint(0, maybesize - 1)]


def generate(l):
    return ''.join(map(_rbit, xrange(l)))


def chk(pwd, chklogic=_FULL):
    d, l, u, s = 0, 0, 0, 0
    for c in pwd:
        if c in 'abcdefghijklmnopqrstuvwxyz':
            l = _L
        elif c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            u = _U
        elif c in '0123456789':
            d = _D
        elif c in '~!@#$%^&*()_+':
            s = _S
    return (l | u | d | s) == chklogic


def groupGenerate(cnt, chklogic=_FULL):
    pwds = []
    while cnt:
        pwd = generate(12)
        if chk(pwd, chklogic):
            pwds.append(pwd)
            cnt -= 1
    print '\n'.join(pwds)


if __name__ == '__main__':
    groupGenerate(cnt=10)
    print '-' * 32
    groupGenerate(cnt=10, chklogic=_DLU_)
