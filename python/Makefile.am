# nghttp2 - HTTP/2 C Library

# Copyright (c) 2013 Tatsuhiro Tsujikawa

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This will avoid that setup.py gets deleted before it is executed in
# clean-local in parallel build.
.NOTPARALLEL:

EXTRA_DIST = cnghttp2.pxd nghttp2.pyx

if ENABLE_PYTHON_BINDINGS

all-local: nghttp2.c
	$(PYTHON) setup.py build

install-exec-local:
	$(PYTHON) setup.py install --prefix=$(DESTDIR)$(prefix)

# uninstall-local:
# 	rm -rf $(DESTDIR)$(libdir)/python*/site-packages/*nghttp2*

clean-local:
	$(PYTHON) setup.py clean --all
	-rm -f $(builddir)/nghttp2.c

.pyx.c:
	$(CYTHON) -o $@ $<

endif # ENABLE_PYTHON_BINDINGS
