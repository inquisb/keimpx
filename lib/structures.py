#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# -*- Mode: python -*-

import sys
from struct import unpack

try:
    from impacket.structure import Structure

except ImportError:
    sys.stderr.write('Impacket by SecureAuth Corporation is required for this tool to work. Please download it using:'
                     '\npip: pip install -r requirements.txt\nOr through your package manager:\npython-impacket.')
    sys.exit(255)


####################################################################
# Code borrowed and adapted from Impacket's secretsdump.py example #
####################################################################
# Taken from http://insecurety.net/?p=768
class SAM_KEY_DATA(Structure):
    structure = (
        ('Revision', '<L=0'),
        ('Length', '<L=0'),
        ('Salt', '16s=""'),
        ('Key', '16s=""'),
        ('CheckSum', '16s=""'),
        ('Reserved', '<Q=0'),
    )


class DOMAIN_ACCOUNT_F(Structure):
    structure = (
        ('Revision', '<L=0'),
        ('Unknown', '<L=0'),
        ('CreationTime', '<Q=0'),
        ('DomainModifiedCount', '<Q=0'),
        ('MaxPasswordAge', '<Q=0'),
        ('MinPasswordAge', '<Q=0'),
        ('ForceLogoff', '<Q=0'),
        ('LockoutDuration', '<Q=0'),
        ('LockoutObservationWindow', '<Q=0'),
        ('ModifiedCountAtLastPromotion', '<Q=0'),
        ('NextRid', '<L=0'),
        ('PasswordProperties', '<L=0'),
        ('MinPasswordLength', '<H=0'),
        ('PasswordHistoryLength', '<H=0'),
        ('LockoutThreshold', '<H=0'),
        ('Unknown2', '<H=0'),
        ('ServerState', '<L=0'),
        ('ServerRole', '<H=0'),
        ('UasCompatibilityRequired', '<H=0'),
        ('Unknown3', '<Q=0'),
        ('Key0', ':'),
        # Commenting this, not needed and not present on Windows 2000 SP0
        #        ('Key1',':', SAM_KEY_DATA),
        #        ('Unknown4','<L=0'),
    )


# Great help from here http://www.beginningtoseethelight.org/ntsecurity/index.htm
class USER_ACCOUNT_V(Structure):
    structure = (
        ('Unknown', '12s=b""'),
        ('NameOffset', '<L=0'),
        ('NameLength', '<L=0'),
        ('Unknown2', '<L=0'),
        ('FullNameOffset', '<L=0'),
        ('FullNameLength', '<L=0'),
        ('Unknown3', '<L=0'),
        ('CommentOffset', '<L=0'),
        ('CommentLength', '<L=0'),
        ('Unknown3', '<L=0'),
        ('UserCommentOffset', '<L=0'),
        ('UserCommentLength', '<L=0'),
        ('Unknown4', '<L=0'),
        ('Unknown5', '12s=b""'),
        ('HomeDirOffset', '<L=0'),
        ('HomeDirLength', '<L=0'),
        ('Unknown6', '<L=0'),
        ('HomeDirConnectOffset', '<L=0'),
        ('HomeDirConnectLength', '<L=0'),
        ('Unknown7', '<L=0'),
        ('ScriptPathOffset', '<L=0'),
        ('ScriptPathLength', '<L=0'),
        ('Unknown8', '<L=0'),
        ('ProfilePathOffset', '<L=0'),
        ('ProfilePathLength', '<L=0'),
        ('Unknown9', '<L=0'),
        ('WorkstationsOffset', '<L=0'),
        ('WorkstationsLength', '<L=0'),
        ('Unknown10', '<L=0'),
        ('HoursAllowedOffset', '<L=0'),
        ('HoursAllowedLength', '<L=0'),
        ('Unknown11', '<L=0'),
        ('Unknown12', '12s=b""'),
        ('LMHashOffset', '<L=0'),
        ('LMHashLength', '<L=0'),
        ('Unknown13', '<L=0'),
        ('NTHashOffset', '<L=0'),
        ('NTHashLength', '<L=0'),
        ('Unknown14', '<L=0'),
        ('Unknown15', '24s=b""'),
        ('Data', ':=b""'),
    )


class NL_RECORD(Structure):
    structure = (
        ('UserLength', '<H=0'),
        ('DomainNameLength', '<H=0'),
        ('EffectiveNameLength', '<H=0'),
        ('FullNameLength', '<H=0'),
        ('MetaData', '52s=""'),
        ('FullDomainLength', '<H=0'),
        ('Length2', '<H=0'),
        ('CH', '16s=""'),
        ('T', '16s=""'),
        ('EncryptedData', ':'),
    )


class SAMR_RPC_SID_IDENTIFIER_AUTHORITY(Structure):
    structure = (
        ('Value', '6s'),
    )


class SAMR_RPC_SID(Structure):
    structure = (
        ('Revision', '<B'),
        ('SubAuthorityCount', '<B'),
        ('IdentifierAuthority', ':', SAMR_RPC_SID_IDENTIFIER_AUTHORITY),
        ('SubLen', '_-SubAuthority', 'self["SubAuthorityCount"]*4'),
        ('SubAuthority', ':'),
    )

    def formatCanonical(self):
        ans = 'S-%d-%d' % (self['Revision'], ord(self['IdentifierAuthority']['Value'][5]))

        for i in range(self['SubAuthorityCount']):
            ans += '-%d' % (unpack('>L', self['SubAuthority'][i * 4:i * 4 + 4])[0])

        return ans


class LSA_SECRET_BLOB(Structure):
    structure = (
        ('Length', '<L=0'),
        ('Unknown', '12s=""'),
        ('_Secret', '_-Secret', 'self["Length"]'),
        ('Secret', ':'),
        ('Remaining', ':'),
    )


class LSA_SECRET(Structure):
    structure = (
        ('Version', '<L=0'),
        ('EncKeyID', '16s=""'),
        ('EncAlgorithm', '<L=0'),
        ('Flags', '<L=0'),
        ('EncryptedData', ':'),
    )


class LSA_SECRET_XP(Structure):
    structure = (
        ('Length', '<L=0'),
        ('Version', '<L=0'),
        ('_Secret', '_-Secret', 'self["Length"]'),
        ('Secret', ':'),
    )


class SAM_KEY_DATA(Structure):
    structure = (
        ('Revision', '<L=0'),
        ('Length', '<L=0'),
        ('Salt', '16s=b""'),
        ('Key', '16s=b""'),
        ('CheckSum', '16s=b""'),
        ('Reserved', '<Q=0'),
    )


class SAM_HASH(Structure):
    structure = (
        ('PekID', '<H=0'),
        ('Revision', '<H=0'),
        ('Hash', '16s=b""'),
    )


class SAM_HASH_AES(Structure):
    structure = (
        ('PekID', '<H=0'),
        ('Revision', '<H=0'),
        ('DataOffset', '<L=0'),
        ('Salt', '16s=b""'),
        ('Hash', ':'),
    )


class SAM_KEY_DATA_AES(Structure):
    structure = (
        ('Revision', '<L=0'),
        ('Length', '<L=0'),
        ('CheckSumLen', '<L=0'),
        ('DataLen', '<L=0'),
        ('Salt', '16s=b""'),
        ('Data', ':'),
    )
