<?php
  $x = 0.0001;
  for ($i = 0; $i <= 200000; $i++) {
    $x += sqrt($x);
  }
  echo "Hostname: ".gethostname()."\n";
?>

