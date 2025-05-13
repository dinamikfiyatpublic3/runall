import { fork } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Test verisi – yalnızca urun_kodu, timestamp, sira gerçek
const testData = {
    link: 'Test',
    ana_kat: 'Test',
    alt_kat1: 'Test',
    alt_kat2: 'Test',
    marka: 'Test',
    urun_kodu: '66211428',
    timestamp: 111111111,
    sira: 1,
    p_adi: 'Test'
};

// Alt süreci başlat
async function processLinkInChildProcess(link, kategoriAna, kategoriAlt, kategoriAlt2, marka, urun_kodu, timestamp, sira, p_adi) {
    return new Promise((resolve, reject) => {
        console.log(`Test: ${urun_kodu} için alt süreç başlatılıyor...`);
        const child = fork(path.resolve(__dirname, '../tests/scrape_api_urunlerim_rakipler.mjs'), [
            link, kategoriAna, kategoriAlt, kategoriAlt2, marka, urun_kodu, timestamp, sira, p_adi
        ]);
        console.log(`Test: Alt süreç PID: ${child.pid}`);

        child.on('message', (message) => {
            console.log(`Test: Alt süreç mesajı (${urun_kodu}):`, message);
            if (message.status === 'error') {
                reject(new Error(`Alt süreç hata: ${message.message}`));
            } else {
                resolve(message);
            }
        });

        child.on('error', (err) => {
            console.error(`Test: Alt süreç başlatılamadı:`, err);
            reject(err);
        });

        child.on('exit', (code) => {
            console.log(`Test: Alt süreç çıktı: Kod = ${code}`);
            if (code !== 0) {
                reject(new Error(`Alt süreç hata ile çıktı: Kod ${code}`));
            } else {
                resolve(`Alt süreç başarıyla tamamlandı.`);
            }
        });
    });
}

// Test başlat
(async () => {
    try {
        await processLinkInChildProcess(
            testData.link,
            testData.ana_kat,
            testData.alt_kat1,
            testData.alt_kat2,
            testData.marka,
            testData.urun_kodu,
            testData.timestamp,
            testData.sira,
            testData.p_adi
        );
    } catch (err) {
        console.error('Test: Hata:', err);
    }
})();
