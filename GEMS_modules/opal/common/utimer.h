
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
#ifndef _UTIMER_H_
#define _UTIMER_H_

/*------------------------------------------------------------------------*/
/* Includes                                                               */
/*------------------------------------------------------------------------*/

/*------------------------------------------------------------------------*/
/* Macro declarations                                                     */
/*------------------------------------------------------------------------*/

/*------------------------------------------------------------------------*/
/* Class declaration(s)                                                   */
/*------------------------------------------------------------------------*/

/**
* User-level timer for wall-clock timing. Currently uses 'gettimeoday()'
* so it only reflects a lower resolution wall clock time.
*
* @author  cmauer
* @version $Id: utimer.h 1.4 06/02/13 18:49:12-06:00 mikem@maya.cs.wisc.edu $
*/
class utimer_t {

public:
  /**
   * @name Constructor(s) / destructor
   */
  //@{

  /**
   * Constructor: creates object
   */
  utimer_t();

  /**
   * Destructor: frees object.
   */
  ~utimer_t();
  //@}

  /**
   * @name Methods
   */
  //@{

  /// starts timing an event
  void   startTimer( void );

  /// stops timing an event
  void   stopTimer( void );

  /// returns the elapsed time
  void   getElapsedTime( int64 *sec_elapsed, int64 *usec_elapsed );

  /// accumulates the most recent 'stopped' time to a cumulative total
  void   accumulateTime( void );

  /// returns the cumulative total of times
  void   getCumulativeTime( int64 *sec_cumulative, int64 *usec_cumulative );
  //@}

private:
  /// start time
  struct timeval   m_timer_start;
  /// stop time
  struct timeval   m_timer_stop;

  /// cumulative time (in seconds)
  int64    m_cumulative_secs;
  /// cumulative time (in micro-seconds)
  int64    m_cumulative_usecs;
};

/*------------------------------------------------------------------------*/
/* Global variables                                                       */
/*------------------------------------------------------------------------*/

/*------------------------------------------------------------------------*/
/* Global functions                                                       */
/*------------------------------------------------------------------------*/

#endif  /* _UTIMER_H_ */
