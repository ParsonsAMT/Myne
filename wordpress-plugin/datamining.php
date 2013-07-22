<?php
/*
Plugin Name: Datamining Profile Inserter
Plugin URI: http://mining.parsons.edu
Description: 
Version: 0.1
Author: rory solomon (solomonr@newschool.edu)
Author URI: http://mining.parsons.edu
*/

/*
	Copyright 2009 Parsons, the New School for Design

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	
	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>
*/

function datamining_profiles($content) {
	// Search for matches
  /*
	$patterns = array (
		'/<!--ducktime-->/e',
		'/<!--ducktime\+(\d+)-->/e',
		'/<!--ducktime-(\d+)-->/e'
	);
	$replace = array (
		"time()",
		"time()+\\1",
		"time()-\\1"
	);
	return preg_replace($patterns, $replace, $content);
  */

  $pattern = '/<!-- ?datamining-profiles ([0-9 ]+) ?-->/e';

  $n = preg_match_all($pattern,$content,$matches);

  if ( !$n || $n == 0 ) {
    return $content;
  }

  $ids = explode(' ',trim($matches[1][0]));

  $bios = '';
  foreach ($ids as $n=>$id) {

    // create a new cURL resource
    $ch = curl_init();

    // set URL and other appropriate options
    curl_setopt($ch, CURLOPT_URL, "http://stage.mining.parsons.edu/django/api/wordpress/".$id);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    // grab URL and pass it to the browser
    $b = curl_exec($ch);
    $bios .= $b;

    // close cURL resource, and free up system resources
    curl_close($ch);
  }

  return $bios;
}

add_filter('the_content', 'datamining_profiles');
