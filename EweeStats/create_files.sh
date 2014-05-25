#!/bin/sh
#  create_dirs.sh
#  
#  Copyright 2014 Gabriel Hondet <gabrielhondet@gmail.com>
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

# Must have 2 arguments : save dir, web_root, graph name
if [ $# -ne 3 ]
then
    echo 'Arguments incorrects !'
    exit 1
fi

# Check save dir exists
if [ -d $1 ]
then
    echo 'Directory exists'
else
    mkdir $1
fi

# Removes symlink to recreate a new one
if [ -L "$2/EweeGraph.svg" ]
then
    rm "$2/EweeGraph.svg"
    rm "$2/EweeCoder.svg"
fi

# Create dumb files for symlinks
touch "$3"
touch "$1/EweeCoder.svg"
# Create link for graph
ln -s "$3" "$2/EweeGraph.svg"
# Create coder graph link
ln -s "$1/EweeCoder.svg" "$2/EweeCoder.svg"

return 0
