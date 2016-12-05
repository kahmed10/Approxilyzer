// 
// Copyright (C) 2003 Virtual Silicon Technology Inc. All Rights Reserved.
// Silicon Ready, The Heart of Great Silicon, and the Virtual Silicon
// logo are registered trademarks of Virtual Silicon Technology Inc.  All
// other trademarks are the property of their respective owner.
// 
// Virtual Silicon Technology Inc.
// 1322 Orleans Drive
// Sunnyvale, CA 94089-1116
// Phone : (408) 548-2700
// Fax   : (408) 548-2750
// Web Site : http://www.virtual-silicon.com
// 
// File Name:       HDAO211D1.v
// Library Name:    umce13h210t3
// Library Release: 1.2
// Product:         High Density Standard Cells
// Process:         UMC L130E-HS-FSG
// Generated:       07/16/2003 15:26:40
// ------------------------------------------------------------------------
//  
// $RCSfile: HDAO211D1.v,v $ 
// $Source: /syncdisk/rcs/common/verilog/5.1.4.3/sc/RCS/HDAO211D1.v,v $ 
// $Date: 2003/04/23 22:38:02 $ 
// $Revision: 1.2 $ 
//  
// ---------------------- 
// Verilog dump Timing Insertion Version 1.5

// Verilog dump veralc Version 1.9
/*****************************************************************************/
/*                                                                           */
/*  CellRater, version 5.1.4.3 production                                    */
/*  Created:  Thu Feb 20 16:21:07 2003 by sasana                             */
/*    for Verilog Simulator:  verilog-xl                                     */
/*                                                                           */
/*****************************************************************************/
`timescale 1 ns / 1 ps
`define VCC 1'b1
`define VSS 0
`celldefine
`suppress_faults
`enable_portfaults
module HDAO211D1(Z, A1, A2, B, C);
input A1;
input A2;
input B;
input C;
output Z;
 HDAO211D1_UDPZ(Z, A1, A2, B, C);
specify
// arc A1 --> Z
  ( A1 => Z ) = (1,1);
// arc A2 --> Z
  ( A2 => Z ) = (1,1);
// arc B --> Z
  ( B => Z ) = (1,1);
// arc C --> Z
  ( C => Z ) = (1,1);
endspecify
endmodule // HDAO211D1 //

primitive HDAO211D1_UDPZ(Z, A1, A2, B, C);
output Z;
input A1;
input A2;
input B;
input C;

table
// A1  A2  B  C Z
   ?    ?    1    ?   : 1   ;
   1    1    ?    ?   : 1   ;
   ?    ?    ?    1   : 1   ;
   ?    0    0    0   : 0   ;
   0    ?    0    0   : 0   ;
endtable
endprimitive
`disable_portfaults
`nosuppress_faults
`endcelldefine
