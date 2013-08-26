var page = require('webpage').create();
system = require("system")
source = system.args[1]
page.open(source, function () {
    page.viewportSize = { width: 1190, height: 873 };
    page.paperSize = { format: 'A4', orientation: 'portrait', margin: '1cm' };
    page.render(source + '.pdf')
    phantom.exit()
});
