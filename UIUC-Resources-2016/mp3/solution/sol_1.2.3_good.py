#!/usr/bin/python
# -*- coding: utf-8 -*-
blob = """
           l��U������1�$H��{�Z�1^�rf�,���^�`���C:�1��Y��Px= ����76M`K���$[���15�G�0�K
l�K���g~�}�z�6.r�����XI�������d+
"""

from hashlib import sha256
a = sha256(blob).hexdigest()
if a == '5cde7159314ea40617631b9d2511bfca72acda2f6808691c280b86f11649d514':
	print 'I come in peace.'
else:
	print 'Prepare to be destroyed!'
