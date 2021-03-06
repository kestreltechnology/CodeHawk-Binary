# ------------------------------------------------------------------------------
# Access to the CodeHawk Binary Analyzer Analysis Results
# Author: Henny Sipma
# ------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 Kestrel Technology LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------

import chb.asm.X86OpcodeBase as X
import chb.simulate.SimulationState as S
import chb.simulate.SimUtil as SU
import chb.simulate.SimValue as SV

class X86Movzx(X.X86OpcodeBase):

    # tags: [ 'movzx' ]
    # args: [ size, dst-op, src-op ]
    def __init__(self,x86d,index,tags,args):
        X.X86OpcodeBase.__init__(self,x86d,index,tags,args)

    def get_size(self): return int(self.args[0])

    def get_src_operand(self): return self.x86d.get_operand(self.args[2])

    def get_dst_operand(self): return self.x86d.get_operand(self.args[1])

    def get_operands(self):
        return [ self.get_dst_operand(), self.get_src_operand() ]

    # xdata: [ "a:vxx" ],[ lhs, rhs, rhs-rewrittenn ]
    def get_annotation(self,xdata):
        (xtags,xargs,xprs) = xdata.get_xprdata()
        if len(xprs) == 3:
            lhs = str(xprs[0])
            rhs = str(xprs[1])
            rrhs = str(xprs[2])
            rhs = X.simplify_result(xargs[1],xargs[2],rhs,rrhs)
            return lhs + ' = ' + rhs
        else:
            return 'movzx:????'

    def get_lhs(self,xdata):
        (xtags,xargs,xprs) = xdata.get_xprdata()
        if len(xprs) == 3:
            return [ xprs[0] ]
        else:
            return []

    def get_rhs(self,xdata):
        (xtags,xargs,xprs) = xdata.get_xprdata()
        if len(xprs) == 3:
            return [ xprs[2] ]
        else:
            return []

    # --------------------------------------------------------------------------
    # Copies the contents of the source operand (register or memory location) to
    # the desti- nation operand (register) and zero extends the value.
    #
    # Flags affected: None
    # --------------------------------------------------------------------------
    def simulate(self,iaddr,simstate):
        dstop = self.get_dst_operand()
        srcval = simstate.get_rhs(iaddr,self.get_src_operand())
        srcval = srcval.zero_extend(dstop.get_size())
        simstate.set(iaddr,dstop,srcval)

