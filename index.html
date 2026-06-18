<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ParkKarma</title>
    
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#ffc107">
    
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <link rel="stylesheet" href="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css" />
    <script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>

    <script src="https://accounts.google.com/gsi/client" async defer></script>
    
    <style>
        body, html { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; font-family: sans-serif; transition: background 0.3s; }
        #map { height: 100%; width: 100%; position: absolute; top: 0; left: 0; z-index: 1; }
        
        .leaflet-popup-content-wrapper { background: transparent !important; box-shadow: none !important; border: none !important; }
        .leaflet-popup-tip { display: none !important; }
        .leaflet-container a.leaflet-popup-close-button { display: none !important; }

        .marquee-container {
            position: absolute; top: 0; left: 0; width: 100%;
            background: rgba(0, 0, 0, 0.8); color: white;
            padding: 8px 0; overflow: hidden; z-index: 2000;
            white-space: nowrap; pointer-events: none; font-size: 14px;
        }
        .marquee-text {
            display: inline-block; padding-left: 100%;
            animation: marquee 15s linear infinite;
        }
        @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
        
        .controls-container {
            position: absolute; top: 45px; right: 10px; z-index: 1000;
            display: flex; flex-direction: column; gap: 8px;
        }
        
        .karma-display {
            background: #ffc107; padding: 8px 12px; border-radius: 5px;
            font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            text-align: center; color: black; border: 2px solid #e0a800; font-size: 13px;
        }
        
        .menu-btn, .my-location-btn, .my-car-btn {
            background: white; padding: 8px 12px; border-radius: 5px;
            cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            text-align: center; pointer-events: auto; transition: 0.3s; color: #333; font-size: 13px;
        }
        
        .filter-container {
            position: absolute; bottom: 15px; left: 50%; transform: translateX(-50%); z-index: 1000;
            background: rgba(255, 255, 255, 0.95); padding: 8px; border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.4); display: flex; gap: 6px; flex-wrap: nowrap; justify-content: center;
            width: 90%; max-width: 500px; backdrop-filter: blur(5px); transition: 0.3s;
        }
        .filter-select { flex: 1; padding: 6px; border-radius: 6px; border: 1px solid #ccc; font-size: 12px; background: white; font-weight: bold; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        #menu-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 250px; height: 100%;
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px);
            z-index: 3000; padding: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.3); transition: 0.3s; overflow-y: auto;
        }
        .close-menu { cursor: pointer; color: red; font-size: 20px; font-weight: bold; margin-bottom: 20px; }

        .modal {
            display: none; position: fixed; top: 5%; left: 5%; width: 90%; height: 85%;
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
            z-index: 4000; border-radius: 15px; padding: 15px; box-sizing: border-box;
            box-shadow: 0 0 20px rgba(0,0,0,0.3); overflow-y: auto; transition: 0.3s;
        }

        .btn-action, .nav-btn, .occupy-btn, .save-btn, .close-modal, .car-btn { 
            border: none; padding: 10px; width: 100%; margin-top: 8px; 
            cursor: pointer; font-size: 15px; border-radius: 8px; font-weight: bold; color: white;
        }
        .btn-action { background-color: #28a745; }
        .nav-btn { background-color: #007bff; }
        .occupy-btn { background-color: #dc3545; }
        .save-btn { background-color: #ffc107; color: black; }
        .car-btn { background-color: #343a40; }
        .close-modal { background-color: #007bff; }
        .photo-preview { max-width: 100%; display: block; margin: 5px auto; border-radius: 5px; }
        
        .address-text { color: #555; font-size: 13px; margin: 5px 0; font-weight: normal; }
        .spot-tag { background: #e9ecef; color: #333; padding: 4px 8px; border-radius: 4px; font-size: 13px; display: inline-block; margin-bottom: 5px; border: 1px solid #ccc; font-weight: bold; }
        .tag-dropdown { width: 100%; padding: 8px; margin: 5px 0; border-radius: 5px; border: 1px solid #ccc; font-size: 14px; box-sizing: border-box; }

        .leaderboard-list { margin-top: 15px; padding: 0; list-style: none; }
        .leaderboard-item { padding: 12px 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; font-size: 15px; }
        .leaderboard-karma { background: #ffc107; padding: 4px 10px; border-radius: 12px; font-weight: bold; color: black; font-size: 13px;}

        /* RADAR TOAST NOTIFICATION */
        .toast-notification {
            position: fixed; top: 50px; left: 50%; transform: translateX(-50%);
            background: #28a745; color: white; padding: 10px 15px; border-radius: 30px;
            font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 5000;
            display: none; font-size: 14px; white-space: nowrap;
        }

        /* DARK MODE STYLES */
        body.dark-mode .menu-btn, body.dark-mode .my-location-btn, body.dark-mode .my-car-btn { background: #222; color: #fff; border: 1px solid #444; }
        body.dark-mode .filter-container { background: rgba(30, 30, 30, 0.95); }
        body.dark-mode .filter-select { background: #333; color: white; border: 1px solid #555; }
        body.dark-mode #menu-overlay, body.dark-mode .modal { background: rgba(30, 30, 30, 0.95); color: white; }
        body.dark-mode .address-text { color: #ccc; }
        body.dark-mode .leaderboard-item { border-bottom: 1px solid #444; }
        body.dark-mode .spot-tag { background: #444; color: white; border: 1px solid #666; }
        
        .popup-inner { text-align:center; background:white; padding:10px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.3); width: 180px; }
        body.dark-mode .popup-inner { background:#222; color:white; }
        body.dark-mode .tag-dropdown { background: #333; color: white; border: 1px solid #555; }

        /* RESPONSIVE CSS ΓΙΑ ΚΙΝΗΤΑ */
        @media (max-width: 600px) {
            .controls-container { top: 35px; right: 5px; gap: 6px; }
            .menu-btn, .my-location-btn, .my-car-btn { padding: 6px 8px; font-size: 12px; }
            .karma-display { padding: 5px 8px; font-size: 11px; }
            .filter-container { bottom: 10px; width: 95%; padding: 5px; gap: 4px; flex-wrap: nowrap; }
            .filter-select { font-size: 11px; padding: 5px; }
            .leaflet-control-geocoder { max-width: 180px; } 
            .marquee-container { font-size: 12px; padding: 5px 0; }
        }
    </style>
</head>
<body>
    <div class="marquee-container">
        <div class="marquee-text">
            ⚠️ Προσοχή: Η διαθεσιμότητα των θέσεων δεν είναι εγγυημένη 100%! | Δημοσιεύστε μια θέση που αδειάζει | Βοηθήστε την κοινότητα!
        </div>
    </div>

    <div id="radar-toast" class="toast-notification">📡 Νέα θέση μόλις άδειασε κοντά σου!</div>

    <div class="filter-container">
        <select id="filterStatus" class="filter-select" onchange="loadSpots()">
            <option value="all">🚦 Όλες οι Καταστάσεις</option>
            <option value="green">🟢 Μόνο Ελεύθερες</option>
            <option value="red">🔴 Λήγουν Σύντομα</option>
            <option value="violet">🟣 Κρατημένες</option>
        </select>
        <select id="filterTag" class="filter-select" onchange="loadSpots()">
            <option value="all">🏷️ Όλες οι Παροχές</option>
            <option value="photo">📸 Με Φωτογραφία</option>
            <option value="🚙 Χωράει μεγάλο όχημα">🚙 Μεγάλο όχημα</option>
            <option value="♿ Θέση ΑμεΑ / Ράμπα">♿ Θέση ΑμεΑ</option>
            <option value="🌳 Κάτω από δέντρο/Σκιά">🌳 Σκιά</option>
            <option value="⚡ Κοντά σε φορτιστή EV">⚡ Φορτιστής EV</option>
        </select>
    </div>

    <div class="controls-container">
        <div id="karma-box">
            <div id="g_id_onload"
                 data-client_id="766231748892-a0p1h7k1f2nprlqkvdgl0sfffuk0r0am.apps.googleusercontent.com"
                 data-callback="handleCredentialResponse">
            </div>
            <div class="g_id_signin" data-type="standard"></div>
        </div>
        <div class="menu-btn" onclick="toggleMenu()">☰ Μενού</div>
        <div class="my-location-btn" onclick="resetUserMarker()">📍 Επαναφορά μου</div>
        <div class="my-car-btn" onclick="findMyCar()">🅿️ Το αμάξι μου</div>
    </div>

    <div id="menu-overlay">
        <div class="close-menu" onclick="toggleMenu()">✖ Κλείσιμο</div>
        <h2 style="margin-top: 0;">Μενού</h2>
        <ul style="list-style: none; padding: 0;">
            <li id="logout-li" style="display:none; padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer; color: red; font-weight: bold;" onclick="handleLogout()">🚪 Αποσύνδεση</li>
            <li onclick="toggleTheme()" style="padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer; font-weight: bold;">🌞/🌙 Σκοτεινό Θέμα</li>
            <li onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLSdzXc1Wd7tzhm5Nh--3amQbS9rofAzOZNsDLwofPGu6lPESww/viewform?usp=dialog', '_blank')" style="padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer; font-weight: bold; color: #17a2b8;">📝 Αναφορά Προβλήματος / Ιδέες</li>
            <li onclick="openLeaderboard()" style="padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer; font-weight: bold;">🏆 Top Οδηγοί (Leaderboard)</li>
            <li id="admin-li" style="display:none; padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer; color: #e0a800; font-weight: bold;" onclick="openAdminPanel()">👑 Διαχείριση (Admin)</li>
            <li onclick="openModal('instructions-modal')" style="padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer;">ℹ️ Οδηγίες Χρήσης</li>
            <li onclick="openModal('about-modal')" style="padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer;">👥 Σχετικά με εμάς</li>
            <li onclick="openModal('terms-modal')" style="padding:15px 0; border-bottom:1px solid #ccc; cursor:pointer;">📜 Όροι Χρήσης</li>
        </ul>
    </div>

    <div id="leaderboard-modal" class="modal">
        <h2 style="color:#ffc107; text-align:center; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">🏆 Top Οδηγοί</h2>
        <p style="text-align:center; color:#888; margin-top:-10px; font-size: 14px;">Οι χρήστες που βοηθούν περισσότερο την πόλη!</p>
        <ul id="leaderboard-list" class="leaderboard-list">
            <p style="text-align:center;">Φόρτωση...</p>
        </ul>
        <button class="close-modal" onclick="closeModal('leaderboard-modal')">Κλείσιμο</button>
    </div>

    <div id="instructions-modal" class="modal">
        <div class="modal-content">
            <h2 style="color:#007bff;">🚗 Οδηγίες Χρήσης</h2>
            <p>Καλώς ήρθες στην παρέα μας! Εδώ, το παρκάρισμα στην πόλη γίνεται ομαδικό άθλημα. Δες πώς λειτουργεί:</p>

            <h3 style="margin-bottom: 5px;">1. Βρες την ιδανική θέση 🗺️</h3>
            <p style="margin-top: 0; font-size: 14px;">
            • <b>🟢 Πράσινο:</b> Η θέση είναι ελεύθερη – πρόλαβέ την!<br>
            • <b>🔴 Κόκκινο:</b> Ο οδηγός φεύγει σε λιγότερο από 3 λεπτά.<br>
            • <b>🟣 Μοβ:</b> Κάποιος έχει πατήσει "Έρχομαι!". Ψάξε για άλλη!<br>
            • <b>📍 GPS:</b> Πάτα "Οδηγίες" για πλοήγηση.
            </p>

            <h3 style="margin-bottom: 5px;">2. Κάνε κράτηση (Έρχομαι!) 🙋‍♂️</h3>
            <p style="margin-top: 0; font-size: 14px;">Πάτα "Έρχομαι!" σε μια θέση. Γίνεται <b>Μοβ</b> και "κλειδώνει" για σένα για 5 λεπτά, ώστε οι άλλοι να μην κατευθυνθούν εκεί.</p>

            <h3 style="margin-bottom: 5px;">3. Radar Θέσεων 📡</h3>
            <p style="margin-top: 0; font-size: 14px;">Αν αδειάσει θέση σε ακτίνα 1χλμ, ακούς "Μπιπ!" (Θυμήσου να πατήσεις μια φορά τον χάρτη όταν μπαίνεις για να επιτρέψεις τον ήχο).</p>

            <h3 style="margin-bottom: 5px;">4. Γίνε "Θρύλος" 🏆</h3>
            <p style="margin-top: 0; font-size: 14px;">Όταν φεύγεις, πάτα "Δημοσίευσε". Κερδίζεις +10 Karma, βάζεις ετικέτες (π.χ. 🌳 Σκιά) και ανεβαίνεις στο Leaderboard!</p>

            <h3 style="margin-bottom: 5px;">5. Smart Planning (Χρυσή Πινέζα) 🟡</h3>
            <p style="margin-top: 0; font-size: 14px;">Πάτα "Αποθήκευση" μόλις παρκάρεις. Λίγα λεπτά πριν φύγεις, πάτα τη χρυσή πινέζα και "Δημοσίευσε" για να προειδοποιήσεις τους άλλους.</p>

            <h3 style="margin-bottom: 5px;">6. "Πού πάρκαρα;" (Το αμάξι μου) 🚗</h3>
            <p style="margin-top: 0; font-size: 14px;">
            Ξέχασες πού άφησες το αμάξι; <br>
            1️⃣ Πάτα <b>"📍 Επαναφορά μου"</b> και μετά <b>"🚗 Πάρκαρα Εδώ!"</b> για να βάλεις τη μόνιμη Μαύρη Πινέζα.<br>
            2️⃣ Όταν θες να γυρίσεις, πάτα <b>"🅿️ Το αμάξι μου"</b> (πάνω δεξιά) για να δεις οδηγίες πλοήγησης με τα πόδια!
            </p>

            <h3 style="margin-bottom: 5px;">7. Dark Mode & Φίλτρα 🌙</h3>
            <p style="margin-top: 0; font-size: 14px;">Οδηγείς βράδυ; Άνοιξε το Σκοτεινό Θέμα από το μενού. Ψάχνεις πάρκινγκ για ΑμεΑ ή μεγάλο όχημα; Βάλε φίλτρα!</p>

            <div style="background: #e9ecef; padding: 10px; border-radius: 8px; margin-top: 15px; color: #333;">
                <b>Με λίγα λόγια:</b> Είδες ελεύθερο; Πήγαινε. Φεύγεις; Ενημέρωσε. Βοηθάς την πόλη σου!
            </div>

            <button class="close-modal" style="margin-top: 15px;" onclick="closeModal('instructions-modal')">Κλείσιμο</button>
        </div>
    </div>

    <div id="about-modal" class="modal">
        <div class="modal-content">
            <h2 style="color:#007bff;">👥 Σχετικά με εμάς</h2>
            
            <p>Το <b>ParkKarma</b> γεννήθηκε μέσα από το τιμόνι, τις ατέλειωτες γύρες στο ίδιο τετράγωνο και την κλασική καθημερινή ερώτηση: <i>«Πού θα παρκάρω πάλι;»</i>.</p>
            
            <p>Σκεφτήκαμε το εξής απλό: Γιατί να ψάχνουμε στα τυφλά, όταν μπορούμε να γίνουμε όλοι μαζί ένας «ζωντανός χάρτης»; Όταν φεύγει ένας, μπορεί να έρθει απευθείας ο επόμενος. Χωρίς άγχος, χωρίς χαμένη βενζίνη.</p>
            
            <div style="background: #e9ecef; padding: 10px; border-radius: 8px; margin: 15px 0; color: #333;">
                <p style="margin: 0;">Σκοπός μας δεν είναι απλώς να φτιάξουμε άλλη μια εφαρμογή, αλλά μια <b>κοινότητα αλληλεγγύης</b>. Να μοιραζόμαστε τον χώρο και να κάνουμε την πόλη μας πιο φιλική και την καθημερινότητά μας πιο εύκολη.</p>
            </div>

            <h3 style="color:#333; margin-bottom: 5px;">🚀 Το Μέλλον</h3>
            <p style="margin-top: 0; font-size: 14px;">Αυτό είναι μόνο η αρχή! Το όραμά μας είναι το ParkKarma να εξελιχθεί στον απόλυτο συνοδηγό σου. Σύντομα θα προσθέσουμε τρόπους επικοινωνίας (Social Media & Email) για να ακούμε τις ιδέες σου, τις προτάσεις ή ακόμα και τα προβλήματα που συναντάς.</p>
            
            <p style="text-align: center; font-weight: bold; color: #28a745; font-size: 16px; margin-top: 20px;">
                Σε ευχαριστούμε που δίνεις και παίρνεις το καλό... Karma! 🚙✨
            </p>

            <button class="close-modal" style="margin-top: 15px;" onclick="closeModal('about-modal')">Κλείσιμο</button>
        </div>
    </div>

    <div id="terms-modal" class="modal">
        <div class="modal-content">
            <h2 style="color:#007bff;">📜 Όροι Χρήσης & Αποποίηση Ευθύνης</h2>
            
            <p style="font-size: 14px; color: #555;">Παρακαλούμε διαβάστε προσεκτικά τους παρακάτω όρους πριν χρησιμοποιήσετε το ParkKarma.</p>

            <h3 style="margin-bottom: 5px; font-size: 16px;">1. Ασφαλής Οδήγηση (Σημαντικό!) ⚠️</h3>
            <p style="margin-top: 0; font-size: 14px;">Η προσοχή σας πρέπει να βρίσκεται πάντα στον δρόμο. Μην χειρίζεστε την εφαρμογή ενώ οδηγείτε. Χρησιμοποιήστε το ηχητικό Radar ή ζητήστε από τον συνοδηγό να ελέγχει τον χάρτη.</p>

            <h3 style="margin-bottom: 5px; font-size: 16px;">2. Ενημερωτικός Χαρακτήρας ℹ️</h3>
            <p style="margin-top: 0; font-size: 14px;">Το <b>ParkKarma</b> βασίζεται αποκλειστικά στην κοινότητα (crowdsourcing). Η εφαρμογή <b>δεν εγγυάται</b> τη διαθεσιμότητα καμίας θέσης στάθμευσης, καθώς μια θέση μπορεί να καταληφθεί από άλλο όχημα πριν φτάσετε.</p>

            <h3 style="margin-bottom: 5px; font-size: 16px;">3. Αποποίηση Ευθύνης 🚫</h3>
            <p style="margin-top: 0; font-size: 14px;">Οι δημιουργοί της εφαρμογής δεν φέρουν απολύτως καμία ευθύνη για:<br>
            • Τυχόν ατυχήματα ή υλικές ζημιές κατά την οδήγηση ή στάθμευση.<br>
            • Κλήσεις της Τροχαίας, πρόστιμα ή παράνομη στάθμευση. Ο οδηγός οφείλει να ελέγχει πάντα τη σήμανση (π.χ. ράμπες ΑμεΑ, διαβάσεις, πινακίδες).<br>
            • Ανακρίβειες στα δεδομένα που αναρτούν άλλοι χρήστες.</p>

            <h3 style="margin-bottom: 5px; font-size: 16px;">4. Υπεύθυνη Χρήση & Karma ⚖️</h3>
            <p style="margin-top: 0; font-size: 14px;">Απαγορεύεται η σκόπιμη δημοσίευση ψευδών θέσεων ή η κατάχρηση του κουμπιού "Έρχομαι!". Οι λογαριασμοί που δημοσιεύουν κακόβουλα (trolls) ή προσπαθούν να ξεγελάσουν το σύστημα πόντων (Karma) θα αποκλείονται από την εφαρμογή.</p>

            <h3 style="margin-bottom: 5px; font-size: 16px;">5. Ιδιωτικότητα & Διαχείριση Δεδομένων 🔒</h3>
            <p style="margin-top: 0; font-size: 14px;">
            Η εφαρμογή σέβεται την ιδιωτικότητά σας, ωστόσο για την αποφυγή κακόβουλης χρήσης (trolling) και την προστασία της κοινότητας, ισχύουν τα εξής:<br>
            • <b>Για Επώνυμους Χρήστες:</b> Το Email που χρησιμοποιείτε κατά τη σύνδεση μέσω Google αποθηκεύεται με ασφάλεια στη βάση δεδομένων και είναι ορατό <u>αποκλειστικά και μόνο στον διαχειριστή (Admin)</u> της εφαρμογής για λόγους ελέγχου εγκυρότητας των πινεζών.<br>
            • <b>Για Ανώνυμους Χρήστες:</b> Παράγεται ένα τυχαίο, ανώνυμο αναγνωριστικό συσκευής (Device ID) το οποίο συνδέεται με τις πινέζες σας.<br>
            • Σε καμία περίπτωση τα στοιχεία αυτά δεν δημοσιοποιούνται σε άλλους απλούς χρήστες ούτε κοινοποιούνται σε τρίτους. Χρησιμοποιώντας την εφαρμογή, συναινείτε στην παραπάνω διαχείριση για την ασφάλεια του app.
            </p>

            <button id="accept-terms-btn" class="close-modal" style="margin-top: 15px; background-color: #28a745;" onclick="acceptTerms()">Συμφωνώ & Αποδοχή</button>
        </div>
    </div>

    <div id="admin-modal" class="modal">
        <div class="modal-content">
            <h2 style="color:#e0a800; text-align: center;">👑 Πίνακας Διαχειριστή</h2>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: inset 0 0 5px rgba(0,0,0,0.1); margin-bottom: 20px; color: #333;">
                <h3 style="margin-top: 0;">📊 Live Στατιστικά</h3>
                <p>• Εγγεγραμμένοι Χρήστες: <b id="stat-users">0</b></p>
                <p>• Ελεύθερες Πινέζες (🟢/🔴): <b id="stat-active">0</b></p>
                <p>• Κρατημένες Πινέζες (🟣): <b id="stat-booked">0</b></p>
            </div>

            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: inset 0 0 5px rgba(0,0,0,0.1); color: #333;">
                <h3 style="margin-top: 0; color: #dc3545;">🚫 Διαχείριση Χρηστών (Ban)</h3>
                <p style="font-size: 13px; color: #666;">Εισάγετε το Email χρήστη ή το Ανώνυμο ID (π.χ. anon_x9b2) για οριστική διαγραφή.</p>
                <input type="text" id="ban-email-input" placeholder="π.χ. troll@gmail.com ή anon_x9b2" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box;">
                <button class="occupy-btn" style="margin-top: 10px;" onclick="adminBanUser()">Οριστική Διαγραφή</button>
            </div>

            <button class="close-modal" style="margin-top: 20px; background-color: #343a40;" onclick="closeModal('admin-modal')">Κλείσιμο</button>
        </div>
    </div>

    <div id="map"></div>
    
    <script>
        const API_BASE_URL = "https://parking-mhsn.onrender.com";
        var map = L.map('map', { maxZoom: 19, minZoom: 3 }).setView([39.6384, 22.4152], 16);
        var savedPositions = [], markers = [], savedMarkers = [], userMarker = null, lastClickedMarker = null, searchMarker = null, myCarMarker = null;

        let userEmail = localStorage.getItem('parkkarma_email') || null;
        let anonDeviceID = localStorage.getItem('parkkarma_anon_id');
        if (!anonDeviceID) {
            anonDeviceID = 'anon_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('parkkarma_anon_id', anonDeviceID);
        }

        let currentTheme = localStorage.getItem('parkkarma_theme') || 'light';
        let mapLayerLight = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        let mapLayerDark = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
        
        let baseLayer = L.tileLayer(currentTheme === 'dark' ? mapLayerDark : mapLayerLight, { 
            attribution: '© OpenStreetMap/CartoDB', maxZoom: 19 
        }).addTo(map);

        if (currentTheme === 'dark') document.body.classList.add('dark-mode');

        function toggleTheme() {
            currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('parkkarma_theme', currentTheme);
            if(currentTheme === 'dark') {
                document.body.classList.add('dark-mode');
                baseLayer.setUrl(mapLayerDark);
            } else {
                document.body.classList.remove('dark-mode');
                baseLayer.setUrl(mapLayerLight);
            }
            toggleMenu(); 
        }

        function getBadge(karma) {
            if(karma >= 500) return "💎 Θρύλος";
            if(karma >= 150) return "🥇 Τοπικός Ήρωας";
            if(karma >= 50) return "🥈 Πρόσκοπος";
            return "🥉 Αρχάριος";
        }

        let isPopupOpen = false;
        let popupJustClosed = false;

        map.on('popupopen', function() { isPopupOpen = true; });
        map.on('popupclose', function() {
            isPopupOpen = false;
            popupJustClosed = true;
            setTimeout(() => { popupJustClosed = false; }, 200);
        });

        let notifiedSpots = new Set();
        function playRadarBeep() {
            try {
                let audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
                audio.play().catch(e => console.log("Audio muted"));
            } catch(e){}
        }
        function showRadarToast(distance) {
            let toast = document.getElementById('radar-toast');
            toast.innerText = `📡 Νέα θέση μόλις άδειασε στα ${distance} μέτρα!`;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 5000);
        }

        function setMyCar() {
            if (!userMarker) return;
            let pos = userMarker.getLatLng();
            localStorage.setItem('parkkarma_my_car', JSON.stringify({lat: pos.lat, lng: pos.lng}));
            alert("Η θέση του αυτοκινήτου σου αποθηκεύτηκε! Μπορείς να την βρεις από το κουμπί 'Το αμάξι μου'.");
            map.closePopup();
            renderMyCarMarker();
        }
        function clearMyCar() {
            localStorage.removeItem('parkkarma_my_car');
            if(myCarMarker) { map.removeLayer(myCarMarker); myCarMarker = null; }
            map.closePopup();
        }
        function renderMyCarMarker() {
            let data = localStorage.getItem('parkkarma_my_car');
            if (!data) return;
            let pos = JSON.parse(data);
            if (myCarMarker) map.removeLayer(myCarMarker);
            
            let icon = L.icon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png', shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png', iconSize: [25, 41], iconAnchor: [12, 41] });
            
            myCarMarker = L.marker([pos.lat, pos.lng], {icon: icon}).addTo(map)
                .bindPopup(`<div class="popup-inner"><b>Το αυτοκίνητό μου 🚗</b><br><button class="nav-btn" onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${pos.lat},${pos.lng}&travelmode=walking', '_blank')">🚶 Πλοήγηση (Πόδια)</button><button class="occupy-btn" onclick="clearMyCar()">❌ Διαγραφή</button></div>`);
        }
        function findMyCar() {
            let data = localStorage.getItem('parkkarma_my_car');
            if (data) {
                let pos = JSON.parse(data);
                map.setView([pos.lat, pos.lng], 18);
                if(myCarMarker) myCarMarker.openPopup();
            } else {
                alert("Δεν έχεις αποθηκεύσει τη θέση! Πάτα 'Επαναφορά μου' και 'Πάρκαρα Εδώ!' για να την σώσεις.");
            }
        }
        renderMyCarMarker();

        async function getAddress(lat, lng) {
            try {
                let res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`);
                let data = await res.json();
                if (data && data.address) {
                    let street = data.address.road || data.address.pedestrian || "";
                    let number = data.address.house_number || "";
                    let city = data.address.city || data.address.town || data.address.village || "";
                    let result = `${street} ${number}, ${city}`.trim();
                    result = result.replace(/^,\s*/, '').replace(/,\s*$/, '');
                    return result || "Άγνωστη διεύθυνση";
                }
                return "Διεύθυνση μη διαθέσιμη";
            } catch (e) { return "Σφάλμα διεύθυνσης"; }
        }

        // --- ΛΟΓΙΚΗ ΓΙΑ ADMIN ---
        function checkAdminStatus(email) {
            if (email === "george@parkkarmaapp.com") {
                document.getElementById('admin-li').style.display = 'block';
            } else {
                document.getElementById('admin-li').style.display = 'none';
            }
        }

        async function openAdminPanel() {
            openModal('admin-modal');
            try {
                let res = await fetch(`${API_BASE_URL}/admin/stats?email=${userEmail}`);
                if (res.ok) {
                    let data = await res.json();
                    document.getElementById('stat-users').innerText = data.total_users;
                    document.getElementById('stat-active').innerText = data.active_spots;
                    document.getElementById('stat-booked').innerText = data.booked_spots;
                }
            } catch(e) { alert("Σφάλμα κατά τη φόρτωση των στατιστικών."); }
        }

        async function adminBanUser() {
            let trollEmail = document.getElementById('ban-email-input').value.trim();
            if (!trollEmail) { alert("Παρακαλώ βάλτε ένα έγκυρο email ή ID."); return; }
            
            if (confirm(`Είστε σίγουρος ότι θέλετε να διαγράψετε οριστικά τον χρήστη/συσκευή ${trollEmail};`)) {
                try {
                    let res = await fetch(`${API_BASE_URL}/admin/ban-user?email=${userEmail}&user_to_ban=${trollEmail}`, { method: 'DELETE' });
                    if (res.ok) {
                        alert("Η διαγραφή ολοκληρώθηκε επιτυχώς!");
                        document.getElementById('ban-email-input').value = "";
                        openAdminPanel();
                        loadSpots();
                    } else {
                        let err = await res.json();
                        alert(err.detail || "Σφάλμα.");
                    }
                } catch(e) { alert("Αποτυχία σύνδεσης με τον server."); }
            }
        }

        // --- ΛΟΓΙΚΗ ΓΙΑ REPORT SPOT ---
        async function reportSpot(spotId) {
            if(confirm("Είστε σίγουρος ότι αυτή η θέση είναι ψεύτικη ή δεν υπάρχει πια;")) {
                let ident = userEmail ? userEmail : anonDeviceID;
                try {
                    let res = await fetch(`${API_BASE_URL}/report-spot/${spotId}?reporter_id=${ident}`, { method: 'POST' });
                    if (res.ok) {
                        let data = await res.json();
                        alert(data.message);
                        map.closePopup();
                        loadSpots();
                    } else {
                        alert("Σφάλμα κατά την αναφορά.");
                    }
                } catch(e) { alert("Αποτυχία σύνδεσης με τον server."); }
            }
        }

        async function handleCredentialResponse(response) {
            let localSpots = JSON.parse(localStorage.getItem('parkkarma_saved_spots')) || [];
            let res = await fetch(`${API_BASE_URL}/auth/google`, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id_token: response.credential, local_spots: localSpots })
            });
            if (res.ok) {
                let data = await res.json();
                userEmail = data.email;
                localStorage.setItem('parkkarma_email', userEmail);
                localStorage.removeItem('parkkarma_saved_spots'); 
                savedPositions = data.saved_locations || [];
                showAllSavedMarkers();
                updateUIForLoggedInUser(data.karma);
                checkAdminStatus(userEmail);
            }
        }

        function updateUIForLoggedInUser(karma) {
            let badge = getBadge(karma);
            document.getElementById('karma-box').innerHTML = `<div class="karma-display" id="karma-points">🌟 ${karma} Karma<br><small>${badge}</small></div>`;
            document.getElementById('logout-li').style.display = 'block';
        }

        function handleLogout() {
            localStorage.removeItem('parkkarma_email');
            localStorage.removeItem('parkkarma_saved_spots');
            location.reload();
        }

        async function fetchKarma() {
            if (!userEmail) return;
            try {
                let res = await fetch(`${API_BASE_URL}/my-karma/${userEmail}`);
                if (res.ok) {
                    let data = await res.json();
                    let badge = getBadge(data.karma);
                    document.getElementById('karma-points').innerHTML = `🌟 ${data.karma} Karma<br><small>${badge}</small>`;
                    savedPositions = data.saved_locations || [];
                    showAllSavedMarkers();
                }
            } catch (e) {}
        }

        if (userEmail) { 
            setTimeout(() => { 
                updateUIForLoggedInUser(0); 
                fetchKarma(); 
                checkAdminStatus(userEmail);
            }, 500); 
        } 
        else { 
            savedPositions = JSON.parse(localStorage.getItem('parkkarma_saved_spots')) || []; 
            setTimeout(showAllSavedMarkers, 500); 
        }

        function toggleMenu() { document.getElementById('menu-overlay').style.display = (document.getElementById('menu-overlay').style.display === 'block') ? 'none' : 'block'; }
        
        function openModal(id) { 
            if (localStorage.getItem('parkkarma_terms_accepted') !== 'true' && id !== 'terms-modal') {
                return;
            }
            document.getElementById(id).style.display = 'block'; 
            if(document.getElementById('menu-overlay').style.display === 'block') toggleMenu(); 
        }
        
        function closeModal(id) { 
            if (localStorage.getItem('parkkarma_terms_accepted') !== 'true' && id === 'terms-modal') {
                alert("Πρέπει να αποδεχτείτε τους όρους χρήσης για να χρησιμοποιήσετε την εφαρμογή.");
                return;
            }
            document.getElementById(id).style.display = 'none'; 
        }

        function checkTermsOnStartup() {
            if (localStorage.getItem('parkkarma_terms_accepted') !== 'true') {
                document.getElementById('terms-modal').style.display = 'block';
            }
        }
        
        function acceptTerms() {
            localStorage.setItem('parkkarma_terms_accepted', 'true');
            document.getElementById('terms-modal').style.display = 'none';
        }

        async function openLeaderboard() {
            openModal('leaderboard-modal');
            document.getElementById('leaderboard-list').innerHTML = "<p style='text-align:center;'>Φόρτωση δεδομένων...</p>";
            try {
                let res = await fetch(`${API_BASE_URL}/leaderboard`);
                let data = await res.json();
                let html = "";
                if(data.leaderboard.length === 0) {
                    html = "<p style='text-align:center;'>Δεν υπάρχουν ακόμα οδηγοί με Karma.</p>";
                } else {
                    data.leaderboard.forEach((item, index) => {
                        let rankIcon = index === 0 ? "👑" : index === 1 ? "🥈" : index === 2 ? "🥉" : "🔹";
                        let userBadge = getBadge(item.karma);
                        html += `<li class="leaderboard-item">
                                    <span style="display:flex; flex-direction:column;">
                                        <span>${rankIcon} <b>${item.user}</b></span>
                                        <small style="color:#888; font-size:12px; margin-left:25px;">${userBadge}</small>
                                    </span>
                                    <span class="leaderboard-karma">${item.karma}</span>
                                 </li>`;
                    });
                }
                document.getElementById('leaderboard-list').innerHTML = html;
            } catch(e) {
                document.getElementById('leaderboard-list').innerHTML = "<p style='text-align:center; color:red;'>Σφάλμα σύνδεσης.</p>";
            }
        }

        L.Control.geocoder({
            position: 'topleft', defaultMarkGeocode: false, placeholder: 'Αναζήτηση...', errorMessage: 'Δεν βρέθηκε.'
        }).on('markgeocode', function(e) {
            var bbox = e.geocode.bbox; map.fitBounds(bbox);
            if (searchMarker) map.removeLayer(searchMarker);
            searchMarker = L.marker(e.geocode.center).addTo(map).bindPopup(`<div class="popup-inner"><b>Αναζήτηση:</b><br><span class="address-text">📍 ${e.geocode.name}</span></div>`).openPopup();
        }).addTo(map);

        window.addEventListener('resize', () => map.invalidateSize());

        function showAllSavedMarkers() {
            savedMarkers.forEach(m => map.removeLayer(m)); savedMarkers = [];
            savedPositions.forEach((spot, index) => {
                let popupId = `saved_addr_${index}`;
                let tagSelectId = `savedTagInput_${index}`;
                let popupContent = `<div class="popup-inner">
                    <b>Αποθηκευμένη θέση #${index+1}</b><br>
                    <div class="address-text" id="${popupId}">📍 Φόρτωση...</div>
                    <select id="${tagSelectId}" class="tag-dropdown">
                        <option value="">-- Χωρίς Ετικέτα --</option>
                        <option value="🚙 Χωράει μεγάλο όχημα">🚙 Μεγάλο όχημα</option>
                        <option value="♿ Θέση ΑμεΑ / Ράμπα">♿ Θέση ΑμεΑ</option>
                        <option value="🌳 Κάτω από δέντρο/Σκιά">🌳 Σκιά</option>
                    </select>
                    <input type="file" id="savedPhotoInput_${index}" accept="image/*" style="width:100%; margin:5px 0;">
                    <button class="btn-action" onclick="submitSavedWithPhoto(${index}, ${spot.lat}, ${spot.lng})">📢 Δημοσίευσε</button>
                    <button class="occupy-btn" onclick="deleteSavedMarker(${spot.id}, ${index})">🗑️ Διαγραφή</button>
                </div>`;
                let marker = L.marker([spot.lat, spot.lng], { icon: L.icon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png', shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png', iconSize: [25, 41], iconAnchor: [12, 41] }) }).addTo(map).bindPopup(popupContent);
                marker.on('click', async () => {
                    let el = document.getElementById(popupId);
                    if(el && el.innerText.includes('Φόρτωση')) { let addr = await getAddress(spot.lat, spot.lng); if(document.getElementById(popupId)) document.getElementById(popupId).innerText = `📍 ${addr}`; }
                });
                savedMarkers.push(marker);
            });
        }

        function submitSavedWithPhoto(index, lat, lng) {
            const file = document.getElementById(`savedPhotoInput_${index}`).files[0];
            const tagValue = document.getElementById(`savedTagInput_${index}`).value;
            let mins = prompt("Πόσα λεπτά θα είσαι ελεύθερος;", "10");
            if (mins) {
                if (file) {
                    const reader = new FileReader();
                    reader.onloadend = () => { sendToServer(lat, lng, mins, reader.result, tagValue); };
                    reader.readAsDataURL(file);
                } else { sendToServer(lat, lng, mins, null, tagValue); }
            }
        }

        async function deleteSavedMarker(dbId, localIndex) { 
            if (userEmail && dbId) await fetch(`${API_BASE_URL}/delete-saved-location/${dbId}`, { method: 'DELETE' });
            savedPositions.splice(localIndex, 1);
            if (!userEmail) localStorage.setItem('parkkarma_saved_spots', JSON.stringify(savedPositions));
            map.closePopup(); showAllSavedMarkers();
        }

        function resetUserMarker() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(async (pos) => {
                    const lat = pos.coords.latitude; const lng = pos.coords.longitude;
                    if (userMarker) userMarker.setLatLng([lat, lng]); else userMarker = L.marker([lat, lng], { draggable: true }).addTo(map);
                    
                    let popupId = "user_spot_addr";
                    userMarker.bindPopup(`<div class="popup-inner">
                        <b>Είσαι εδώ!</b><br>
                        <div class="address-text" id="${popupId}">📍 Φόρτωση...</div>
                        <select id="userTagInput" class="tag-dropdown">
                            <option value="">-- Χωρίς Ετικέτα --</option>
                            <option value="🚙 Χωράει μεγάλο όχημα">🚙 Μεγάλο όχημα</option>
                            <option value="♿ Θέση ΑμεΑ / Ράμπα">♿ Θέση ΑμεΑ</option>
                        </select>
                        <button class="save-btn" onclick="saveCurrentLocation()">💾 Αποθήκευση</button>
                        <button class="car-btn" onclick="setMyCar()">🚗 Πάρκαρα Εδώ!</button>
                        <input type="file" id="photoInput" accept="image/*" style="width:100%; margin:5px 0;">
                        <button class="btn-action" onclick="submitPosition(true)">📢 Δημοσίευσε</button>
                    </div>`).openPopup();
                    
                    map.setView([lat, lng], 17);
                    let addr = await getAddress(lat, lng);
                    let addrEl = document.getElementById(popupId);
                    if(addrEl) addrEl.innerText = `📍 ${addr}`;
                }, null, { enableHighAccuracy: true });
            }
        }

        async function saveCurrentLocation() {
            let pos = userMarker.getLatLng();
            if (savedPositions.length >= 10) { alert("Μέγιστο όριο 10 θέσεων!"); return; }
            let newSpot = { lat: pos.lat, lng: pos.lng, id: null };
            if (userEmail) {
                let res = await fetch(`${API_BASE_URL}/save-location`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: userEmail, latitude: pos.lat, longitude: pos.lng }) });
                if (res.ok) { let data = await res.json(); newSpot.id = data.id; }
            } else { newSpot.id = Date.now(); }
            savedPositions.push(newSpot);
            if (!userEmail) localStorage.setItem('parkkarma_saved_spots', JSON.stringify(savedPositions));
            showAllSavedMarkers(); alert("Αποθηκεύτηκε!"); userMarker.closePopup();
        }

        function saveClickedLocation() {
            if (!lastClickedMarker) return;
            let pos = lastClickedMarker.getLatLng();

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(async (currentPos) => {
                    let distance = L.latLng(currentPos.coords.latitude, currentPos.coords.longitude).distanceTo(L.latLng(pos.lat, pos.lng));
                    if (distance > 60) { 
                        alert("Μπορείς να αποθηκεύσεις μια θέση μόνο αν βρίσκεσαι κοντά της (έως 60 μέτρα)!"); 
                        return; 
                    }
                    
                    if (savedPositions.length >= 10) { alert("Μέγιστο όριο 10 θέσεων!"); return; }
                    let newSpot = { lat: pos.lat, lng: pos.lng, id: null };
                    if (userEmail) {
                        let res = await fetch(`${API_BASE_URL}/save-location`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: userEmail, latitude: pos.lat, longitude: pos.lng }) });
                        if (res.ok) { let data = await res.json(); newSpot.id = data.id; }
                    } else { newSpot.id = Date.now(); }
                    
                    savedPositions.push(newSpot);
                    if (!userEmail) localStorage.setItem('parkkarma_saved_spots', JSON.stringify(savedPositions));
                    showAllSavedMarkers(); 
                    alert("Αποθηκεύτηκε!"); 
                    cancelClickedMarker();
                }, (err) => { alert("Πρέπει να δώσεις άδεια (GPS) για να αποθηκεύσεις."); }, { enableHighAccuracy: true });
            } else { alert("Δεν υποστηρίζεται GPS."); }
        }

        function submitPosition(isUserMarker) {
            let pos, fileInput, tagValue;
            if (isUserMarker) { 
                pos = userMarker.getLatLng(); fileInput = document.getElementById('photoInput'); tagValue = document.getElementById('userTagInput') ? document.getElementById('userTagInput').value : "";
                processSubmission(pos, fileInput, isUserMarker, tagValue);
            } else { 
                if (!lastClickedMarker) return; 
                pos = lastClickedMarker.getLatLng(); fileInput = document.getElementById('clickPhotoInput'); tagValue = document.getElementById('clickTagInput') ? document.getElementById('clickTagInput').value : "";
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition((currentPos) => {
                        let distance = L.latLng(currentPos.coords.latitude, currentPos.coords.longitude).distanceTo(L.latLng(pos.lat, pos.lng));
                        if (distance > 60) { alert("Μόνο αν βρίσκεσαι κοντά της (έως 60 μέτρα)!"); return; }
                        processSubmission(pos, fileInput, isUserMarker, tagValue);
                    }, (err) => { alert("Πρέπει να δώσεις άδεια (GPS)."); }, { enableHighAccuracy: true });
                } else { alert("Δεν υποστηρίζεται GPS."); }
            }
        }

        function processSubmission(pos, fileInput, isUserMarker, tagValue) {
            const file = fileInput.files[0];
            let mins = prompt("Πόσα λεπτά θα είσαι ελεύθερος;", "10");
            if (mins) {
                if (file) {
                    const reader = new FileReader();
                    reader.onloadend = () => { sendToServer(pos.lat, pos.lng, mins, reader.result, tagValue); if (!isUserMarker) cancelClickedMarker(); };
                    reader.readAsDataURL(file);
                } else { sendToServer(pos.lat, pos.lng, mins, null, tagValue); if (!isUserMarker) cancelClickedMarker(); }
            }
        }

        map.on('click', async function(e) {
            let menuOverlay = document.getElementById('menu-overlay');
            let isMenuOpen = menuOverlay && menuOverlay.style.display === 'block';

            if (isMenuOpen || isPopupOpen || popupJustClosed || lastClickedMarker || searchMarker) {
                if (isMenuOpen) menuOverlay.style.display = 'none';
                if (lastClickedMarker) { map.removeLayer(lastClickedMarker); lastClickedMarker = null; }
                if (searchMarker) { map.removeLayer(searchMarker); searchMarker = null; }
                map.closePopup(); 
                return; 
            }

            lastClickedMarker = L.marker(e.latlng, { draggable: true }).addTo(map);
            let popupId = "new_spot_addr";
            let popupContent = `<div class="popup-inner">
                <b>Νέα θέση</b><br>
                <div class="address-text" id="${popupId}">📍 Φόρτωση...</div>
                <select id="clickTagInput" class="tag-dropdown">
                    <option value="">-- Χωρίς Ετικέτα --</option>
                    <option value="🚙 Χωράει μεγάλο όχημα">🚙 Μεγάλο όχημα</option>
                    <option value="♿ Θέση ΑμεΑ / Ράμπα">♿ Θέση ΑμεΑ</option>
                </select>
                <button class="save-btn" style="margin-top:5px; width:100%;" onclick="saveClickedLocation()">💾 Αποθήκευση</button><br>
                <input type="file" id="clickPhotoInput" accept="image/*" style="width:100%; margin:8px 0;"><br>
                <button class="btn-action" style="margin-top:5px; width:100%;" onclick="submitPosition(false)">📢 Δημοσίευσε</button>
                <button class="occupy-btn" style="margin-top:5px; width:100%;" onclick="cancelClickedMarker()">✖️ Ακύρωση</button>
            </div>`;
            
            lastClickedMarker.bindPopup(popupContent).openPopup();
            lastClickedMarker.bringToFront();
            L.DomEvent.disableClickPropagation(lastClickedMarker._popup._container);
            
            let addr = await getAddress(e.latlng.lat, e.latlng.lng);
            let addrEl = document.getElementById(popupId);
            if(addrEl) addrEl.innerText = `📍 ${addr}`;
        });

        function cancelClickedMarker() { if (lastClickedMarker) map.removeLayer(lastClickedMarker); lastClickedMarker = null; map.closePopup(); }

        async function sendToServer(lat, lng, mins, photo, tagValue) {
            await fetch(`${API_BASE_URL}/free-spot`, { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify({ 
                    user_email: userEmail, 
                    latitude: lat, 
                    longitude: lng, 
                    minutes_until_free: parseInt(mins), 
                    photo: photo, 
                    tag: tagValue || null,
                    device_id: anonDeviceID
                }) 
            });
            alert(userEmail ? "Δημοσιεύτηκε! Θα κερδίσεις πόντους (Karma) όταν κάποιος οδηγός πιάσει τη θέση." : "Η θέση δημοσιεύτηκε ανώνυμα!");
            map.closePopup(); loadSpots();
        }

        async function bookSpot(spotId) {
            let ident = userEmail ? userEmail : anonDeviceID;
            let res = await fetch(`${API_BASE_URL}/book-spot/${spotId}?occupier_id=${ident}`, { method: 'POST' });
            if (res.ok) { alert("🚙 Η θέση κρατήθηκε για 5 λεπτά!"); map.closePopup(); loadSpots(); } 
            else { let error = await res.json(); alert(error.detail || "Σφάλμα."); }
        }

        async function unbookSpot(spotId) {
            let ident = userEmail ? userEmail : anonDeviceID;
            let res = await fetch(`${API_BASE_URL}/unbook-spot/${spotId}?occupier_id=${ident}`, { method: 'POST' });
            if (res.ok) { alert("Ακυρώθηκε."); map.closePopup(); loadSpots(); }
        }

        async function loadSpots() {
            let res = await fetch(`${API_BASE_URL}/search-spots`);
            let data = await res.json();
            let ident = userEmail ? userEmail : anonDeviceID;
            let filterStatus = document.getElementById('filterStatus').value;
            let filterTag = document.getElementById('filterTag').value;
            
            markers.forEach(m => map.removeLayer(m)); markers = [];
            
            data.spots.forEach(spot => {
                let dateStr = spot.created_at;
                if (!dateStr.includes('Z') && !dateStr.includes('+')) { dateStr += 'Z'; }
                let created = new Date(dateStr);
                let remaining = spot.minutes_until_free - Math.floor((new Date() - created) / 60000);
                
                if (remaining > 0) {
                    let isBooked = spot.is_booked;
                    let bookedByMe = isBooked && spot.booked_by === ident;
                    let color = remaining <= 3 ? 'red' : 'green';
                    if (isBooked) color = 'violet'; 
                    
                    if (color === 'green' && !isBooked && !notifiedSpots.has(spot.id) && userMarker) {
                        let distance = Math.round(userMarker.getLatLng().distanceTo(L.latLng(spot.latitude, spot.longitude)));
                        if (distance < 1000) { 
                            playRadarBeep();
                            showRadarToast(distance);
                            notifiedSpots.add(spot.id);
                        }
                    }

                    if (filterStatus === 'green' && color !== 'green') return; 
                    if (filterStatus === 'red' && color !== 'red') return;
                    if (filterStatus === 'violet' && color !== 'violet') return;
                    if (filterTag === 'photo' && !spot.photo) return;
                    if (filterTag !== 'all' && filterTag !== 'photo' && spot.tag !== filterTag) return;
                    
                    let icon = L.icon({ iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`, shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png', iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41] });
                    let photoHtml = spot.photo ? `<img src="${spot.photo}" class="photo-preview"><br>` : "";
                    let tagHtml = spot.tag ? `<div class="spot-tag">${spot.tag}</div><br>` : "";
                    
                    let adminInfoHtml = "";
                    if (userEmail === "george@parkkarmaapp.com") {
                        let publisher = spot.user_email ? spot.user_email : `Ανώνυμος (${spot.device_id})`;
                        let reportsBadge = spot.reports_count > 0 ? `<br><span style="color:red;">🚩 Αναφορές Θέσης: ${spot.reports_count}</span>` : "";
                        let userReportsBadge = spot.user_total_reports > 0 ? `<br><span style="color:darkred;">⚠️ Συνολικές Αναφορές Χρήστη: ${spot.user_total_reports}</span>` : "";
                        adminInfoHtml = `<div style="font-size:11px; color:#e0a800; font-weight:bold; margin-bottom:5px; background:#fff3cd; padding:3px; border-radius:4px; border:1px solid #ffeeba; word-break:break-all;">👤 Από: ${publisher}${reportsBadge}${userReportsBadge}</div>`;
                    }
                    
                    let buttonsHtml = `<button class="nav-btn" onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${spot.latitude},${spot.longitude}&travelmode=driving', '_blank')">🚗 Οδηγίες GPS</button>`;
                    
                    if (isBooked) {
                        if (bookedByMe) {
                            buttonsHtml += `<button class="save-btn" onclick="unbookSpot(${spot.id})">✖️ Ακύρωση 'Έρχομαι'</button>`;
                            buttonsHtml += `<button class="occupy-btn" onclick="occupySpot(${spot.id}, ${spot.latitude}, ${spot.longitude}, '${spot.device_id}')">❌ Έφτασα! (Κατάληψη)</button>`;
                        } else { buttonsHtml += `<p style="color:purple; font-weight:bold; margin-top:10px; border: 2px solid purple; padding: 5px; border-radius: 5px;">🟣 Οδηγός καθ' οδόν!</p>`; }
                    } else {
                        buttonsHtml += `<button class="btn-action" style="background-color: #17a2b8;" onclick="bookSpot(${spot.id})">🙋‍♂️ Έρχομαι!</button>`;
                        buttonsHtml += `<button class="occupy-btn" onclick="occupySpot(${spot.id}, ${spot.latitude}, ${spot.longitude}, '${spot.device_id}')">❌ Κατειλημμένη</button>`;
                    }

                    buttonsHtml += `<button class="occupy-btn" style="background-color: #fd7e14; margin-top:5px;" onclick="reportSpot(${spot.id})">🚩 Αναφορά (Fake)</button>`;
                    
                    let popupId = `pub_addr_${spot.id}`;
                    let marker = L.marker([spot.latitude, spot.longitude], {icon: icon}).addTo(map)
                        .bindPopup(`<div class="popup-inner">${adminInfoHtml}${photoHtml}${tagHtml}<div class="address-text" id="${popupId}">📍 Φόρτωση...</div><b>Λήγει σε: ${remaining} λεπτά</b><br>${buttonsHtml}</div>`);
                        
                    marker.on('click', async () => {
                        let el = document.getElementById(popupId);
                        if(el && el.innerText.includes('Φόρτωση')) { let addr = await getAddress(spot.latitude, spot.longitude); if(document.getElementById(popupId)) document.getElementById(popupId).innerText = `📍 ${addr}`; }
                    });
                    markers.push(marker);
                }
            });
        }

        async function occupySpot(spotId, spotLat, spotLng, creatorId) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(async (pos) => {
                    let distance = L.latLng(pos.coords.latitude, pos.coords.longitude).distanceTo(L.latLng(spotLat, spotLng));
                    if (distance > 60) { alert("Είσαι μακριά (όριο 60μ)!"); return; }
                    let ident = userEmail ? userEmail : "anonymous";
                    await fetch(`${API_BASE_URL}/occupy-spot/${spotId}?occupier_email=${ident}`, { method: 'DELETE' });
                    map.closePopup(); loadSpots(); fetchKarma(); 
                }, (err) => { alert("Άδεια GPS απαραίτητη."); }, { enableHighAccuracy: true });
            }
        }

        resetUserMarker(); loadSpots(); 
        
        setInterval(loadSpots, 20000);
        setInterval(fetchKarma, 20000);

        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(reg => console.log('Service Worker Registered!'))
                    .catch(err => console.log('Service Worker Failed:', err));
            });
        }

        window.addEventListener('DOMContentLoaded', checkTermsOnStartup);
    </script>
</body>
</html>
