#!/usr/bin/env python3
class Printable:
    def __repr__(self, indent=2):
        result = self.__class__.__name__
        in_array: bool = False
        for k, v in self.__dict__.items():
            if type(v) is list:
                in_array = True
            elif type(v) is not str or ' / ' not in v or len(v.split(' / ')) != 2:
                in_array = False
            if k.startswith('__'):
                continue
            if isinstance(v, Printable):
                v_str = v.__repr__(indent + 2)
            elif in_array:
                v_str = '['
                n_indent: int = indent + 2
                for a_v in v:
                    v_str += '\n' + ' '*n_indent
                    if isinstance(a_v, Printable):
                        v_str += a_v.__repr__(n_indent + 2)
                    else:
                        v_str += str(v)
                v_str += '\n' + ' '*indent + ']'
            else:
                v_str = str(v)
            result += '\n' + ' '*indent + k + ': ' + v_str
        return result
