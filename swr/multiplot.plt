#!/usr/bin/gnuplot

set term pdf size 12,4

#FF=system("echo $FILE")
FF=system("ls -tr *.swr|paste -sd ' ' ")
TITLE=system("basename $PWD")
#FF="tmp.dat"
set o sprintf("%s.pdf",FF)
PLOT="p"
do for [f in FF] {
  PLOT=sprintf("%s '%s' u ($1/1000.):2 w lp ps 1 lw 2 dashtype '-' tit '%s',",PLOT,f,f)
  #PLOT=sprintf("%s '%s' u ($1/1000.):2 w lp ps .5 pt 2 lw 2 tit '%s',",PLOT,f,f)
}
PLOT=PLOT."1 notit lt 0"



set multiplot tit TITLE layout 1,12 margins 0.06,.98,0.1,0.83 spacing 0.01;
set xtics nomirror
set grid
band_i=0




set log y
set xla "Freq [MHz]"
set yrange [.8:8]
set ytics format "%4.1f"

set xtics rotate by 60 font ",8" offset 0,0 right format "%5.2f"

FRST="set border 1+4+2;unset key; set yla 'SWR'; set ytics (1,1.5,2,3,5);set xtics autofreq "
NEXT="set border 1+4; set ytics  offset 10000; unset yla; set xtics autofreq; unset key "
LAST="set border 1+4+8;set key right Right; set xtics autofreq "



set xrange [ 1.800: 2.000];set tit "160m";@FRST;set xtics 0.05;@PLOT ;
set xrange [ 3.500: 3.800];set tit  "80m";@NEXT;@PLOT ;
set xrange [ 7.000: 7.200];set tit  "40m";@NEXT;@PLOT ;
set xrange [10.100:10.150];set tit  "30m";@NEXT;@PLOT ;
set xrange [14.000:14.350];set tit  "20m";@NEXT;@PLOT ;
set xrange [18.050:18.200];set tit  "17m";@NEXT;@PLOT ;
set xrange [21.000:21.450];set tit  "15m";@NEXT;@PLOT ;
set xrange [24.850:25.000];set tit  "12m";@NEXT;@PLOT ;
set xrange [28.000:30.000];set tit  "10m";@NEXT;@PLOT ;
set xrange [50.000:50.200];set tit   "6m";@NEXT;@PLOT ;
set xrange [144   :146   ];set tit   "2m";@NEXT;@PLOT ;
set xrange [430   :440   ];set tit "70cm";@LAST;@PLOT ;

unset multiplot


set o
