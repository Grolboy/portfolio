<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php echo $title ?? 'Portfolio'; ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;600&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <link rel="stylesheet" href="../assets/css/styles.css">
    <link rel="stylesheet" href="../assets/css/sidebar.css">
</head>
<body>
    <header>
        <?php include 'sidebar.php'; ?>
    </header>

    <div class="main-content">
        <?php echo $content ?? ''; ?>
    </div>

    <!-- <footer>
        <?php include 'footer.php'; ?>
    </footer> -->

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <?php if (isset($custom_js)): ?>
        <script src="<?php echo $custom_js; ?>"></script>
    <?php endif; ?>
</body>
</html>