const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.launch({headless: 'new'});
        const page = await browser.newPage();
        await page.setViewport({width: 1440, height: 900});
        await page.goto('file:///C:/Users/Augusto/Desktop/AH3/painel_controle.html', {waitUntil: 'networkidle0'});
        await page.screenshot({path: 'C:/Users/Augusto/Desktop/AH3/saida/screenshot_painel_atualizado.png', fullPage: false});
        await browser.close();
        console.log('OK');
    } catch (e) {
        console.error(e);
    }
})();
