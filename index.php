<?php
// Retrieve MSISDN from common header variations
$msisdn = null;

// Standard Apache/Nginx CGI header mappings
$header_keys = [
    'HTTP_X_MSISDN', 
    'HTTP_X_Msisdn', 
    'HTTP_MSISDN',
    'HTTP_X_UP_CALLING_LINE_ID'
];

foreach ($header_keys as $key) {
    if (isset($_SERVER[$key]) && !empty($_SERVER[$key])) {
        $msisdn = $_SERVER[$key];
        break;
    }
}

// Check via getallheaders() for direct case-insensitive matching
if (!$msisdn && function_exists('getallheaders')) {
    $all_headers = getallheaders();
    $request_keys = ['X-MSISDN', 'x-msisdn', 'MSISDN', 'msisdn', 'X-Msisdn'];
    foreach ($request_keys as $key) {
        if (isset($all_headers[$key]) && !empty($all_headers[$key])) {
            $msisdn = $all_headers[$key];
            break;
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BIMA Health | Please Wait</title>
    
    <!-- Premium Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-base: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --border-color: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-primary: #e11d48;
            --accent-secondary: #f59e0b;
            --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-sans);
            background-color: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
            padding: 20px;
        }

        /* Animated Glowing Orbs */
        .glow-orb {
            position: absolute;
            width: 350px;
            height: 350px;
            border-radius: 50%;
            filter: blur(100px);
            z-index: 0;
            opacity: 0.25;
            pointer-events: none;
            animation: orbPulse 8s infinite alternate ease-in-out;
        }

        .orb-1 {
            background: #e11d48;
            top: -50px;
            left: -50px;
        }

        .orb-2 {
            background: #3b82f6;
            bottom: -50px;
            right: -50px;
            animation-delay: -4s;
        }

        @keyframes orbPulse {
            0% { transform: scale(1) translate(0, 0); }
            100% { transform: scale(1.15) translate(30px, 20px); }
        }

        /* Loader Card */
        .loader-card {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 420px;
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 48px 32px;
            text-align: center;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: cardFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes cardFadeIn {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Logo Styling */
        .logo-wrapper {
            margin-bottom: 32px;
            display: inline-block;
            background: #ffffff;
            padding: 14px 24px;
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }

        .logo-img {
            max-height: 60px;
            max-width: 220px;
            width: auto;
            height: auto;
            display: block;
            object-fit: contain;
        }

        /* Spinner */
        .spinner-container {
            position: relative;
            width: 56px;
            height: 56px;
            margin: 0 auto 28px;
        }

        .spinner-ring {
            position: absolute;
            inset: 0;
            border-radius: 50%;
            border: 3.5px solid transparent;
            border-top-color: var(--accent-primary);
            animation: spin 1s linear infinite;
        }

        .spinner-ring-inner {
            position: absolute;
            inset: 8px;
            border-radius: 50%;
            border: 3.5px solid transparent;
            border-top-color: var(--accent-secondary);
            animation: spinReverse 0.75s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @keyframes spinReverse {
            to { transform: rotate(-360deg); }
        }

        /* Text Content */
        .loader-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
            letter-spacing: -0.3px;
        }

        .loader-subtitle {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.5;
        }

        /* Subtle Progress Bar */
        .progress-bar-track {
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 2px;
            margin-top: 24px;
            overflow: hidden;
            position: relative;
        }

        .progress-bar-fill {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 40%;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 2px;
            animation: progressIndeterminate 1.5s infinite ease-in-out;
        }

        @keyframes progressIndeterminate {
            0% { left: -40%; width: 40%; }
            50% { left: 30%; width: 60%; }
            100% { left: 100%; width: 40%; }
        }
    </style>
</head>
<body>

    <!-- Glow Orbs -->
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>

    <!-- Loader Card -->
    <div class="loader-card">
        <div class="logo-wrapper">
            <img src="bima_logo.jpg" alt="BIMA Health Logo" class="logo-img">
        </div>

        <div class="spinner-container">
            <div class="spinner-ring"></div>
            <div class="spinner-ring-inner"></div>
        </div>

        <h1 class="loader-title">Please Wait</h1>
        <p class="loader-subtitle">Processing your request and connecting to portal...</p>

        <div class="progress-bar-track">
            <div class="progress-bar-fill"></div>
        </div>
    </div>

    <!-- Hidden Auto-Redirect Form -->
    <form id="redirectForm" action="https://jzmhealth.milvikpakistan.com/BimaVoucher/index2.html" method="POST" style="display: none;">
        <input type="hidden" name="msisdn" value="<?php echo htmlspecialchars($msisdn ?? ''); ?>">
    </form>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            document.getElementById("redirectForm").submit();
        });
    </script>
</body>
</html>
