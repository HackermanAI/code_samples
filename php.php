
<?php

// Type-like definition: Config container
class DBConfig {
    const HOST = 'localhost';
    const NAME = 'your_database_name';
    const USER = 'your_username';
    const PASS = 'your_password';
    const CHARSET = 'utf8mb4';
}

// Function definition
function connectToDatabase(): PDO {
    $dsn = "mysql:host=" . DBConfig::HOST . ";dbname=" . DBConfig::NAME . ";charset=" . DBConfig::CHARSET;

    $options = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ];

    try {
        return new PDO($dsn, DBConfig::USER, DBConfig::PASS, $options);
    } catch (PDOException $e) {
        throw new PDOException($e->getMessage(), (int)$e->getCode());
    }
}

// Usage
$pdo = connectToDatabase();
?>