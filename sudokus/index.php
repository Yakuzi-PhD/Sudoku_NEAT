<!--

This script has been provided by printable-sudoku-puzzles.com.
The link in the bottom of tha page can not be removed.

-->

<html>
<head>
<title>Free Printable 9x9 Sudoku Puzzles</title>
</head>
<body bgcolor=FFFFFF>
<center>

<h1>Free Printable 9x9 Sudoku Puzzles</h1>
<b>Difficulty:</b> <a href=index.php?1>1</a> | <a href=index.php?2>2</a>
 | <a href=index.php?3>3</a> | <a href=index.php?4>4</a> | <a href=index.php?5>5</a> | <a href=index.php?6>6</a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href=index.php?grid>Blank Grid</a>
<hr width=600>

<?php

// get difficulty level
$q=$_SERVER["QUERY_STRING"];

if ($q==1 or $q==2 or $q==3 or $q==4 or $q==5 or $q==6){
    // when  sodokus are requested we will be here
        // a small control
        if (!file_exists("dif-$q.php")){print "Error:<br>The selected difficulty level is not valid.";die();}

        // include the file with information (in $data array)
        include("dif-$q.php");

        // select sudokus
        $max=sizeof($data)-1;
        $z=mt_rand(0,$max);
        $array[0]=$data[$z];
        $z=mt_rand(0,$max);
        $array[1]=$data[$z];
        $z=mt_rand(0,$max);
        $array[2]=$data[$z];
        $z=mt_rand(0,$max);
        $array[3]=$data[$z];
        $z=mt_rand(0,$max);
        $array[4]=$data[$z];
        $z=mt_rand(0,$max);
        $array[5]=$data[$z];

        // create images
        create_sudoku_image($array,$q);
        print "<table border=0 align=center><tr><td><div align=right><font size=-1><a href=9x9_sudoku_$q.png>Show only the figure</a></font></div><img src=9x9_sudoku_$q.png width=506 height=771 alt=\"printable sudoku\"></td></tr></table>";
}
if ($q=="grid"){
    // when blank grid is requested, we will be here
        print "<table border=0 align=center><tr><td><div align=right><font size=-1><a href=9x9_sudoku_grid.png>Show only the figure</a></font></div><img src=9x9_sudoku_grid.png width=506 height=771 alt=\"printable sudoku grid\"></td></tr></table>";
}
if ($q==""){
    // if no difficulty level is requested (first visit to our page), sodukus with default difficulty level are shown
        $q=3; // default difficulty level
        print "<table border=0 align=center><tr><td><div align=right><font size=-1><a href=9x9_sudoku_$q.png>Show only the figure</a></font></div><img src=9x9_sudoku_$q.png width=506 height=771 alt=\"printable sudoku grid\"></td></tr></table>";

}



// ##################################################################################
function create_sudoku_image($array,$q){
        $mx=0;$my=0;
        $im = @imagecreatefrompng("9x9_sudoku_grid.png"); // image with grids,
        foreach ($array as $n => $code){
                $my=25;$mx=0;
                if ($n==1 or $n==3 or $n==5){$mx=280;}
                if ($n==2 or $n==3){$my=285;}
                if ($n==4 or $n==5){$my=545;}

                $a=preg_split("//"," $code",-1,PREG_SPLIT_NO_EMPTY);
                foreach($a as $k =>$v){
                        if ($v=="0"){continue;}
                        if ($k==0){continue;}
                        $x=floor(($k-1)/9);
                        $y=$k-($x*9);
                        imagestring($im, 7, 9+($y-1)*25+$mx,  5+($x)*25+$my, $v, $black);
                }
        }
        imagestring($im, 2, 5,  5, "Dif: $q", $black);
        imagepng($im,"9x9_sudoku_$q.png");
        imagedestroy($im);
}
?>
<p>Powered by <a href=http://www.printable-sudoku-puzzles.com>printable-sudoku-puzzles.com</a>
</center>
</body>
</html>
