require('dotenv').config();
const QRCode = require('qrcode');
const fs = require('fs');

// 1. THE LIST: Add everyone's details here
const partners = [
    { name: "David Hancock", handle: "davidhancock62", shop: "Eastgate HQ" },
    { name: "Shop Alpha", handle: "shopalpha123", shop: "Alpha Boutique" },
    { name: "Shop Beta", handle: "shopbeta456", shop: "Beta Cafe" }
];

async function generateFactoryQRs() {
    // Create a folder to keep it tidy
    const dir = './DeepBlue_QRs';
    if (!fs.existsSync(dir)) fs.mkdirSync(dir);

    console.log(`🌀 DEEP BLUE FACTORY: STARTING DEPLOYMENT...`);

    for (const person of partners) {
        try {
            const amount = 1.00; // Default test amount
            const payUrl = `https://monzo.me/${person.handle}/${amount}?d=${encodeURIComponent(person.shop)}`;
            
            // File name will be personalized
            const fileName = `${dir}/${person.name.replace(/\s+/g, '_')}_QR.png`;

            await QRCode.toFile(fileName, payUrl, {
                margin: 4,
                scale: 10,
                color: { dark: '#000000', light: '#ffffff' }
            });

            console.log(`✅ Generated: ${person.name} (${person.shop})`);
        } catch (err) {
            console.error(`❌ Error for ${person.name}:`, err.message);
        }
    }
    console.log(`\n📂 All codes are ready in the 'DeepBlue_QRs' folder!`);
}

generateFactoryQRs();