# (c) 2017, Drew Bomhof <dbomhof@redhat.com>
# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash

MANAGEIQ_MODULE_VARS = ('username',
                        'password',
                        'url',
                        'token',
                        'group',
                        'X_MIQ_Group',
                        'manageiq_validate_certs',
                        'force_basic_auth',
                        'client_cert',
                        'client_key')


class ActionModule(ActionBase):

    def manageiq_extra_vars(self, module_vars, task_vars):
        if 'manageiq_connection' in task_vars.keys():
            module_vars['manageiq_connection'] = task_vars['manageiq_connection']
        if 'manageiq_validate_certs' in task_vars.keys():
            module_vars['manageiq_connection']['manageiq_validate_certs'] = task_vars.get('manageiq_validate_certs')
        if 'manageiq' not in task_vars.keys():
            return module_vars


        if 'manageiq_connection' not in module_vars.keys() or module_vars['manageiq_connection'] is None:
            module_vars['manageiq_connection'] = dict()

        for k in MANAGEIQ_MODULE_VARS:
            if k not in module_vars['manageiq_connection'].keys():
                try:
                    module_vars['manageiq_connection'][k] = task_vars['manageiq'][k]
                except KeyError:
                    pass


        return module_vars


    def run(self, tmp=None, task_vars=None):
        results = super(ActionModule, self).run(tmp, task_vars or dict())

        module_vars = self.manageiq_extra_vars(self._task.args.copy(), task_vars)

        results = merge_hash(
            results,
            self._execute_module(module_args=module_vars, task_vars=task_vars),
        )

        return results
