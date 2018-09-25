<?php
session_start();
if (!isset($_SESSION['count'])) {
    $_SESSION['count'] = 1;
} else {
    $_SESSION['count']++;
}
echo "Hostname: ".gethostname()."<br>\n";
echo $_SESSION['count']."th time access.\n";
?>
