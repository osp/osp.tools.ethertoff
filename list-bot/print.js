var page = require('webpage').create();
page.open('email.html', function () {
    page.viewportSize = { width: 1190, height: 873 };
    page.paperSize = { format: 'A4', orientation: 'portrait', margin: '1cm' };
    page.render('example.pdf')
    phantom.exit()
});
