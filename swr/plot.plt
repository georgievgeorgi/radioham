#!/bin/gnuplot

FF=system("echo $FILE")

set term pdf size 12, 3
set o sprintf("%s.pdf",FF)

set xla "Freq [MHz]"
set yla "SWR"
set xti .5
set mxtics 5
set grid xtics mxtics ytics  , dt "-."
#set title FF
set grid
#set xrange [14:14.5]

a="p 1 lt 0"
do for [f in FF] {
  a=sprintf("%s,'%s' u ($1/1000.):2 w l",a,f)
}

@a

set o

