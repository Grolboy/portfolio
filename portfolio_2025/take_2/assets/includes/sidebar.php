<!-- Sidebar for the portfolio dashboard -->
<?php include 'need.php'; ?>
<nav id="sidebar">
    <ul>
        <li>
            <span class="logo">Lucas</span>
            <button id="toggle-btn">
                <i class="bi bi-list"></i>
            </button>
        </li>
        <li class="active">
            <a href="dash_back.php"><i class="bi bi-house"></i> Home</a>
        </li>
        <li>
            <button class="dropdown-btn">
                <i class="bi bi-briefcase"></i> Portfolio
                <i class="bi bi-chevron-down"></i>    
            </button>
            <ul class="sub-menu">
                <li><a href="portfolio.php">Portfolio</a></li>
                <li><a href="portfolio_add.php">Add Portfolio</a></li>
                <li><a href="portfolio_edit.php">Edit Portfolio</a></li>
                <li><a href="portfolio_delete.php">Delete Portfolio</a></li>
            </ul>
        </li>
        <li>
            <button class="dropdown-btn">
                <i class="bi bi-person"></i> Resume
                <i class="bi bi-chevron-down"></i>
            </button>
            <ul class="sub-menu">
                <li><a href="profile.php">Add new Resume</a></li>
                <li><a href="profile_edit.php">Edit Resume</a></li>
                <li><a href="profile_delete.php">Delete Resume</a></li>
            </ul>
        </li>
    </ul>
</nav>

<!--    <div class="sidebar-footer">
<?php include 'footer.php'; ?>
    </div> -->
