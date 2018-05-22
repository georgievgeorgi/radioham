#!/usr/bin/gnuplot

set term pdf size 12,4

#FF=system("echo $FILE")
FF=system("ls *.swr|paste -sd ' ' ")
#FF="tmp.dat"
set o sprintf("%s.pdf",FF)
PLOT="p"
do for [f in FF] {
  PLOT=sprintf("%s '%s' u ($1/1000.):2 w l,",PLOT,f)
}
PLOT=PLOT."1 notit lt 0"


bm = 0.19
tm = 0.75
lm = 0.06
rm = 0.97
gap = 0.01
size = 0.81/12






set multiplot tit FF
set xtics nomirror
set lmargin at screen lm
#set rmargin at screen rm
set bmargin at screen bm
set tmargin at screen tm
set grid
band_i=0




set log y
set xla "Freq [MHz]"
set yrange [.8:8]
set ytics format "%4.1f"

set xtics rotate by 60 autofreq font ",8" offset 0,0 right format "%5.2f"

FRST="set border 1+4+2;unset key; set yla 'SWR'; set ytics (1,1.5,2,3,5)"
NEXT="set border 1+4; unset ytics; set ytics  offset 10000 (1,1.5,2,3,5); unset yla "
LAST="set border 1+4+8;set key"
SHIFTPLOT="set lmargin at screen lm + size*band_i + gap*band_i;band_i=band_i+1;set rmargin at screen lm + size*band_i + gap*(band_i-1)"



set xrange [ 1.800: 2.000];set tit "160m";@FRST;@SHIFTPLOT;@PLOT
set xrange [ 3.500: 3.800];set tit  "80m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [ 7.000: 7.200];set tit  "40m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [10.100:10.150];set tit  "30m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [14.000:14.350];set tit  "20m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [18.050:18.200];set tit  "17m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [21.000:21.450];set tit  "15m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [24.850:25.000];set tit  "12m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [28.000:30.000];set tit  "10m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [50.000:50.200];set tit   "6m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [144   :146   ];set tit   "2m";@NEXT;@SHIFTPLOT;@PLOT
set xrange [430   :440   ];set tit "70cm";@LAST;@SHIFTPLOT;@PLOT

unset multiplot


set o
