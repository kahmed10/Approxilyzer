
/*
    Copyright (C) 1999-2005 by Mark D. Hill and David A. Wood for the
    Wisconsin Multifacet Project.  Contact: gems@cs.wisc.edu
    http://www.cs.wisc.edu/gems/

    --------------------------------------------------------------------

    This file is part of the Opal Timing-First Microarchitectural
    Simulator, a component of the Multifacet GEMS (General 
    Execution-driven Multiprocessor Simulator) software toolset 
    originally developed at the University of Wisconsin-Madison.

    Opal was originally developed by Carl Mauer based upon code by
    Craig Zilles.

    Substantial further development of Multifacet GEMS at the
    University of Wisconsin was performed by Alaa Alameldeen, Brad
    Beckmann, Jayaram Bobba, Ross Dickson, Dan Gibson, Pacia Harper,
    Milo Martin, Michael Marty, Carl Mauer, Michelle Moravan,
    Kevin Moore, Manoj Plakal, Daniel Sorin, Min Xu, and Luke Yen.

    --------------------------------------------------------------------

    If your use of this software contributes to a published paper, we
    request that you (1) cite our summary paper that appears on our
    website (http://www.cs.wisc.edu/gems/) and (2) e-mail a citation
    for your published paper to gems@cs.wisc.edu.

    If you redistribute derivatives of this software, we request that
    you notify us and either (1) ask people to register with us at our
    website (http://www.cs.wisc.edu/gems/) or (2) collect registration
    information and periodically send it to us.

    --------------------------------------------------------------------

    Multifacet GEMS is free software; you can redistribute it and/or
    modify it under the terms of version 2 of the GNU General Public
    License as published by the Free Software Foundation.

    Multifacet GEMS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with the Multifacet GEMS; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
    02111-1307, USA

    The GNU General Public License is contained in the file LICENSE.

### END HEADER ###
*/
/*****************************************************************************
 * Microbenchmark to test the number of instructions in copying a
 * block from somewhere to somewhere else
 *
 * A command line parameter gives the number of times to run the benchmark.
 *
 ****************************************************************************/

/* -- define magic call for breakpoint */

#define RUBY_MAGIC_CALL( service )                              \
  do                                                            \
  {                                                             \
    asm volatile (                                              \
                   "sethi %0, %%g0"                             \
                   : /* -- no outputs */                        \
                   : "g" ( (((service) & 0xff) << 16) | 0 )     \
                 );                                             \
  } while( 0 );
               
#include "stdio.h"
#include "stdlib.h"

int main(int argc, char* argv[])
{

  if ( argc != 2 ) {
    printf("usage: %s number-of-trials\n", argv[0]);
    exit(1);
  }

  int   bufferSize = 1 * 1048576;
  char *readBuffer  = (char *)malloc(sizeof(char)*bufferSize);
  char *writeBuffer = (char *)malloc(sizeof(char)*bufferSize);
  char *readptr;
  char *endptr;
  char *writeptr;
  int   numTrials = atoi( argv[1] );

  readptr = readBuffer;
  for (int i = 0; i < bufferSize; i++) {
    *readptr++ = i % 255;
  }

  /* -- 4 == Do_Breakpoint */
  RUBY_MAGIC_CALL( 4 );    
  for (int i = 0; i < numTrials; i++) {
    memcpy( writeBuffer, readBuffer, bufferSize );
  }
  /* -- 4 == Do_Breakpoint */
  RUBY_MAGIC_CALL( 4 );               

  long total;
  for (int i = 0; i < bufferSize; i++) {
    total += writeBuffer[i];
  }
  printf("Total = %ld\n", total);

  free( readBuffer );
  free( writeBuffer );
  return 0;
}
