
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
#include "Registry.h"
#include <stdio.h>

Registry *Registry::instance = NULL;

Registry::Registry(void) 
{
  numManagers = 0;
  for (int i = 0; i < MAX_CONTROLLERS; i++) {
    m_reg_table[i] = NULL;
  }
}

Registry::~Registry(void)
{
}

void Registry::addController( CacheController *manager )
{
    int id = numManagers;
    numManagers++;
    // check that this id hasn't been already added
    if ( m_reg_table[id] != NULL ) {
        printf("Warning: replacing %d in the registry with new entry\n", id);
    }
    // add the manager to the list
    m_reg_table[id] = manager;
}

void Registry::removeAllControllers( void )
{
    for (int iter = 0; iter  < numManagers; iter++) {
        delete m_reg_table[iter];
    }
}
void Registry::cacheAccess(memory_transaction_t *mem_trans, Address pc )
{
    for (int iter = 0; iter  < numManagers; iter++) {
       m_reg_table[iter]->cacheAccess( mem_trans, pc );
    }
}

void Registry::clearStats(void)
{
    for (int iter = 0; iter  < numManagers; iter++) {
       m_reg_table[iter]->clearRecentStats();
       m_reg_table[iter]->clearTotalStats();
    }
}

