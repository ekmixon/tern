# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

"""
Helper functions for packages in SPDX document
"""

from tern.formats.spdx.spdxtagvalue import formats as spdx_formats
from tern.formats.spdx import spdx_common
from tern.report import content


def get_package_comment(package_obj):
    '''Return a PackageComment tag-value text block for a list of
    NoticeOrigin objects'''
    comment = ''
    if package_obj.origins.origins:
        for notice_origin in package_obj.origins.origins:
            comment = comment + content.print_notices(
                notice_origin, '', '\t')
        return spdx_formats.package_comment.format(comment=comment)
    return comment


def get_package_block(package_obj, template):
    '''Given a package object and its SPDX template mapping, return a SPDX
    document block for the package. The mapping should have keys:
        PackageName
        PackageVersion
        PackageLicenseDeclared
        PackageCopyrightText
        PackageDownloadLocation'''
    block = ''
    mapping = package_obj.to_dict(template)
    # Package Name
    block += f"PackageName: {mapping['PackageName']}\n"
    # SPDXID
    block += f'SPDXID: {spdx_common.get_package_spdxref(package_obj)}\n'
    # Package Version
    if mapping['PackageVersion']:
        block += f"PackageVersion: {mapping['PackageVersion']}\n"
    # Package Download Location
    if mapping['PackageDownloadLocation']:
        block += f"PackageDownloadLoaction: {mapping['PackageDownloadLocation']}\n"
    else:
        block += 'PackageDownloadLocation: NOASSERTION\n'
    # Files Analyzed (always false for packages)
    block += 'FilesAnalyzed: false\n'
    # Package License Concluded (always NOASSERTION)
    block += 'PackageLicenseConcluded: NOASSERTION\n'
    # Package License Declared (use the license ref for this)
    if mapping['PackageLicenseDeclared']:
        block += f"PackageLicenseDeclared: {spdx_common.get_license_ref(mapping['PackageLicenseDeclared'])}\n"

    else:
        block += 'PackageLicenseDeclared: NONE\n'
    # Package Copyright Text
    if mapping['PackageCopyrightText']:
        block += 'PackageCopyrightText:' + spdx_formats.block_text.format(
            message=mapping['PackageCopyrightText']) + '\n'
    else:
        block += 'PackageCopyrightText: NONE\n'
    # Package Comments
    block += get_package_comment(package_obj)
    return block
