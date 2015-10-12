###
# Copyright (c) 2015, John Marrett
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Ark')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import valve.source.a2s
import re



class Ark(callbacks.Plugin):
    """Report Ark Server Status"""
    threaded = True

    def ark(self, irc, msg, args):
        """takes no arguments

        Returns the server status
        """

        serverDetails=("server.name.or.ip",34001)

        server = valve.source.a2s.ServerQuerier(serverDetails,timeout=3)

        try:
            info = server.get_info()
            players = server.get_players()
        except Exception:
            irc.reply("Server Timeout")
            exit(1)

        info = server.get_info()
        players = server.get_players()

        serverName=info["server_name"]

        # Remove version string from server name, Ark servers return
        # the following form:
        # ARK-PvP.com [20xFarm][30xEXP][50xTame][FRESHWIPE] - (v218.7)

        m=re.search(r"(.*) - \(.*\)$",serverName)
        if m is not None:
            serverName=m.group(1)

        serverSlots="({player_count}/{max_players})".format(**info)

        connecting=0

        playerNames=[]
        for player in players["players"]:
            if player["name"]=="":
                connecting+=1
            else:
                playerNames.append(player["name"])

        if connecting==0:
            irc.reply("{} {} {}".format(serverName,serverSlots,", ".join(playerNames)))
        elif connecting==info["player_count"]:
            irc.reply("{} {} {} connecting".format(serverName,serverSlots,connecting))
        else:
            irc.reply("{} {} {} and {} connecting".format(serverName,serverSlots,", ".join(playerNames),connecting))

    ark = wrap(ark)

Class = Ark

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
