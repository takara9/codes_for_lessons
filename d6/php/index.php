<html>
<head><title>PHP CONNECTION TEST</title></head>
<body>

<?php
$servername = "mysql";
$database = "mysql";

$username = getenv('MYSQL_USER');
$password = getenv('MYSQL_PASSWORD');

try {
    $dsn = "mysql:host=$servername;dbname=$database";
    $conn = new PDO($dsn, $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    print("<p>接続に成功しました。</p>");
} catch(PDOException $e) {
    print("<p>接続に失敗しました。</p>");
    echo $e->getMessage();
}

$conn = null; 
print('<p>クローズしました。</p>');

?>
</body>
</html>