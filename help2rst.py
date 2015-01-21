#!/usr/bin/env python
# -*- coding: utf-8 -*-

# script to produce rst file from program's help output.

from __future__ import unicode_literals
import sys
import re
import argparse

arg_indent = ' ' * 14

def help2man(infile):
    # We assume that first line is usage line like this:
    #
    # Usage: nghttp [OPTIONS]... URI...
    #
    # The second line is description of the command.  Multiple lines
    # are permitted.  The blank line signals the end of this section.
    # After that, we parses positional and optional arguments.
    #
    # The positional argument is enclosed with < and >:
    #
    # <PRIVATE_KEY>
    #
    # We may describe default behavior without any options by encoding
    # ( and ):
    #
    # (default mode)
    #
    # "Options:" is treated specially and produces "OPTIONS" section.
    # We allow subsection under OPTIONS.  Lines not starting with (, <
    # and Options: are treated as subsection name and produces section
    # one level down:
    #
    # TLS/SSL:
    #
    # The above is an example of subsection.
    #
    # The description of arguments must be indented by len(arg_indent)
    # characters.  The default value should be placed in separate line
    # and should be start with "Default: " after indentation.

    line = infile.readline().strip()
    m = re.match(r'^Usage: (.*)', line)
    if not m:
        print 'usage line is invalid.  Expected following lines:'
        print 'Usage: cmdname ...'
        sys.exit(1)
    synopsis = m.group(1).split(' ', 1)
    if len(synopsis) == 2:
        cmdname, args = synopsis
    else:
        cmdname, args = synopsis[0], ''

    description = []
    for line in infile:
        line = line.strip()
        if not line:
            break
        description.append(line)

    print '''
{cmdname}(1)
{cmdnameunderline}

SYNOPSIS
--------

**{cmdname}** {args}

DESCRIPTION
-----------

{description}
'''.format(cmdname=cmdname, args=args,
           cmdnameunderline='=' * (len(cmdname) + 3),
           synopsis=synopsis, description=format_text('\n'.join(description)))

    in_arg = False

    for line in infile:
        line = line.rstrip()

        if not line.strip() and in_arg:
            print ''
            continue
        if line.startswith('   ') and in_arg:
            if not line.startswith(arg_indent):
                sys.stderr.write('warning: argument description is not indented correctly.  We need {} spaces as indentation.\n'.format(len(arg_indent)))
            print '{}'.format(format_arg_text(line[len(arg_indent):]))
            continue

        if in_arg:
            print ''
            in_arg = False

        if line == 'Options:':
            print 'OPTIONS:'
            print '--------'
            print ''
            continue

        if line.startswith('  <'):
            # positional argument
            m = re.match(r'^(?:\s+)([a-zA-Z0-9-_<>]+)(.*)', line)
            argname, rest = m.group(1), m.group(2)
            print '.. describe:: {}'.format(argname)
            print ''
            print '{}'.format(format_arg_text(rest.strip()))
            in_arg = True
            continue

        if line.startswith('  ('):
            # positional argument
            m = re.match(r'^(?:\s+)(\([a-zA-Z0-9-_<> ]+\))(.*)', line)
            argname, rest = m.group(1), m.group(2)
            print '.. describe:: {}'.format(argname)
            print ''
            print '{}'.format(format_arg_text(rest.strip()))
            in_arg = True
            continue

        if line.startswith('  -'):
            # optional argument
            m = re.match(
                r'^(?:\s+)(-\S+?(?:, -\S+?)*)($| .*)',
                line)
            argname, rest = m.group(1), m.group(2)
            print '.. option:: {}'.format(argname)
            print ''
            rest = rest.strip()
            if len(rest):
                print '{}'.format(format_arg_text(rest))
            in_arg = True
            continue

        if not line.startswith(' ') and line.endswith(':'):
            # subsection
            subsec = line.strip()
            print '{}'.format(subsec)
            print '{}'.format('~' * len(subsec))
            print ''
            continue

        print line.strip()

def format_text(text):
    # escape *
    if len(text) > len(arg_indent):
        text = text[:len(arg_indent) + 1] + re.sub(r'\*', r'\*', text[len(arg_indent) + 1:])
    else:
        text = re.sub(r'\*', r'\*', text)
    # markup option reference
    text = re.sub(r'(^|\s)(-[a-zA-Z0-9-]+)', r'\1:option:`\2`', text)
    # sphinx does not like markup like ':option:`-f`='.  We need
    # backslash between ` and =.
    text = re.sub(r'(:option:`.*?`)(\S)', r'\1\\\2', text)
    # file path should be italic
    text = re.sub(r'(^|\s|\'|")(/[^\s\'"]*)', r'\1*\2*', text)
    return text

def format_arg_text(text):
    if text.strip().startswith('Default: '):
        return '\n    ' + re.sub(r'^(\s*Default: )(.*)$', r'\1``\2``', text)
    return '    {}'.format(format_text(text))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Produces rst document from help output.')
    parser.add_argument('-i', '--include', metavar='FILE',
                        help='include content of <FILE> as verbatim.  It should be ReST formatted text.')
    args = parser.parse_args()
    help2man(sys.stdin)
    if args.include:
        print ''
        with open(args.include) as f:
            sys.stdout.write(f.read())